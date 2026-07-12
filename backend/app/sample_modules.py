"""Module snapshot grid — a public-safe map of the full Pantheon Research system.

Pantheon Research is a multi-asset research operating system (macro, technical,
FICC — FI/FX/commodity — and equities). This module surfaces a **context-only**
snapshot grid so a judge can see the system's full scope without any proprietary
engine, live feed, or secret being exposed.

Most cards are bundled illustrative context (`CONTEXT_ONLY` / `OFFLINE_SAMPLE`).
The two LLM/governance cards (`qwen_vs_deepseek`, `data_quality`) are computed
**live in-process** from bundled samples, so the grid reflects real state for the
parts this repo actually runs.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"
_SNAPSHOT_FILE = DATA_DIR / "redacted_traces" / "module_snapshots_redacted.json"


def _load_grid() -> Dict[str, Any]:
    with open(_SNAPSHOT_FILE, encoding="utf-8") as f:
        return json.load(f)


def _live_qwen_card(card: Dict[str, Any]) -> Dict[str, Any]:
    """Refresh the Qwen-vs-DeepSeek card from a real in-process comparison."""
    try:
        from .comparison import build_comparison
        from .evidence_pack import build_evidence_pack
        from .sample_loader import load_evidence
        from .qwen_overlay import _load_sample_overlay as _q
        from .deepseek_overlay import _load_sample_overlay as _d

        ev = load_evidence("NVDA")
        pack = build_evidence_pack(ev)
        cmp = build_comparison(ev, _q("NVDA"), _d("NVDA"), pack.provenance.evidence_hash)
        card = dict(card)
        card["data_state"] = cmp.data_state.value
        score = "n/a" if cmp.agreement_score is None else cmp.agreement_score
        review = "review required" if cmp.human_review_required else "no review needed"
        card["headline"] = (
            f"NVDA: {cmp.data_state.value}, agreement {score} "
            f"({cmp.agreement_level.value}), {review}"
        )
    except Exception:
        # Fail soft — keep the bundled headline rather than break the grid.
        pass
    return card


def _live_data_quality_card(card: Dict[str, Any]) -> Dict[str, Any]:
    """Refresh the Data-Quality card from the real governance snapshot."""
    try:
        from .data_quality import get_data_quality_report

        dq = get_data_quality_report()
        cov = dq["sample_evidence_coverage"]
        card = dict(card)
        card["headline"] = (
            f"{cov['healthy_comparisons']}/{cov['evidence_packs_present']} healthy "
            f"· mode {dq['mode']}"
        )
    except Exception:
        pass
    return card


def get_module_snapshots() -> Dict[str, Any]:
    """Return the module snapshot grid (context cards + live LLM/governance cards)."""
    grid = _load_grid()
    refreshers = {
        "qwen_vs_deepseek": _live_qwen_card,
        "data_quality": _live_data_quality_card,
    }
    modules = []
    for card in grid.get("modules", []):
        fn = refreshers.get(card.get("key"))
        modules.append(fn(card) if fn else card)

    return {
        "schema_version": grid.get("schema_version", "module-snapshots-1.0"),
        "as_of": grid.get("as_of"),
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "disclaimer": (
            "Context-only snapshots demonstrating system scope. Most cards are "
            "bundled illustrative samples, not live proprietary data. LLM and "
            "data-quality cards are computed in-process from bundled samples."
        ),
        "modules": modules,
    }
