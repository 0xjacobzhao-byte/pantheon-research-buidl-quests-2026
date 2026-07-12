"""Macro risk budget tests: valid / stale / missing / hard-stop / hysteresis."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.macro_risk_budget import classify_regime, extract_risk_budget
from app.macro_sample_loader import load_current_snapshot, load_history


def test_regime_quadrants():
    assert classify_regime(0.7, 0.3) == "REFLATION"
    assert classify_regime(0.7, 0.7) == "OVERHEAT"
    assert classify_regime(0.3, 0.7) == "STAGFLATION"
    assert classify_regime(0.3, 0.3) == "DEFLATION"


def test_valid_snapshot():
    rb = extract_risk_budget(load_current_snapshot(), load_history())
    assert rb["regime"] == "REFLATION"
    assert rb["confirmed_regime"] == "REFLATION"
    assert rb["freshness"] == "FRESH"
    assert rb["degraded_reason"] is None
    assert 0.0 <= rb["exposure_cap_pct"] <= 1.0
    assert rb["final_exposure"] in {"FULL", "HIGH", "MODERATE", "LOW", "MINIMAL", "NONE"}


def test_hard_stop_forces_zero_exposure():
    snap = {
        "as_of": "2026-07-01", "growth_score": 0.3, "inflation_score": 0.72,
        "data_quality_summary": "PARTIAL", "freshness_source": "DB_SNAPSHOT",
        "hard_stops": [{"id": "HS2", "active": True}], "anomaly_flags": [],
    }
    rb = extract_risk_budget(snap, [])
    assert rb["hard_stops_active"] is True
    assert "HS2" in rb["hard_stops_triggered"]
    assert rb["exposure_cap_pct"] == 0.0
    assert rb["final_exposure"] == "NONE"


def test_stale_snapshot_marks_freshness():
    snap = {
        "as_of": "2026-07-01", "growth_score": 0.6, "inflation_score": 0.4,
        "data_quality_summary": "FULL", "freshness_source": "DB_SNAPSHOT_STALE",
        "hard_stops": [], "anomaly_flags": [],
    }
    rb = extract_risk_budget(snap, [])
    assert rb["freshness"] == "STALE"
    assert "macro_data_stale" in rb["anomaly_flags"]


def test_degraded_snapshot_is_conservative():
    snap = {
        "as_of": "2026-06-01", "growth_score": 0.55, "inflation_score": 0.4,
        "data_quality_summary": "DEGRADED", "freshness_source": "DB_SNAPSHOT_HARD_STALE",
        "degraded_reason": "hard_ttl_exceeded", "hard_stops": [],
    }
    rb = extract_risk_budget(snap, [])
    assert rb["freshness"] == "DEGRADED"
    assert rb["final_exposure"] == "UNKNOWN"
    assert rb["exposure_cap_pct"] == 0.0
    assert rb["degraded_reason"] == "hard_ttl_exceeded"


def test_missing_snapshot_fails_closed():
    rb = extract_risk_budget({"as_of": "x"}, [])
    assert rb["regime"] == ""
    assert rb["final_exposure"] == "UNKNOWN"
    assert rb["degraded_reason"] == "missing_or_malformed_snapshot"
    rb2 = extract_risk_budget(None, [])
    assert rb2["degraded_reason"] == "missing_or_malformed_snapshot"


def test_extractor_is_deterministic():
    snap = load_current_snapshot()
    hist = load_history()
    assert extract_risk_budget(snap, hist) == extract_risk_budget(snap, hist)


def test_hysteresis_confirms_after_persistence():
    # A single flip should NOT immediately confirm a new regime.
    history = [
        {"as_of": f"2025-0{i}", "growth_score": 0.3, "inflation_score": 0.3,
         "data_quality_summary": "FULL", "freshness_source": "DB_SNAPSHOT"}
        for i in range(1, 6)
    ]
    flip = {"as_of": "2025-06", "growth_score": 0.65, "inflation_score": 0.3,
            "data_quality_summary": "FULL", "freshness_source": "DB_SNAPSHOT"}
    rb = extract_risk_budget(flip, history)
    assert rb["regime"] == "REFLATION"  # raw flips
    assert rb["confirmed_regime"] == "DEFLATION"  # not yet confirmed
    assert rb["hysteresis"]["transition_pending"] is True
