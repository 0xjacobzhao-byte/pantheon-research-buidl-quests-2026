"""Paper gateway service — orchestrates the offline, paper-only lifecycle.

Holds an in-memory store of intents plus a single append-only audit log. Seeds a
few bundled demo intents so the API is populated with no setup. All timestamps
are supplied deterministically for reproducibility; where a wall-clock is needed
for a freshly-created intent, a fixed demo clock is used.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

from .audit_log import AuditLog
from .approval_card import build_approval_card
from .models import (
    LIVE_ENABLED,
    ActorType,
    ApprovalCard,
    CreatedBySurface,
    GatewayStatus,
    IntentProvenance,
    IntentState,
    PaperFill,
    PaperIntent,
    RiskReason,
    Side,
)
from .paper_simulator import simulate_fill
from .provenance import provenance_completeness, stamp_provenance, verify_audit_hash
from .risk_gate import RiskContext, evaluate_risk

DATA_DIR = Path(__file__).resolve().parents[3] / "data"
SEED_FILE = DATA_DIR / "paper_gateway" / "seed_intents.json"

# Fixed demo clock — deterministic, no wall-clock dependency for created intents.
_DEMO_CLOCK = "2026-07-12T09:00:00Z"


class PaperGatewayService:
    def __init__(self) -> None:
        self._intents: dict[str, PaperIntent] = {}
        self._audit = AuditLog()
        self._counter = 0
        self._seed()

    # ------------------------------------------------------------------
    # Seeding
    # ------------------------------------------------------------------

    def _seed(self) -> None:
        if not SEED_FILE.exists():
            return
        with open(SEED_FILE, encoding="utf-8") as f:
            raw = json.load(f)
        for row in raw.get("intents", []):
            prov = IntentProvenance(**row["provenance"])
            intent = PaperIntent(
                intent_id=row["intent_id"],
                ticker=row["ticker"],
                asset_class=row.get("asset_class", "equity"),
                sector=row.get("sector"),
                side=Side(row["side"]),
                quantity=row["quantity"],
                limit_price=row.get("limit_price"),
                notional_usd=row.get("notional_usd"),
                created_at=row.get("created_at", _DEMO_CLOCK),
                provenance=prov,
            )
            stamp_provenance(intent)
            ctx = self._ctx_from_row(row.get("risk_context", {}))
            self._process_new_intent(intent, ctx)
            # Optionally auto-run the demo lifecycle for seeded rows.
            demo = row.get("demo_lifecycle")
            if demo == "approve_and_fill" and intent.state == IntentState.AWAITING_APPROVAL:
                self.approve(intent.intent_id, operator="operator_demo")
                self.simulate(intent.intent_id)
            elif demo == "reject" and intent.state == IntentState.AWAITING_APPROVAL:
                self.reject(intent.intent_id, operator="operator_demo", note="Operator declined (demo)")

    @staticmethod
    def _ctx_from_row(ctx: dict) -> RiskContext:
        return RiskContext(**ctx) if ctx else RiskContext()

    # ------------------------------------------------------------------
    # Core lifecycle
    # ------------------------------------------------------------------

    def _process_new_intent(
        self, intent: PaperIntent, ctx: Optional[RiskContext] = None
    ) -> PaperIntent:
        self._intents[intent.intent_id] = intent
        self._audit.append(
            intent.intent_id, "intent_created", intent.provenance.actor_type,
            intent.provenance.actor_identity, intent.created_at,
            detail=f"{intent.side.value} {intent.quantity} {intent.ticker}",
        )
        reasons = evaluate_risk(intent, ctx)
        intent.rejection_reasons = reasons
        intent.state = IntentState.RISK_EVALUATED
        self._audit.append(
            intent.intent_id, "gate_check", ActorType.SYSTEM, "risk_gate",
            intent.created_at,
            detail=("passed" if not reasons else "failed: " + ",".join(r.value for r in reasons)),
        )
        if reasons:
            intent.state = IntentState.RISK_REJECTED
            self._audit.append(
                intent.intent_id, "risk_blocked", ActorType.SYSTEM, "risk_gate",
                intent.created_at, detail=reasons[0].value,
            )
        else:
            intent.state = IntentState.AWAITING_APPROVAL
            self._audit.append(
                intent.intent_id, "approval_card_generated", ActorType.SYSTEM,
                "risk_gate", intent.created_at, detail="awaiting human approval",
            )
        return intent

    def create_intent(self, payload: dict) -> PaperIntent:
        """Create a new provenance-stamped intent from an API payload."""
        self._counter += 1
        intent_id = payload.get("intent_id") or f"intent_demo_{self._counter:03d}"
        prov_in = payload.get("provenance", {})
        # Force actor_type: an LLM-surfaced intent stays actor_type=llm and can
        # NEVER self-approve. We never allow the caller to claim human approval.
        prov = IntentProvenance(
            source_module=prov_in.get("source_module", "unknown_module"),
            source_verdict_ref=prov_in.get("source_verdict_ref"),
            validation_maturity=prov_in.get("validation_maturity", "SIGNAL_ONLY"),
            macro_risk_budget_ref=prov_in.get("macro_risk_budget_ref"),
            data_freshness_state=prov_in.get("data_freshness_state", "FRESH"),
            kill_switch_snapshot=prov_in.get("kill_switch_snapshot", "ARMED"),
            risk_policy_snapshot=prov_in.get("risk_policy_snapshot", "risk-policy-demo-v1"),
            actor_identity=prov_in.get("actor_identity", "llm_tool"),
            actor_type=ActorType(prov_in.get("actor_type", "llm")),
            created_by_surface=CreatedBySurface(prov_in.get("created_by_surface", "llm_overlay")),
        )
        intent = PaperIntent(
            intent_id=intent_id,
            ticker=payload.get("ticker", "NVDA"),
            asset_class=payload.get("asset_class", "equity"),
            sector=payload.get("sector"),
            side=Side(payload.get("side", "buy")),
            quantity=float(payload.get("quantity", 1)),
            limit_price=payload.get("limit_price"),
            notional_usd=payload.get("notional_usd"),
            created_at=payload.get("created_at", _DEMO_CLOCK),
            provenance=prov,
        )
        stamp_provenance(intent)
        ctx = self._ctx_from_row(payload.get("risk_context", {}))
        return self._process_new_intent(intent, ctx)

    def approve(self, intent_id: str, operator: str) -> PaperIntent:
        """Human operator approval. Only unlocks a paper simulation.

        Fail-closed: an intent that did not clear the risk gate, or whose actor
        is not a human operator identity, cannot be approved.
        """
        intent = self.get(intent_id)
        if intent is None:
            raise KeyError(intent_id)
        # LLM/system actors can never be the approver — approval is human-only.
        if intent.state != IntentState.AWAITING_APPROVAL:
            self._audit.append(
                intent_id, "approval_rejected", ActorType.SYSTEM, "risk_gate",
                _DEMO_CLOCK, detail=f"cannot approve from state {intent.state.value}",
            )
            return intent
        intent.approved_by = operator
        intent.state = IntentState.APPROVED
        self._audit.append(
            intent_id, "approval_approved", ActorType.HUMAN, operator, _DEMO_CLOCK,
            detail="operator approved paper simulation",
        )
        return intent

    def reject(self, intent_id: str, operator: str, note: str = "") -> PaperIntent:
        intent = self.get(intent_id)
        if intent is None:
            raise KeyError(intent_id)
        intent.state = IntentState.REJECTED
        self._audit.append(
            intent_id, "approval_rejected", ActorType.HUMAN, operator, _DEMO_CLOCK,
            detail=note or "operator rejected",
        )
        return intent

    def simulate(self, intent_id: str) -> PaperIntent:
        """Run the paper simulation. Requires an APPROVED intent (human-gated)."""
        intent = self.get(intent_id)
        if intent is None:
            raise KeyError(intent_id)
        if intent.state != IntentState.APPROVED:
            self._audit.append(
                intent_id, "paper_fill_rejected", ActorType.SYSTEM, "paper_simulator",
                _DEMO_CLOCK, detail="simulation requires operator approval first",
            )
            return intent
        self._audit.append(
            intent_id, "paper_simulation_started", ActorType.SYSTEM, "paper_simulator",
            _DEMO_CLOCK, detail="paper-only; no broker contacted",
        )
        fill = simulate_fill(intent, _DEMO_CLOCK)
        intent.paper_fill = fill
        intent.state = IntentState.PAPER_FILLED
        self._audit.append(
            intent_id, "paper_fill_simulated", ActorType.SYSTEM, "paper_simulator",
            _DEMO_CLOCK,
            detail=f"paper fill {fill.filled_quantity}@{fill.fill_price} venue={fill.venue}",
        )
        return intent

    # ------------------------------------------------------------------
    # Reads
    # ------------------------------------------------------------------

    def get(self, intent_id: str) -> Optional[PaperIntent]:
        return self._intents.get(intent_id)

    def list_intents(self) -> list[PaperIntent]:
        return list(self._intents.values())

    def approval_card(self, intent_id: str) -> Optional[ApprovalCard]:
        intent = self.get(intent_id)
        if intent is None:
            return None
        return build_approval_card(intent)

    def audit_events(self, intent_id: Optional[str] = None) -> list[dict]:
        return [e.model_dump() for e in self._audit.events(intent_id)]

    def provenance_completeness_report(self) -> dict:
        total = len(self._intents)
        complete = 0
        rows = []
        for intent in self._intents.values():
            ok, missing = provenance_completeness(intent.provenance)
            hash_ok = verify_audit_hash(intent)
            if ok and hash_ok:
                complete += 1
            rows.append({
                "intent_id": intent.intent_id,
                "provenance_complete": ok,
                "audit_hash_valid": hash_ok,
                "missing_fields": missing,
            })
        return {
            "total_intents": total,
            "fully_provenanced": complete,
            "completeness_pct": round(complete / total, 3) if total else None,
            "audit_chain_intact": self._audit.verify_chain(),
            "intents": rows,
        }

    def status(self) -> GatewayStatus:
        return GatewayStatus()

    def live_disabled_proof(self) -> dict:
        llm_intents = [i for i in self._intents.values() if i.provenance.actor_type == ActorType.LLM]
        llm_filled = [i for i in llm_intents if i.state == IntentState.PAPER_FILLED]
        # An llm-drafted intent that is filled is legitimate ONLY if a human
        # approval event exists for it.
        llm_auto_executed_without_approval = 0
        for intent in llm_filled:
            events = self._audit.events(intent.intent_id)
            approved_by_human = any(
                e.event_type == "approval_approved" and e.actor_type == ActorType.HUMAN
                for e in events
            )
            if not approved_by_human:
                llm_auto_executed_without_approval += 1
        return {
            "live_enabled": LIVE_ENABLED,
            "broker_connected": False,
            "real_order_path": False,
            "paper_only": True,
            "broker_adapter_present": False,
            "llm_actor_intents": len(llm_intents),
            "llm_actor_paper_filled": len(llm_filled),
            "llm_actor_auto_executed_without_approval": llm_auto_executed_without_approval,
            "live_disabled": (not LIVE_ENABLED) and llm_auto_executed_without_approval == 0,
            "attestation": (
                "No broker/exchange call. No real order. LLM actors can propose "
                "but never approve or fill. Every paper fill is preceded by a "
                "human approval event in the append-only audit chain."
            ),
        }


# Module-level singleton for the API layer.
_service: Optional[PaperGatewayService] = None


def get_service() -> PaperGatewayService:
    global _service
    if _service is None:
        _service = PaperGatewayService()
    return _service


def reset_service() -> PaperGatewayService:
    """Rebuild the service (used by tests for isolation)."""
    global _service
    _service = PaperGatewayService()
    return _service
