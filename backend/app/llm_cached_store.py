"""Loader for bundled, sanitized cached LLM overlays.

Reads ``data/llm/<CASE>/<provider>.json`` into ``ModelOverlay`` objects. When a
provider has no safe cached artifact for a case, the fixture carries an explicit
state (e.g. ``NOT_GENERATED``) — a completed analysis is NEVER fabricated.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

from .llm_schema import (
    PROVIDER_ORDER,
    EvidenceTier,
    Factor,
    FactorVerdict,
    LLMProvider,
    LLMState,
    ModelOverlay,
)

DATA_DIR = Path(__file__).resolve().parents[2] / "data" / "llm"


def load_cases() -> list[dict]:
    path = DATA_DIR / "cases.json"
    if not path.exists():
        return []
    with open(path, encoding="utf-8") as f:
        return json.load(f).get("cases", [])


def get_case(case_id: str) -> Optional[dict]:
    for c in load_cases():
        if c["case_id"].lower() == case_id.lower():
            return c
    return None


def _factor(raw: Optional[dict]) -> Optional[Factor]:
    if not raw:
        return None
    try:
        return Factor(verdict=FactorVerdict(raw.get("verdict", "insufficient_evidence")),
                      note=raw.get("note", ""))
    except ValueError:
        return Factor(verdict=FactorVerdict.INSUFFICIENT_EVIDENCE, note=raw.get("note", ""))


def _load_overlay(case: dict, provider: LLMProvider) -> ModelOverlay:
    case_id = case["case_id"]
    path = DATA_DIR / case_id / f"{provider.value}.json"
    if not path.exists():
        # No fixture at all → explicit NOT_GENERATED (never fabricated).
        return ModelOverlay(
            provider=provider,
            model="(none)",
            ticker=case.get("ticker", case_id),
            market=case.get("market", "US"),
            data_state=LLMState.NOT_GENERATED,
            error_message="No public-safe cached artifact available for this provider/case.",
        )
    with open(path, encoding="utf-8") as f:
        raw = json.load(f)

    try:
        state = LLMState(raw.get("data_state", "NOT_GENERATED"))
    except ValueError:
        state = LLMState.SCHEMA_INVALID

    # Explicit non-usable state fixture: carry the reason, no fabricated analysis.
    if state not in {LLMState.CACHED, LLMState.AVAILABLE}:
        return ModelOverlay(
            provider=provider,
            model=raw.get("model", "(none)"),
            ticker=case.get("ticker", case_id),
            market=case.get("market", "US"),
            data_state=state,
            generated_at=raw.get("generated_at", ""),
            error_message=raw.get("reason", "Not usable."),
        )

    cov = raw.get("evidence_coverage")
    try:
        coverage = EvidenceTier(cov) if cov else None
    except ValueError:
        coverage = None

    return ModelOverlay(
        provider=provider,
        model=raw.get("model", "(none)"),
        ticker=case.get("ticker", case_id),
        market=case.get("market", "US"),
        generated_at=raw.get("generated_at", ""),
        data_state=state,
        evidence_hash=case.get("evidence_hash") or raw.get("evidence_hash"),
        evidence_coverage=coverage,
        confidence=raw.get("confidence"),
        business_quality=_factor(raw.get("business_quality")),
        moat=_factor(raw.get("moat")),
        pricing_power=_factor(raw.get("pricing_power")),
        management_capital_allocation=_factor(raw.get("management_capital_allocation")),
        valuation_view=_factor(raw.get("valuation_view")),
        red_flags=raw.get("red_flags", []),
        missing_evidence=raw.get("missing_evidence", []),
        risk_summary=raw.get("risk_summary", ""),
        tone=raw.get("tone", "neutral"),
        human_review_required=raw.get("human_review_required", False),
        source_refs=raw.get("source_refs", []),
    )


def load_case_overlays(case_id: str) -> Optional[dict]:
    case = get_case(case_id)
    if case is None:
        return None
    overlays = [_load_overlay(case, p) for p in PROVIDER_ORDER]
    return {"case": case, "overlays": overlays}
