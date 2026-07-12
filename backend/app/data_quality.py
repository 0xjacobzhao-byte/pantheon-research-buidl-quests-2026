"""Mini Research-Ops / Data-Quality panel for the public demo.

A deliberately small, public-safe slice of Pantheon Research's internal
Research-Ops governance plane. It reports *governance state* — what is
configured, what is reachable, which overlays are usable, and which fail-closed
states are in play — without exposing any admin surface, secret, or private
dataset. It makes the demo read as a governed research system rather than an
LLM wrapper.
"""

from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import Any, Dict

from .alibaba_cloud_proof import provider_snapshot
from .comparison import build_comparison
from .evidence_pack import build_evidence_pack
from .models import DataState, OverlayStatus
from .qwen_overlay import _load_sample_overlay as _load_qwen_sample
from .deepseek_overlay import _load_sample_overlay as _load_deepseek_sample
from .sample_loader import list_available_tickers, load_evidence


def _coverage_for_ticker(ticker: str) -> Dict[str, Any]:
    """Offline coverage/state for one ticker, computed from bundled samples."""
    try:
        evidence = load_evidence(ticker)
    except FileNotFoundError:
        return {"ticker": ticker, "evidence_present": False}

    pack = build_evidence_pack(evidence)
    qwen = _load_qwen_sample(ticker)
    deepseek = _load_deepseek_sample(ticker)
    comparison = build_comparison(
        evidence, qwen, deepseek, evidence_hash=pack.provenance.evidence_hash
    )
    return {
        "ticker": ticker,
        "evidence_present": True,
        "evidence_hash": pack.provenance.evidence_hash,
        "qwen_status": qwen.status.value,
        "deepseek_status": deepseek.status.value,
        "data_state": comparison.data_state.value,
        "agreement_level": comparison.agreement_level.value,
        "human_review_required": comparison.human_review_required,
    }


def get_data_quality_report() -> Dict[str, Any]:
    """Return a secret-free data-quality / governance snapshot."""
    providers = provider_snapshot()
    demo_mode = os.environ.get("DEMO_MODE", "offline")
    tickers = list_available_tickers()
    coverage = [_coverage_for_ticker(t) for t in tickers]

    present = [c for c in coverage if c.get("evidence_present")]
    healthy = [
        c
        for c in present
        if c.get("data_state") in (DataState.LIVE_DUAL.value, DataState.OFFLINE_SAMPLE.value)
    ]

    return {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "demo_mode": demo_mode,
        "mode": "offline (bundled samples)" if demo_mode == "offline" else "live",
        "providers": {
            "qwen_configured": providers["qwen"]["configured"],
            "qwen_model": providers["qwen"]["model"],
            "deepseek_configured": providers["deepseek"]["configured"],
            "deepseek_model": providers["deepseek"]["model"],
        },
        "alibaba_proof_reachable": True,  # served in-process by this app
        "sample_evidence_coverage": {
            "tickers": tickers,
            "evidence_packs_present": len(present),
            "healthy_comparisons": len(healthy),
        },
        "overlay_statuses": coverage,
        "fail_closed_states": [s.value for s in OverlayStatus],
        "governance_note": (
            "This is a read-only, public-safe slice of Pantheon Research's "
            "Research-Ops plane. No admin actions, secrets, or private datasets "
            "are exposed. Comparisons that are not fully usable are surfaced as "
            "PARTIAL/BLOCKED and flagged for human review — never a hollow "
            "SUCCESS."
        ),
    }
