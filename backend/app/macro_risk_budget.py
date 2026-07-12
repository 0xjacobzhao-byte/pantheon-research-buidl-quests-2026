"""Deterministic, public-safe Macro Risk Budget extractor.

A sanitized reimplementation of the production macro risk-budget contract. It is
a PURE function of a bundled macro snapshot (plus prior history for hysteresis):
same input → same output, no clock, no network, no secrets.

Regime taxonomy is the production four-quadrant growth×inflation model
(REFLATION / OVERHEAT / STAGFLATION / DEFLATION). All thresholds, ladders and
multipliers here are ILLUSTRATIVE public-safe constants — the real proprietary
thresholds are NOT ported.
"""

from __future__ import annotations

from typing import Any, Optional

RISK_BUDGET_VERSION = "public-1.1"

# Number of consecutive observations a new raw regime must persist before the
# confirmed regime flips (hysteresis). Illustrative.
OBSERVATIONS_REQUIRED = 3
# Buffer band around the 0.5 growth/inflation decision boundary that blocks a
# regime confirmation (avoids flip-flopping near the boundary). Illustrative.
SCORE_BAND_BUFFER = 0.08

# Illustrative per-regime exposure multipliers (REFLATION most favorable).
_REGIME_MULTIPLIER = {
    "REFLATION": 1.0,
    "OVERHEAT": 0.8,
    "DEFLATION": 0.6,
    "STAGFLATION": 0.4,
    "": 0.0,
}


# ---------------------------------------------------------------------------
# Regime + score
# ---------------------------------------------------------------------------

def classify_regime(growth_score: float, inflation_score: float) -> str:
    """Four-quadrant growth×inflation regime."""
    growth_rising = growth_score >= 0.5
    inflation_rising = inflation_score >= 0.5
    if growth_rising and not inflation_rising:
        return "REFLATION"
    if growth_rising and inflation_rising:
        return "OVERHEAT"
    if not growth_rising and inflation_rising:
        return "STAGFLATION"
    return "DEFLATION"


def compute_score(growth_score: float, inflation_score: float) -> float:
    """Illustrative 0–100 macro score: growth-favorable up, inflation-hot down."""
    raw = 50.0 + (growth_score - 0.5) * 80.0 - (inflation_score - 0.5) * 60.0
    return round(max(0.0, min(100.0, raw)), 1)


def _exposure_from_score(score: float) -> float:
    """Monotone step ladder: higher score → higher base exposure."""
    if score >= 70:
        return 0.90
    if score >= 55:
        return 0.60
    if score >= 45:
        return 0.40
    if score >= 35:
        return 0.25
    if score >= 25:
        return 0.10
    return 0.05


def _bucket_exposure(cap_pct: float, degraded: bool) -> str:
    if degraded:
        return "UNKNOWN"
    if cap_pct <= 0.0:
        return "NONE"
    if cap_pct >= 0.75:
        return "FULL"
    if cap_pct >= 0.50:
        return "HIGH"
    if cap_pct >= 0.30:
        return "MODERATE"
    if cap_pct >= 0.15:
        return "LOW"
    return "MINIMAL"


def _coverage_from_quality(quality: str) -> str:
    q = (quality or "").upper()
    if q == "FULL":
        return "OK"
    if q == "PARTIAL":
        return "PARTIAL"
    return "DEGRADED"


def _freshness_from_source(source: str) -> str:
    s = (source or "").upper()
    if "HARD_STALE" in s or "DEGRADED" in s or "NO_SNAPSHOT" in s or "FALLBACK" in s:
        return "DEGRADED"
    if "STALE" in s:
        return "STALE"
    return "FRESH"


# ---------------------------------------------------------------------------
# Hysteresis
# ---------------------------------------------------------------------------

def _raw_regime_of(snap: dict) -> str:
    return classify_regime(float(snap["growth_score"]), float(snap["inflation_score"]))


def _in_score_band(snap: dict) -> bool:
    g = float(snap["growth_score"])
    i = float(snap["inflation_score"])
    return abs(g - 0.5) <= SCORE_BAND_BUFFER or abs(i - 0.5) <= SCORE_BAND_BUFFER


def compute_hysteresis(history: list[dict], current: dict) -> dict:
    """Walk the ordered observation stream and derive the confirmed regime.

    Deterministic: the confirmed regime only flips after a new raw regime
    persists for ``OBSERVATIONS_REQUIRED`` consecutive observations AND the
    scores are outside the boundary buffer band.
    """
    stream = list(history) + [current]
    confirmed: Optional[str] = None
    pending: Optional[str] = None
    seen = 0
    reason = "initial_observation"
    transition_pending = False

    for snap in stream:
        raw = _raw_regime_of(snap)
        if confirmed is None:
            confirmed = raw
            pending = raw
            seen = 1
            reason = "initial_observation"
            transition_pending = False
            continue
        if raw == confirmed:
            pending = confirmed
            seen = 0
            reason = "regime_stable"
            transition_pending = False
            continue
        # raw differs from confirmed
        if raw == pending:
            seen += 1
        else:
            pending = raw
            seen = 1
        if seen >= OBSERVATIONS_REQUIRED and not _in_score_band(snap):
            confirmed = raw
            pending = raw
            seen = 0
            reason = "persistence_met"
            transition_pending = False
        else:
            transition_pending = True
            reason = "pending_transition_in_score_band" if _in_score_band(snap) else "pending_transition"

    return {
        "raw_regime": _raw_regime_of(current),
        "confirmed_regime": confirmed or "",
        "pending_regime": pending or "",
        "observations_required": OBSERVATIONS_REQUIRED,
        "observations_seen": seen,
        "transition_pending": transition_pending,
        "reason": reason,
    }


# ---------------------------------------------------------------------------
# Extractor
# ---------------------------------------------------------------------------

def degraded_budget(reason: str, as_of: str = "") -> dict[str, Any]:
    """Conservative fail-closed output — never a fabricated score/regime."""
    return {
        "version": RISK_BUDGET_VERSION,
        "score": 0.0,
        "regime": "",
        "confirmed_regime": "",
        "regime_confidence": "LOW",
        "coverage": "DEGRADED",
        "hard_stops_active": False,
        "hard_stops_triggered": [],
        "final_exposure": "UNKNOWN",
        "exposure_cap_pct": 0.0,
        "anomaly_flags": ["macro_unavailable"],
        "as_of": as_of,
        "freshness": "DEGRADED",
        "hysteresis": None,
        "degraded_reason": reason,
    }


def _is_valid_snapshot(snap: Any) -> bool:
    if not isinstance(snap, dict):
        return False
    for key in ("growth_score", "inflation_score"):
        if key not in snap:
            return False
        try:
            float(snap[key])
        except (TypeError, ValueError):
            return False
    return True


def extract_risk_budget(
    snapshot: Any, history: Optional[list[dict]] = None
) -> dict[str, Any]:
    """Pure deterministic extraction of the macro risk budget.

    Fail-closed: any missing/malformed snapshot, or a hard-degraded freshness
    state, yields a conservative ``degraded_budget`` rather than raising.
    """
    try:
        history = history or []
        if not _is_valid_snapshot(snapshot):
            as_of = snapshot.get("as_of", "") if isinstance(snapshot, dict) else ""
            return degraded_budget("missing_or_malformed_snapshot", as_of)

        freshness = _freshness_from_source(snapshot.get("freshness_source", "DB_SNAPSHOT"))
        as_of = snapshot.get("as_of", "")
        if freshness == "DEGRADED":
            return degraded_budget(
                snapshot.get("degraded_reason", "freshness_degraded"), as_of
            )

        growth = float(snapshot["growth_score"])
        inflation = float(snapshot["inflation_score"])
        regime = classify_regime(growth, inflation)
        score = compute_score(growth, inflation)
        coverage = _coverage_from_quality(snapshot.get("data_quality_summary", "FULL"))

        # Hard stops.
        hard_stops = snapshot.get("hard_stops", [])
        triggered = [
            hs.get("id", f"HS{i+1}")
            for i, hs in enumerate(hard_stops)
            if hs.get("active")
        ]
        hard_stops_active = bool(triggered)

        # Exposure: score ladder × regime multiplier, forced to 0 on any hard stop.
        base = _exposure_from_score(score)
        cap = base * _REGIME_MULTIPLIER.get(regime, 0.5)
        if hard_stops_active:
            cap = 0.0
        cap = round(cap, 3)
        final_exposure = _bucket_exposure(cap, degraded=False)

        # Hysteresis / confirmed regime.
        hyst = compute_hysteresis(history, snapshot)
        confirmed_regime = hyst["confirmed_regime"] or regime

        # Confidence.
        if coverage == "OK" and not hyst["transition_pending"]:
            confidence = "HIGH"
        elif coverage == "DEGRADED":
            confidence = "LOW"
        else:
            confidence = "MEDIUM"

        anomaly_flags = list(snapshot.get("anomaly_flags", []))
        if freshness == "STALE" and "macro_data_stale" not in anomaly_flags:
            anomaly_flags.append("macro_data_stale")

        return {
            "version": RISK_BUDGET_VERSION,
            "score": score,
            "regime": regime,
            "confirmed_regime": confirmed_regime,
            "regime_confidence": confidence,
            "coverage": coverage,
            "hard_stops_active": hard_stops_active,
            "hard_stops_triggered": triggered,
            "final_exposure": final_exposure,
            "exposure_cap_pct": cap,
            "anomaly_flags": anomaly_flags,
            "as_of": as_of,
            "freshness": freshness,
            "hysteresis": hyst,
            "degraded_reason": None,
        }
    except Exception as exc:  # noqa: BLE001 — fail closed on anything unexpected
        return degraded_budget(f"extractor_error:{type(exc).__name__}")
