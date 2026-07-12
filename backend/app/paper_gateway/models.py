"""Pydantic models + vocabularies for the paper-only trading gateway."""

from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Hard live-safety constants — fixed by construction in the public repo.
# ---------------------------------------------------------------------------

LIVE_ENABLED = False
BROKER_CONNECTED = False
REAL_ORDER_PATH = False
PAPER_ONLY = True


# ---------------------------------------------------------------------------
# Actors
# ---------------------------------------------------------------------------

class ActorType(str, Enum):
    """Who is acting. The split is load-bearing: an LLM actor can PROPOSE an
    intent but can never approve or fill it. Only a HUMAN operator approves."""

    HUMAN = "human"
    LLM = "llm"
    SYSTEM = "system"


class CreatedBySurface(str, Enum):
    """Where an intent originated."""

    RESEARCH_CONSOLE = "research_console"
    LLM_OVERLAY = "llm_overlay"
    OPERATOR_UI = "operator_ui"
    BATCH_JOB = "batch_job"


# ---------------------------------------------------------------------------
# Intent lifecycle
# ---------------------------------------------------------------------------

class IntentState(str, Enum):
    CREATED = "CREATED"
    RISK_EVALUATED = "RISK_EVALUATED"
    RISK_REJECTED = "RISK_REJECTED"
    AWAITING_APPROVAL = "AWAITING_APPROVAL"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    PAPER_FILLED = "PAPER_FILLED"


class Side(str, Enum):
    BUY = "buy"
    SELL = "sell"


# ---------------------------------------------------------------------------
# Risk rejection taxonomy — every fail-closed reason a gate can emit.
# ---------------------------------------------------------------------------

class RiskReason(str, Enum):
    MACRO_HARD_STOP = "macro_hard_stop"
    MACRO_BUDGET_EXCEEDED = "macro_budget_exceeded"
    KILL_SWITCH_TRIGGERED = "kill_switch_triggered"
    KILL_SWITCH_FEED_EXPIRED = "kill_switch_feed_expired"
    DATA_HARD_STALE = "data_hard_stale"
    DATA_MISSING = "data_missing"
    VALIDATION_NOT_READY = "validation_not_ready"
    PROVENANCE_MISSING = "provenance_missing"
    AUDIT_HASH_INVALID = "audit_hash_invalid"
    SINGLE_NAME_CAP = "single_name_cap"
    ASSET_CLASS_CAP = "asset_class_cap"
    SECTOR_CAP = "sector_cap"
    DRAWDOWN_CAP = "drawdown_cap"
    DAILY_LOSS_CAP = "daily_loss_cap"
    DAILY_TRADE_COUNT_CAP = "daily_trade_count_cap"
    INSUFFICIENT_CASH = "insufficient_cash"
    MARKET_CLOSED = "market_closed"
    RISK_POLICY_BLOCKED = "risk_policy_blocked"
    OPERATOR_APPROVAL_MISSING = "operator_approval_missing"
    LIVE_DISABLED = "live_disabled"
    LEGACY_INTENT_INELIGIBLE = "legacy_intent_ineligible"
    UNKNOWN_FAIL_CLOSED = "unknown_fail_closed"


# ---------------------------------------------------------------------------
# Provenance
# ---------------------------------------------------------------------------

class IntentProvenance(BaseModel):
    """Immutable provenance stamp attached at intent creation.

    Completeness of this stamp is itself a gate: an intent missing required
    provenance fields is rejected with ``provenance_missing`` (fail-closed).
    """

    source_module: str = Field(..., description="Originating research module, e.g. 'equity_overlay'")
    source_verdict_ref: Optional[str] = Field(None, description="Reference to the research verdict/comparison")
    validation_maturity: str = Field(
        ..., description="Validation maturity of the source signal: MATURE | PROSPECTIVE | WARMING_UP | SIGNAL_ONLY"
    )
    macro_risk_budget_ref: Optional[str] = Field(None, description="Reference to the macro risk-budget snapshot version")
    data_freshness_state: str = Field(..., description="FRESH | STALE | HARD_STALE | MISSING")
    kill_switch_snapshot: str = Field(..., description="Kill-switch state at creation: ARMED | TRIGGERED | FEED_EXPIRED")
    risk_policy_snapshot: str = Field(..., description="Risk-policy version/id in force at creation")
    actor_identity: str = Field(..., description="Sanitized actor id (never a real user id)")
    actor_type: ActorType = Field(..., description="human | llm | system")
    created_by_surface: CreatedBySurface = Field(..., description="Where the intent originated")
    audit_hash: Optional[str] = Field(None, description="SHA-256 over the canonical provenance + intent body")


# ---------------------------------------------------------------------------
# Intent + audit
# ---------------------------------------------------------------------------

class PaperIntent(BaseModel):
    """A provenance-stamped, paper-only trade intent."""

    intent_id: str = Field(..., description="Stable intent id")
    ticker: str = Field(..., description="Instrument symbol")
    asset_class: str = Field("equity", description="equity | crypto | fi | fx | commodity")
    sector: Optional[str] = Field(None, description="Sector for sector-cap checks")
    side: Side = Field(..., description="buy | sell")
    quantity: float = Field(..., description="Requested paper quantity")
    limit_price: Optional[float] = Field(None, description="Optional limit price (paper)")
    notional_usd: Optional[float] = Field(None, description="Notional in USD for cap checks")
    state: IntentState = Field(IntentState.CREATED, description="Lifecycle state")
    provenance: IntentProvenance = Field(..., description="Immutable provenance stamp")
    created_at: str = Field(..., description="Creation timestamp (UTC ISO)")
    rejection_reasons: list[RiskReason] = Field(default_factory=list, description="Risk gate rejection reasons")
    approved_by: Optional[str] = Field(None, description="Operator identity who approved (human only)")
    paper_fill: Optional["PaperFill"] = Field(None, description="Paper fill once approved + simulated")


class PaperFill(BaseModel):
    """A simulated (paper) fill. Never a real order."""

    fill_id: str = Field(..., description="Paper fill id")
    intent_id: str = Field(..., description="Parent intent id")
    filled_quantity: float = Field(..., description="Simulated filled quantity")
    fill_price: float = Field(..., description="Simulated fill price")
    slippage_bps: float = Field(..., description="Illustrative modeled slippage (bps)")
    venue: str = Field("PAPER_SIMULATOR", description="Always the paper simulator; never a broker")
    is_paper: bool = Field(True, description="Always true")
    filled_at: str = Field(..., description="Simulated fill timestamp (UTC ISO)")


class AuditEvent(BaseModel):
    """A single append-only audit-log entry, hash-chained to the previous one."""

    seq: int = Field(..., description="Monotonic sequence number")
    intent_id: str = Field(..., description="Intent this event concerns")
    event_type: str = Field(..., description="INTENT_CREATED | RISK_EVALUATED | APPROVED | REJECTED | PAPER_FILLED")
    actor_type: ActorType = Field(..., description="Actor that caused the event")
    actor_identity: str = Field(..., description="Sanitized actor id")
    detail: str = Field("", description="Human-readable detail")
    at: str = Field(..., description="Event timestamp (UTC ISO)")
    prev_hash: Optional[str] = Field(None, description="Hash of the previous event (chain link)")
    event_hash: str = Field(..., description="SHA-256 over this event + prev_hash")


PaperIntent.model_rebuild()


# ---------------------------------------------------------------------------
# Approval card + status
# ---------------------------------------------------------------------------

class ApprovalCard(BaseModel):
    """What a human operator sees before approving a paper simulation."""

    intent_id: str
    ticker: str
    side: Side
    quantity: float
    notional_usd: Optional[float]
    validation_maturity: str
    macro_risk_budget_ref: Optional[str]
    data_freshness_state: str
    kill_switch_snapshot: str
    provenance_complete: bool
    risk_gate_passed: bool
    rejection_reasons: list[RiskReason]
    requires_human_approval: bool = True
    llm_can_approve: bool = False
    live_enabled: bool = LIVE_ENABLED
    operator_note: str = Field(
        "Approval unlocks a PAPER simulation only. No broker is contacted. "
        "LLM actors can propose but never approve or fill.",
        description="Operator-facing safety note",
    )


class GatewayStatus(BaseModel):
    """Public LIVE_DISABLED proof + gateway posture."""

    live_enabled: bool = LIVE_ENABLED
    broker_connected: bool = BROKER_CONNECTED
    real_order_path: bool = REAL_ORDER_PATH
    paper_only: bool = PAPER_ONLY
    broker_adapter_present: bool = False
    llm_can_execute: bool = False
    llm_can_approve: bool = False
    human_approval_required: bool = True
    audit_append_only: bool = True
    note: str = (
        "This is a paper-only governance demo. LIVE execution is disabled by "
        "construction; there is no broker adapter, credential path, or real "
        "order path in this public repository."
    )
