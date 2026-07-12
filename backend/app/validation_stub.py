"""Forward-validation methodology stub (public-safe).

Pantheon Research does not treat an LLM overlay as an alpha oracle. Every
overlay is a *tracked artifact*: its agreement/divergence versus a second
independent model feeds a human-review queue, and any performance claim must
wait for out-of-sample forward validation. This module documents that stance
in code and emits a redacted, illustrative validation summary — it deliberately
carries NO production outcome data.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict

VALIDATION_SCHEMA_VERSION = "validation-methodology-1.0"

METHODOLOGY = [
    "The dual-LLM overlay is a qualitative research signal, not an alpha oracle.",
    "Each overlay is stored with its evidence hash, prompt version, and model id.",
    "Agreement and divergence between two independent models are computed, not assumed.",
    "Low agreement or a major divergence routes the case to a human-review queue.",
    "No forward-return or performance claim is made until out-of-sample validation "
    "against realized outcomes is complete.",
    "Validation is prospective and no-lookahead: signals are frozen at decision time "
    "and scored only against subsequently-realized data.",
]

NON_CLAIMS = [
    "No backtested or live alpha is claimed by this repository.",
    "The illustrative summary below contains NO production outcome data.",
    "Sample sizes here are illustrative and below any statistical-significance gate.",
]


def get_validation_methodology() -> Dict[str, Any]:
    """Return the methodology + a clearly-labelled illustrative summary."""
    return {
        "schema_version": VALIDATION_SCHEMA_VERSION,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "stance": "LLM overlay is a tracked research signal, not an alpha oracle.",
        "methodology": METHODOLOGY,
        "non_claims": NON_CLAIMS,
        "illustrative_summary": {
            "note": "ILLUSTRATIVE ONLY — not production outcomes, not statistically "
            "significant. Shows the shape of the validation ledger.",
            "cohort": "public-demo-illustrative",
            "signals_tracked": 2,
            "awaiting_forward_window": 2,
            "matured_and_scored": 0,
            "human_review_queue": 0,
            "performance_claim": "NONE — awaiting forward validation",
        },
    }
