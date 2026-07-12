"""Deterministic BTC layer conflict resolution.

Combines L1 (long-cycle accumulation), L2 (directional posture with a macro
gate), and L3 (tactical risk radar) plus the macro risk budget into ONE research
posture. The precedence is public-safe and structural (not a proprietary
formula):

- Degraded freshness anywhere → RESEARCH_ONLY (never act on stale/missing data).
- Macro hard stop OR L2 Guardian RED (long gate closed) → NO_TRADE (the macro
  gate zeroes a bullish signal; Hunter can never override it).
- A directional L2 signal is scaled DOWN by L3: RED/high-alert → RISK_THROTTLE,
  AMBER → SLOW_SCALE, GREEN → SLOW_SCALE (staged, never a live order).
- No dominant signal with layers disagreeing → WAIT; truly no signal → NO_TRADE.

Outputs are research postures only; this module never emits a live order.
"""

from __future__ import annotations

from typing import Any

OUTCOMES = ["NO_TRADE", "WAIT", "SLOW_SCALE", "RISK_THROTTLE", "RESEARCH_ONLY"]

_L1_ACCUMULATION = {"STRONG", "EXTREME", "MODERATE"}


def resolve_posture(
    l1: dict[str, Any], l2: dict[str, Any], l3: dict[str, Any], macro: dict[str, Any]
) -> dict[str, Any]:
    """Resolve the three layers + macro into a single research posture."""
    reasons: list[str] = []

    # 1. Freshness / degraded honesty — reference-only if any layer is degraded.
    l1_degraded = l1.get("state") == "DATA_INSUFFICIENT" or not l1.get("available", True)
    l2_missing = bool(l2.get("missing_fields"))
    l3_degraded = bool(l3.get("degraded_mode")) or l3.get("state") == "DEGRADED_AMBER"
    if l1_degraded or l2_missing or l3_degraded:
        if l1_degraded:
            reasons.append("l1_data_insufficient")
        if l2_missing:
            reasons.append("l2_missing_fields")
        if l3_degraded:
            reasons.append("l3_degraded_mode")
        return _result("RESEARCH_ONLY", reasons, l1, l2, l3, macro)

    # 2. Macro gate — hard stop or a closed long gate zeroes a bullish signal.
    macro_hard = bool(macro.get("hard_stops_active"))
    guardian_red = l2.get("guardian_state") == "RED" or float(l2.get("long_gate", 1.0)) <= 0.0
    if macro_hard:
        reasons.append("macro_hard_stop")
        return _result("NO_TRADE", reasons, l1, l2, l3, macro)
    if guardian_red:
        reasons.append("guardian_red_long_gate_closed")
        return _result("NO_TRADE", reasons, l1, l2, l3, macro)

    final = float(l2.get("final_signal_score", 0.0))
    conviction = l2.get("final_signal_conviction", "WEAK")
    directional = abs(final) >= 0.15 and conviction in ("MODERATE", "STRONG")

    # 3. Directional signal — scaled down by the risk radar (never up).
    if directional:
        l3_state = l3.get("state")
        if l3_state == "RED" or l3.get("high_alert_mode"):
            reasons.append("l3_red_or_high_alert_throttle")
            return _result("RISK_THROTTLE", reasons, l1, l2, l3, macro)
        if l3_state == "AMBER":
            reasons.append("l3_amber_reduce_pace")
            return _result("SLOW_SCALE", reasons, l1, l2, l3, macro)
        reasons.append("l2_directional_l3_green_staged")
        return _result("SLOW_SCALE", reasons, l1, l2, l3, macro)

    # 4. No dominant directional signal.
    l1_accum = l1.get("state") in _L1_ACCUMULATION
    if abs(final) < 0.05 and not l1_accum:
        reasons.append("no_signal_alignment")
        return _result("NO_TRADE", reasons, l1, l2, l3, macro)
    reasons.append("layers_disagree_no_dominant")
    return _result("WAIT", reasons, l1, l2, l3, macro)


def _result(outcome: str, reasons: list[str], l1, l2, l3, macro) -> dict[str, Any]:
    return {
        "outcome": outcome,
        "reasons": reasons,
        "layer_inputs": {
            "l1_state": l1.get("state"),
            "l2_guardian": l2.get("guardian_state"),
            "l2_final_signal_score": l2.get("final_signal_score"),
            "l2_conviction": l2.get("final_signal_conviction"),
            "l3_state": l3.get("state"),
            "macro_hard_stops_active": macro.get("hard_stops_active"),
            "macro_regime": macro.get("confirmed_regime") or macro.get("regime"),
        },
        "note": (
            "Research posture only. L2 owns direction under a macro gate; L3 "
            "modulates pace/leverage only; L1 raises long-cycle willingness only. "
            "No live order is emitted."
        ),
    }
