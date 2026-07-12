"""Research Ops / Validation Console — public-safe readiness + summary.

Reports each research module's *governance* state (readiness, validation method,
record kind, PIT policy, public-performance eligibility) with a hard honesty
contract: performance fields are never invented. Modules without mature, eligible
outcomes make NO alpha/return/performance claim.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

DATA_DIR = Path(__file__).resolve().parents[2] / "data" / "research_ops"

NO_ALPHA_CLAIM = (
    "No alpha, return, or performance claim is made for modules without mature, "
    "eligible outcomes."
)


def _load(name: str) -> dict:
    path = DATA_DIR / name
    if not path.exists():
        return {}
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def get_readiness() -> dict[str, Any]:
    data = _load("readiness.json")
    data.setdefault("no_alpha_claim", NO_ALPHA_CLAIM)
    return data


def get_summary() -> dict[str, Any]:
    """Aggregate scorecard across all modules (counts only, no performance)."""
    readiness = get_readiness().get("modules", [])
    from .research_outcomes import get_outcomes  # local import to avoid cycles

    outcomes = {o["module"]: o for o in get_outcomes().get("modules", [])}

    by_readiness: dict[str, int] = {}
    eligible = 0
    matured = 0
    for m in readiness:
        by_readiness[m["readiness"]] = by_readiness.get(m["readiness"], 0) + 1
        if m.get("public_performance_eligible") is True:
            eligible += 1
        o = outcomes.get(m["module"], {})
        if o.get("performance", {}).get("hit_rate") is not None:
            matured += 1

    return {
        "schema_version": "research-ops-summary-1.0",
        "as_of": get_readiness().get("as_of"),
        "total_modules": len(readiness),
        "readiness_distribution": by_readiness,
        "public_performance_eligible_count": eligible,
        "modules_with_public_performance": matured,
        "no_alpha_claim": NO_ALPHA_CLAIM,
        "scorecards": [
            {
                "module": m["module"],
                "display_name": m["display_name"],
                "readiness": m["readiness"],
                "record_kind": m["record_kind"],
                "pit_policy": m["pit_policy"],
                "public_performance_eligible": m["public_performance_eligible"],
                "sample_count": m["sample_count"],
                "outcome_maturity": m["outcome_maturity"],
            }
            for m in readiness
        ],
    }
