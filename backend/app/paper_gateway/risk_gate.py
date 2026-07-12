"""Fail-closed risk gate.

Evaluates a provenance-stamped intent against the full rejection taxonomy. The
gate is fail-closed: any unexpected condition maps to ``unknown_fail_closed``
rather than silently passing. LIVE is always disabled, so the gate can *approve
a paper simulation* but can never authorize a real order.
"""

from __future__ import annotations

from typing import Optional

from .models import (
    LIVE_ENABLED,
    ActorType,
    IntentProvenance,
    PaperIntent,
    RiskReason,
)
from .provenance import provenance_completeness, verify_audit_hash

# Illustrative public-safe caps. Real production limits are NOT ported; these
# are round demo numbers so a judge can see each cap fire.
SINGLE_NAME_NOTIONAL_CAP_USD = 250_000.0
ASSET_CLASS_NOTIONAL_CAP_USD = 1_000_000.0
SECTOR_NOTIONAL_CAP_USD = 500_000.0
DAILY_TRADE_COUNT_CAP = 25
ACCOUNT_CASH_USD = 1_000_000.0

MATURE_MATURITIES = {"MATURE", "PROSPECTIVE"}


class RiskContext:
    """Ambient risk context supplied to the gate (all public-safe / illustrative)."""

    def __init__(
        self,
        macro_hard_stop: bool = False,
        macro_exposure_cap_pct: float = 1.0,
        macro_budget_used_pct: float = 0.0,
        kill_switch_state: str = "ARMED",
        market_open: bool = True,
        drawdown_breached: bool = False,
        daily_loss_breached: bool = False,
        daily_trade_count: int = 0,
        available_cash_usd: float = ACCOUNT_CASH_USD,
        sector_notional_used_usd: float = 0.0,
        asset_class_notional_used_usd: float = 0.0,
        risk_policy_blocked: bool = False,
    ) -> None:
        self.macro_hard_stop = macro_hard_stop
        self.macro_exposure_cap_pct = macro_exposure_cap_pct
        self.macro_budget_used_pct = macro_budget_used_pct
        self.kill_switch_state = kill_switch_state
        self.market_open = market_open
        self.drawdown_breached = drawdown_breached
        self.daily_loss_breached = daily_loss_breached
        self.daily_trade_count = daily_trade_count
        self.available_cash_usd = available_cash_usd
        self.sector_notional_used_usd = sector_notional_used_usd
        self.asset_class_notional_used_usd = asset_class_notional_used_usd
        self.risk_policy_blocked = risk_policy_blocked


def evaluate_risk(
    intent: PaperIntent, ctx: Optional[RiskContext] = None
) -> list[RiskReason]:
    """Return the list of rejection reasons (empty == passes the gate)."""
    ctx = ctx or RiskContext()
    reasons: list[RiskReason] = []

    try:
        prov: IntentProvenance = intent.provenance

        # 0. Live is disabled by construction — a live-routed intent is rejected.
        if LIVE_ENABLED:
            reasons.append(RiskReason.LIVE_DISABLED)

        # 1. Provenance completeness + integrity.
        complete, _missing = provenance_completeness(prov)
        if not complete:
            reasons.append(RiskReason.PROVENANCE_MISSING)
        if prov.audit_hash and not verify_audit_hash(intent):
            reasons.append(RiskReason.AUDIT_HASH_INVALID)
        elif not prov.audit_hash:
            reasons.append(RiskReason.AUDIT_HASH_INVALID)

        # 2. Macro governance.
        if ctx.macro_hard_stop:
            reasons.append(RiskReason.MACRO_HARD_STOP)
        if ctx.macro_budget_used_pct > ctx.macro_exposure_cap_pct:
            reasons.append(RiskReason.MACRO_BUDGET_EXCEEDED)

        # 3. Kill switch.
        if ctx.kill_switch_state == "TRIGGERED":
            reasons.append(RiskReason.KILL_SWITCH_TRIGGERED)
        elif ctx.kill_switch_state == "FEED_EXPIRED":
            reasons.append(RiskReason.KILL_SWITCH_FEED_EXPIRED)

        # 4. Data freshness.
        if prov.data_freshness_state == "HARD_STALE":
            reasons.append(RiskReason.DATA_HARD_STALE)
        elif prov.data_freshness_state == "MISSING":
            reasons.append(RiskReason.DATA_MISSING)

        # 5. Validation maturity.
        if prov.validation_maturity not in MATURE_MATURITIES:
            reasons.append(RiskReason.VALIDATION_NOT_READY)

        # 6. Position / exposure caps.
        notional = intent.notional_usd or 0.0
        if notional > SINGLE_NAME_NOTIONAL_CAP_USD:
            reasons.append(RiskReason.SINGLE_NAME_CAP)
        if ctx.asset_class_notional_used_usd + notional > ASSET_CLASS_NOTIONAL_CAP_USD:
            reasons.append(RiskReason.ASSET_CLASS_CAP)
        if ctx.sector_notional_used_usd + notional > SECTOR_NOTIONAL_CAP_USD:
            reasons.append(RiskReason.SECTOR_CAP)

        # 7. Account-level guards.
        if ctx.drawdown_breached:
            reasons.append(RiskReason.DRAWDOWN_CAP)
        if ctx.daily_loss_breached:
            reasons.append(RiskReason.DAILY_LOSS_CAP)
        if ctx.daily_trade_count >= DAILY_TRADE_COUNT_CAP:
            reasons.append(RiskReason.DAILY_TRADE_COUNT_CAP)
        if notional > ctx.available_cash_usd:
            reasons.append(RiskReason.INSUFFICIENT_CASH)

        # 8. Market + policy.
        if not ctx.market_open:
            reasons.append(RiskReason.MARKET_CLOSED)
        if ctx.risk_policy_blocked:
            reasons.append(RiskReason.RISK_POLICY_BLOCKED)

    except Exception:  # noqa: BLE001 — fail closed on any unexpected condition
        return [RiskReason.UNKNOWN_FAIL_CLOSED]

    # Deduplicate while preserving order.
    seen: set[RiskReason] = set()
    ordered: list[RiskReason] = []
    for r in reasons:
        if r not in seen:
            seen.add(r)
            ordered.append(r)
    return ordered
