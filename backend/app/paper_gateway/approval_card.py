"""Human operator approval card builder (read-only projection of an intent)."""

from __future__ import annotations

from typing import Optional

from .models import ApprovalCard, PaperIntent, RiskReason
from .provenance import provenance_completeness


def build_approval_card(
    intent: PaperIntent, rejection_reasons: Optional[list[RiskReason]] = None
) -> ApprovalCard:
    """Build the operator-facing approval card for an intent.

    The card makes the human-in-the-loop split explicit: ``llm_can_approve`` is
    always False and ``requires_human_approval`` always True. Approving only ever
    unlocks a paper simulation.
    """
    reasons = rejection_reasons if rejection_reasons is not None else intent.rejection_reasons
    complete, _missing = provenance_completeness(intent.provenance)
    return ApprovalCard(
        intent_id=intent.intent_id,
        ticker=intent.ticker,
        side=intent.side,
        quantity=intent.quantity,
        notional_usd=intent.notional_usd,
        validation_maturity=intent.provenance.validation_maturity,
        macro_risk_budget_ref=intent.provenance.macro_risk_budget_ref,
        data_freshness_state=intent.provenance.data_freshness_state,
        kill_switch_snapshot=intent.provenance.kill_switch_snapshot,
        provenance_complete=complete,
        risk_gate_passed=len(reasons) == 0,
        rejection_reasons=list(reasons),
    )
