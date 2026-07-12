"""Provider status endpoint helper for the five-model cockpit."""

from __future__ import annotations

from typing import Any

from .llm_cached_store import load_cases, load_case_overlays
from .llm_registry import list_providers, registered_count
from .llm_schema import PROVIDER_ORDER


def get_provider_status() -> dict[str, Any]:
    """Per-provider status across all cases (cached / offline / not-generated)."""
    providers = list_providers()
    cases = load_cases()

    coverage: dict[str, dict[str, str]] = {}
    for case in cases:
        bundle = load_case_overlays(case["case_id"])
        if not bundle:
            continue
        for overlay in bundle["overlays"]:
            coverage.setdefault(overlay.provider.value, {})[case["case_id"]] = overlay.data_state.value

    return {
        "registered_providers": registered_count(),
        "providers": providers,
        "provider_order": [p.value for p in PROVIDER_ORDER],
        "case_coverage": coverage,
        "cases": [c["case_id"] for c in cases],
        "mode": "offline_cached",
        "note": (
            "All five providers are represented. Cached/offline by default — no "
            "credential is required and no live paid LLM call is made. Providers "
            "without a public-safe cached artifact for a case report an explicit "
            "state (e.g. NOT_GENERATED), never a fabricated analysis."
        ),
    }
