"""Five-model comparison tests: deterministic math, no winner, human review."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.llm_cockpit import get_comparison
from app.llm_five_model_comparison import build_comparison
from app.llm_cached_store import load_case_overlays


def test_no_winner_declared():
    for cid in ("NVDA", "MA", "BTC"):
        comp = get_comparison(cid)
        assert comp["winner"] is None


def test_agreement_math_deterministic():
    overlays = load_case_overlays("NVDA")["overlays"]
    a = build_comparison(overlays)
    b = build_comparison(overlays)
    assert a["agreement_matrix"]["agreement_score"] == b["agreement_matrix"]["agreement_score"]
    assert a["human_review_reasons"] == b["human_review_reasons"]


def test_material_disagreement_triggers_human_review():
    comp = get_comparison("NVDA")
    assert comp["human_review_required"] is True
    assert "material_risk_disagreement" in comp["human_review_reasons"]


def test_weak_evidence_triggers_review():
    comp = get_comparison("MA")
    # qwen carries SOURCE_LIMITED_BRIEF -> weak evidence review reason.
    assert "weak_evidence" in comp["human_review_reasons"]


def test_agreement_score_is_fraction_or_none():
    comp = get_comparison("NVDA")
    score = comp["agreement_matrix"]["agreement_score"]
    assert score is None or (0.0 <= score <= 1.0)


def test_comparison_excludes_not_generated_provider():
    comp = get_comparison("BTC")
    # gemini is NOT_GENERATED and must not be a comparable provider.
    assert "gemini" not in comp["comparable_providers"]
    assert len(comp["comparable_providers"]) == 4
