"""Five-model cockpit service — assembles case, comparison, and agreement views."""

from __future__ import annotations

from typing import Any, Optional

from .llm_cached_store import load_case_overlays, load_cases
from .llm_five_model_comparison import build_agreement_matrix, build_comparison


def get_cases() -> dict[str, Any]:
    cases = load_cases()
    return {
        "cases": [
            {
                "case_id": c["case_id"],
                "ticker": c.get("ticker"),
                "market": c.get("market"),
                "company_name": c.get("company_name"),
                "evidence_hash": c.get("evidence_hash"),
            }
            for c in cases
        ],
        "count": len(cases),
    }


def get_case(case_id: str) -> Optional[dict[str, Any]]:
    bundle = load_case_overlays(case_id)
    if bundle is None:
        return None
    return {
        "case": bundle["case"],
        "overlays": [o.model_dump() for o in bundle["overlays"]],
    }


def get_comparison(case_id: str) -> Optional[dict[str, Any]]:
    bundle = load_case_overlays(case_id)
    if bundle is None:
        return None
    comparison = build_comparison(bundle["overlays"])
    comparison["case"] = bundle["case"]
    return comparison


def get_agreement(case_id: str) -> Optional[dict[str, Any]]:
    bundle = load_case_overlays(case_id)
    if bundle is None:
        return None
    matrix = build_agreement_matrix(bundle["overlays"])
    return {"case": bundle["case"], "agreement_matrix": matrix}
