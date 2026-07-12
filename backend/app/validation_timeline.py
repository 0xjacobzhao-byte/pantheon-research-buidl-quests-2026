"""Validation timeline — public-safe signal lifecycle tracker.

Documents the lifecycle of a dual-LLM overlay signal from capture through
forward validation. No alpha claims are made before maturation. This is an
illustrative, sanitized timeline for the public demo.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict


def get_validation_timeline() -> Dict[str, Any]:
    """Return a signal-lifecycle timeline (illustrative, no production outcomes)."""
    return {
        "schema_version": "validation-timeline-1.0",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "stance": (
            "The dual-LLM overlay is a tracked research signal, not an alpha "
            "oracle. No performance claim is made before forward validation."
        ),
        "stages": [
            {
                "stage": 1,
                "name": "Signal Captured",
                "status": "COMPLETE",
                "description": (
                    "Dual-LLM overlay generated for ticker. Both Qwen and "
                    "DeepSeek assessments stored with model version and "
                    "prompt version metadata."
                ),
                "evidence": "overlay stored with provider, model, ticker, status",
            },
            {
                "stage": 2,
                "name": "Evidence Hash Attached",
                "status": "COMPLETE",
                "description": (
                    "Evidence pack content committed to a SHA-256 hash. "
                    "Hash threaded into comparison record for provenance."
                ),
                "evidence": "evidence_hash: sha256:...",
            },
            {
                "stage": 3,
                "name": "Model Versions Recorded",
                "status": "COMPLETE",
                "description": (
                    "Qwen model (e.g. qwen-plus / qwen3.7-plus) and DeepSeek "
                    "model (e.g. deepseek-chat) recorded with prompt version "
                    "and output schema version."
                ),
                "evidence": "qwen_overlay.model, deepseek_overlay.model, prompt_version",
            },
            {
                "stage": 4,
                "name": "Agreement & Divergence Scored",
                "status": "COMPLETE",
                "description": (
                    "Jaccard-based agreement score computed. Divergences "
                    "classified by severity. Human-review gate evaluated."
                ),
                "evidence": "agreement_score, agreement_level, divergences[], human_review_required",
            },
            {
                "stage": 5,
                "name": "Outcome Window Pending",
                "status": "AWAITING",
                "description": (
                    "Forward-validation window has not yet elapsed. Signal "
                    "is frozen at decision time; no lookahead scoring."
                ),
                "evidence": "no forward return joined yet",
            },
            {
                "stage": 6,
                "name": "Forward Validation Required",
                "status": "PENDING",
                "description": (
                    "Signal must be scored against subsequently-realized "
                    "outcomes (no-lookahead). Only then can any performance "
                    "characterization be made."
                ),
                "evidence": "validation ledger entry will be created",
            },
        ],
        "non_claims": [
            "No alpha or return performance is claimed by this repository.",
            "No backtested results are published here.",
            "Signal quality is tracked; performance characterization awaits forward validation.",
            "The overlay is a research signal — LLMs never execute trades.",
        ],
        "illustrative_demo_summary": {
            "note": (
                "ILLUSTRATIVE ONLY — not production outcomes, not statistically "
                "significant. Shows the shape of the validation ledger."
            ),
            "cohort": "public-demo-illustrative",
            "signals_captured": 2,
            "evidence_hashed": 2,
            "models_recorded": 2,
            "awaiting_forward_window": 2,
            "matured_and_scored": 0,
            "performance_claim": "NONE — awaiting forward validation",
        },
    }
