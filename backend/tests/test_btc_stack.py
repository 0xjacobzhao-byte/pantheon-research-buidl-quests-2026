"""BTC three-layer stack tests: conflict determinism, macro override, honesty."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.btc_stack import get_stack, get_conflicts, get_current_posture
from app.btc_history import get_history
from app.btc_conflict_resolution import resolve_posture, OUTCOMES


def test_stack_has_three_layers():
    stack = get_stack()
    assert stack["l1"] and stack["l2"] and stack["l3"]
    assert "resolved_posture" in stack


def test_current_posture_is_valid_outcome():
    posture = get_current_posture()
    assert posture["outcome"] in OUTCOMES


def test_conflict_examples_match_expected():
    for ex in get_conflicts()["examples"]:
        assert ex["matches_expected"] is True, f"{ex['id']} -> {ex['resolved_outcome']}"


def test_conflict_resolution_deterministic():
    l1 = {"state": "MODERATE", "available": True}
    l2 = {"guardian_state": "GREEN", "long_gate": 1.0, "final_signal_score": 0.3,
          "final_signal_conviction": "MODERATE", "missing_fields": []}
    l3 = {"state": "AMBER", "high_alert_mode": False, "degraded_mode": False}
    macro = {"hard_stops_active": False, "confirmed_regime": "REFLATION"}
    assert resolve_posture(l1, l2, l3, macro) == resolve_posture(l1, l2, l3, macro)


def test_macro_hard_stop_overrides_bullish_signal():
    l1 = {"state": "MODERATE", "available": True}
    l2 = {"guardian_state": "GREEN", "long_gate": 1.0, "final_signal_score": 0.7,
          "final_signal_conviction": "STRONG", "missing_fields": []}
    l3 = {"state": "GREEN", "high_alert_mode": False, "degraded_mode": False}
    macro = {"hard_stops_active": True, "confirmed_regime": "STAGFLATION"}
    out = resolve_posture(l1, l2, l3, macro)
    assert out["outcome"] == "NO_TRADE"
    assert "macro_hard_stop" in out["reasons"]


def test_missing_l2_input_stays_research_only():
    l1 = {"state": "MODERATE", "available": True}
    l2 = {"guardian_state": "GREEN", "long_gate": 1.0, "final_signal_score": None,
          "final_signal_conviction": "WEAK", "missing_fields": ["hunter_state"]}
    l3 = {"state": "AMBER", "high_alert_mode": False, "degraded_mode": False}
    macro = {"hard_stops_active": False}
    assert resolve_posture(l1, l2, l3, macro)["outcome"] == "RESEARCH_ONLY"


def test_no_trade_order_output():
    # The posture vocabulary contains no direct order instruction.
    for outcome in OUTCOMES:
        assert outcome not in ("BUY", "SELL", "PLACE_ORDER", "EXECUTE")


def test_weekly_history_preserves_timestamps():
    hist = get_history()
    assert hist["count"] >= 200
    assert hist["cadence"] == "weekly"
    for row in hist["rows"][:5]:
        assert row.get("date")
        assert "risk_radar_state" in row
