"""Tests for the comparison data_state and fail-closed comparison semantics."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.comparison import build_comparison, derive_data_state
from app.models import (
    AgreementLevel,
    DataState,
    Divergence,
    LLMProvider,
    OverlayAssessment,
    OverlayStatus,
    QualitativeOverlay,
)
from app.sample_loader import load_evidence


def _overlay(provider, status, fields=None, model="test-model"):
    fields = fields or {}
    assessment = None
    if status in (OverlayStatus.SUCCESS, OverlayStatus.OFFLINE_SAMPLE):
        assessment = OverlayAssessment(
            business_quality=fields.get("business_quality", "Excellent strong quality"),
            moat=fields.get("moat", "Wide moat network effects"),
            pricing_power=fields.get("pricing_power", "Strong pricing power"),
            capital_allocation=fields.get("capital_allocation", "Disciplined allocation"),
            red_flags=fields.get("red_flags", "Some risks"),
            confidence=fields.get("confidence", 0.8),
            missing_evidence=fields.get("missing_evidence", []),
        )
    return QualitativeOverlay(
        provider=provider, model=model, ticker="MA",
        status=status, takeaway="Takeaway.", assessment=assessment,
    )


def test_data_state_offline_sample():
    q = _overlay(LLMProvider.QWEN, OverlayStatus.OFFLINE_SAMPLE)
    d = _overlay(LLMProvider.DEEPSEEK, OverlayStatus.OFFLINE_SAMPLE)
    assert derive_data_state(q, d) == DataState.OFFLINE_SAMPLE


def test_data_state_live_dual():
    q = _overlay(LLMProvider.QWEN, OverlayStatus.SUCCESS)
    d = _overlay(LLMProvider.DEEPSEEK, OverlayStatus.SUCCESS)
    assert derive_data_state(q, d) == DataState.LIVE_DUAL


def test_data_state_mixed():
    q = _overlay(LLMProvider.QWEN, OverlayStatus.SUCCESS)
    d = _overlay(LLMProvider.DEEPSEEK, OverlayStatus.OFFLINE_SAMPLE)
    assert derive_data_state(q, d) == DataState.MIXED


def test_data_state_partial_when_one_blocked():
    q = _overlay(LLMProvider.QWEN, OverlayStatus.OFFLINE_SAMPLE)
    d = _overlay(LLMProvider.DEEPSEEK, OverlayStatus.BLOCKED_BY_MISSING_CREDENTIAL)
    assert derive_data_state(q, d) == DataState.PARTIAL


def test_data_state_blocked_when_both_fail():
    q = _overlay(LLMProvider.QWEN, OverlayStatus.API_ERROR)
    d = _overlay(LLMProvider.DEEPSEEK, OverlayStatus.PARSE_ERROR)
    assert derive_data_state(q, d) == DataState.BLOCKED


def test_partial_is_not_comparable_and_requires_review():
    evidence = load_evidence("MA")
    q = _overlay(LLMProvider.QWEN, OverlayStatus.OFFLINE_SAMPLE)
    d = _overlay(LLMProvider.DEEPSEEK, OverlayStatus.API_ERROR)
    result = build_comparison(evidence, q, d)
    assert result.data_state == DataState.PARTIAL
    assert result.agreement_level == AgreementLevel.NOT_COMPARABLE
    assert result.agreement_score is None
    assert result.human_review_required is True
    assert result.human_review_reason


def test_blocked_never_fabricates_agreement():
    evidence = load_evidence("MA")
    q = _overlay(LLMProvider.QWEN, OverlayStatus.BLOCKED_BY_MISSING_CREDENTIAL)
    d = _overlay(LLMProvider.DEEPSEEK, OverlayStatus.API_ERROR)
    result = build_comparison(evidence, q, d)
    assert result.data_state == DataState.BLOCKED
    assert result.agreement_score is None
    assert result.human_review_required is True


def test_large_divergence_requires_human_review():
    evidence = load_evidence("MA")
    q = _overlay(
        LLMProvider.QWEN, OverlayStatus.OFFLINE_SAMPLE,
        fields={
            "business_quality": "Outstanding exceptional dominant superior quality",
            "moat": "Extremely wide impenetrable moat with network effects",
            "pricing_power": "Extraordinary premium pricing leadership",
            "confidence": 0.9,
        },
    )
    d = _overlay(
        LLMProvider.DEEPSEEK, OverlayStatus.OFFLINE_SAMPLE,
        fields={
            "business_quality": "Weak declining deteriorating poor negative",
            "moat": "Narrow shallow eroding easily disrupted by competition",
            "pricing_power": "Limited weak eroding discount pressure",
            "confidence": 0.3,
        },
    )
    result = build_comparison(evidence, q, d)
    assert result.data_state == DataState.OFFLINE_SAMPLE
    assert any(dv.severity == "major" for dv in result.divergences)
    assert result.human_review_required is True
    assert result.human_review_reason


def test_evidence_hash_is_threaded_through():
    evidence = load_evidence("MA")
    q = _overlay(LLMProvider.QWEN, OverlayStatus.OFFLINE_SAMPLE)
    d = _overlay(LLMProvider.DEEPSEEK, OverlayStatus.OFFLINE_SAMPLE)
    result = build_comparison(evidence, q, d, evidence_hash="sha256:deadbeef")
    assert result.evidence_hash == "sha256:deadbeef"
