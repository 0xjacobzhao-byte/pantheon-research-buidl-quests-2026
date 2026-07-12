"""BTC three-layer decision stack — public-safe offline service.

Loads bundled L1/L2/L3 layer states and combines them (with the macro risk
budget) into a single research posture. Missing fields are surfaced honestly and
never fabricated. No live order is ever produced.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Optional

from .btc_conflict_resolution import resolve_posture
from .macro_risk_budget import extract_risk_budget
from .macro_sample_loader import load_current_snapshot, load_history

DATA_DIR = Path(__file__).resolve().parents[2] / "data" / "btc"


def _load(name: str, default: Any) -> Any:
    path = DATA_DIR / name
    if not path.exists():
        return default
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def load_current() -> dict:
    return _load("current.json", {})


def _macro_budget() -> dict:
    return extract_risk_budget(load_current_snapshot(), load_history())


def get_stack() -> dict:
    """Full current stack: L1/L2/L3 + macro input + resolved posture."""
    current = load_current()
    l1 = current.get("l1", {})
    l2 = current.get("l2", {})
    l3 = current.get("l3", {})
    macro = _macro_budget()
    posture = resolve_posture(l1, l2, l3, macro)
    return {
        "as_of": current.get("as_of", ""),
        "l1": l1,
        "l2": l2,
        "l3": l3,
        "macro_risk_budget": {
            "regime": macro.get("regime"),
            "confirmed_regime": macro.get("confirmed_regime"),
            "hard_stops_active": macro.get("hard_stops_active"),
            "exposure_cap_pct": macro.get("exposure_cap_pct"),
            "final_exposure": macro.get("final_exposure"),
        },
        "resolved_posture": posture,
        "missing_fields": {
            "l2": l2.get("missing_fields", []),
        },
        "disclaimer": (
            "Research posture only. Layer states are bundled illustrative samples; "
            "no live order path exists in this public repository."
        ),
    }


def get_current_posture() -> dict:
    stack = get_stack()
    return {
        "as_of": stack["as_of"],
        "outcome": stack["resolved_posture"]["outcome"],
        "reasons": stack["resolved_posture"]["reasons"],
        "layer_inputs": stack["resolved_posture"]["layer_inputs"],
        "note": stack["resolved_posture"]["note"],
    }


def get_conflicts() -> dict:
    """Return each bundled conflict example with its deterministically-resolved
    outcome, and whether it matches the documented expected outcome."""
    examples = _load("conflict_examples.json", {}).get("examples", [])
    resolved = []
    for ex in examples:
        macro = ex.get("macro", {})
        out = resolve_posture(ex.get("l1", {}), ex.get("l2", {}), ex.get("l3", {}), macro)
        resolved.append({
            "id": ex["id"],
            "title": ex["title"],
            "inputs": {k: ex.get(k) for k in ("l1", "l2", "l3", "macro")},
            "resolved_outcome": out["outcome"],
            "expected_outcome": ex.get("expected_outcome"),
            "matches_expected": out["outcome"] == ex.get("expected_outcome"),
            "reasons": out["reasons"],
        })
    return {
        "examples": resolved,
        "outcomes_vocabulary": ["NO_TRADE", "WAIT", "SLOW_SCALE", "RISK_THROTTLE", "RESEARCH_ONLY"],
        "note": "Conflict resolution is deterministic and public-safe; no live order is emitted.",
    }
