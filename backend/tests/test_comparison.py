"""Tests for the comparison, tone, divergence, and agreement logic."""

import os
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.comparison import (
    classify_tone,
    detect_divergences,
    compute_agreement_score,
    agreement_level_from_score,
    collect_evidence_gaps,
    load_comparison_from_sample,
    run_comparison,
)
from app.models import (
    AgreementLevel,
    COMPARISON_FIELDS,
    EquityEvidence,
    LLMProvider,
    OverlayAssessment,
    OverlayStatus,
    QualitativeOverlay,
    Tone,
    AlibabaCloudProof,
    QwenConfig,
    ProjectInfo,
)
from app.sample_loader import list_available_tickers, load_evidence


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def ma_evidence():
    return load_evidence("MA")


def _make_overlay(
    provider=LLMProvider.QWEN,
    assessment_fields: dict | None = None,
    takeaway="Strong business.",
    status=OverlayStatus.OFFLINE_SAMPLE,
):
    af = assessment_fields or {}
    a = OverlayAssessment(
        business_quality=af.get("business_quality", "Excellent."),
        moat=af.get("moat", "Wide moat."),
        pricing_power=af.get("pricing_power", "Strong."),
        capital_allocation=af.get("capital_allocation", "Disciplined."),
        red_flags=af.get("red_flags", "Some risks."),
        confidence=af.get("confidence", 0.8),
        missing_evidence=af.get("missing_evidence", ["No real-time data"]),
    )
    return QualitativeOverlay(
        provider=provider,
        model="test-model",
        ticker="MA",
        status=status,
        takeaway=takeaway,
        assessment=a,
    )


# ---------------------------------------------------------------------------
# Model tests
# ---------------------------------------------------------------------------

class TestModels:
    def test_comparison_fields(self):
        assert COMPARISON_FIELDS == [
            "business_quality",
            "moat",
            "pricing_power",
            "capital_allocation",
            "red_flags",
            "confidence",
            "missing_evidence",
        ]

    def test_overlay_status_values(self):
        assert OverlayStatus.OFFLINE_SAMPLE.value == "OFFLINE_SAMPLE"
        assert OverlayStatus.BLOCKED_BY_MISSING_CREDENTIAL.value == "BLOCKED_BY_MISSING_CREDENTIAL"

    def test_tone_values(self):
        assert Tone.POSITIVE.value == "positive"
        assert Tone.CONSERVATIVE_POSITIVE.value == "conservative_positive"

    def test_agreement_level_values(self):
        assert AgreementLevel.HIGH.value == "HIGH"
        assert AgreementLevel.MEDIUM.value == "MEDIUM"
        assert AgreementLevel.LOW.value == "LOW"

    def test_project_info(self):
        info = ProjectInfo()
        assert "Strategy" in info.architecture_layers
        assert "Trading" in info.architecture_layers
        assert "human-in-the-loop" in info.safety_statement

    def test_alibaba_proof_fields(self):
        from app.alibaba_cloud_proof import get_alibaba_proof

        proof = get_alibaba_proof()
        assert proof.schema_version == "alibaba-proof-2.0"
        assert proof.cloud_provider == "Alibaba Cloud"
        assert proof.backend_runtime == "Dockerized FastAPI"
        assert proof.reverse_proxy == "Nginx"
        assert "DashScope" in proof.qwen_provider
        # Precise, non-overclaiming database representation.
        assert proof.database.production_data_migrated is False
        assert proof.database.connected is None

    def test_qwen_config(self):
        cfg = QwenConfig()
        assert "dashscope" in cfg.base_url
        assert cfg.credential_configured is False


# ---------------------------------------------------------------------------
# Tone classification tests
# ---------------------------------------------------------------------------

class TestToneClassification:
    def test_positive_tone(self):
        overlay = _make_overlay(
            takeaway="Excellent outstanding robust strong growth powerful premium superior",
            assessment_fields={"business_quality": "Excellent strong dominant"},
        )
        assert classify_tone(overlay) == Tone.POSITIVE

    def test_conservative_positive_tone(self):
        overlay = _make_overlay(
            takeaway="Excellent strong robust growth but regulatory risk valuation concern",
            assessment_fields={
                "business_quality": "Excellent strong",
                "red_flags": "Risk concern elevated premium valuation",
            },
        )
        tone = classify_tone(overlay)
        assert tone in (Tone.CONSERVATIVE_POSITIVE, Tone.POSITIVE)

    def test_blocked_returns_neutral(self):
        overlay = _make_overlay(
            status=OverlayStatus.BLOCKED_BY_MISSING_CREDENTIAL,
            takeaway="",
            assessment_fields={
                "business_quality": "", "moat": "", "pricing_power": "",
                "capital_allocation": "", "red_flags": "",
            },
        )
        assert classify_tone(overlay) == Tone.NEUTRAL

    def test_empty_text_returns_neutral(self):
        overlay = _make_overlay(takeaway="", assessment_fields={
            "business_quality": "", "moat": "", "pricing_power": "",
            "capital_allocation": "", "red_flags": "",
        })
        assert classify_tone(overlay) == Tone.NEUTRAL

    def test_parse_error_returns_neutral(self):
        # A PARSE_ERROR overlay is unusable — it must not be scored as a tone.
        overlay = _make_overlay(status=OverlayStatus.PARSE_ERROR, takeaway="")
        assert classify_tone(overlay) == Tone.NEUTRAL


# ---------------------------------------------------------------------------
# Parse-failure handling: invalid JSON must surface, never a hollow SUCCESS
# ---------------------------------------------------------------------------

class TestParseFailure:
    def test_parse_error_status_exists(self):
        assert OverlayStatus.PARSE_ERROR.value == "PARSE_ERROR"

    def test_qwen_parser_raises_on_invalid_json(self):
        from app import qwen_overlay
        with pytest.raises(ValueError):
            qwen_overlay._parse_json_response("this is not json at all")

    def test_deepseek_parser_raises_on_invalid_json(self):
        from app import deepseek_overlay
        with pytest.raises(ValueError):
            deepseek_overlay._parse_json_response("<html>nope</html>")

    def test_qwen_parser_still_reads_fenced_json(self):
        from app import qwen_overlay
        out = qwen_overlay._parse_json_response('```json\n{"takeaway": "ok"}\n```')
        assert out["takeaway"] == "ok"


# ---------------------------------------------------------------------------
# Divergence detection tests
# ---------------------------------------------------------------------------

class TestDivergenceDetection:
    def test_no_divergences_similar(self):
        qwen = _make_overlay(assessment_fields={
            "business_quality": "Excellent business with strong margins",
            "moat": "Wide moat with network effects",
        })
        deepseek = _make_overlay(provider=LLMProvider.DEEPSEEK, assessment_fields={
            "business_quality": "Excellent business with strong margins",
            "moat": "Wide moat with network effects",
        })
        divergences = detect_divergences(qwen, deepseek)
        assert len(divergences) == 0

    def test_major_divergence(self):
        qwen = _make_overlay(assessment_fields={
            "business_quality": "Outstanding exceptional dominant superior quality",
            "moat": "Extremely wide impenetrable moat with network effects",
        })
        deepseek = _make_overlay(provider=LLMProvider.DEEPSEEK, assessment_fields={
            "business_quality": "Weak declining deteriorating poor negative",
            "moat": "Narrow shallow moat easily disrupted by competition",
        })
        divergences = detect_divergences(qwen, deepseek)
        assert len(divergences) >= 1
        assert any(d.severity == "major" for d in divergences)

    def test_missing_assessment_returns_empty(self):
        qwen = QualitativeOverlay(
            provider=LLMProvider.QWEN, model="t", ticker="MA",
            status=OverlayStatus.OFFLINE_SAMPLE, takeaway="x", assessment=None,
        )
        deepseek = _make_overlay()
        assert detect_divergences(qwen, deepseek) == []


# ---------------------------------------------------------------------------
# Agreement scoring tests
# ---------------------------------------------------------------------------

class TestAgreementScoring:
    def test_high_agreement(self):
        qwen = _make_overlay(assessment_fields={"confidence": 0.85})
        deepseek = _make_overlay(provider=LLMProvider.DEEPSEEK, assessment_fields={"confidence": 0.82})
        divergences = []
        score = compute_agreement_score(qwen, deepseek, divergences, Tone.POSITIVE, Tone.POSITIVE)
        assert score >= 0.75
        assert agreement_level_from_score(score) == AgreementLevel.HIGH

    def test_low_agreement_with_major_divergence(self):
        from app.models import Divergence
        qwen = _make_overlay(assessment_fields={"confidence": 0.9})
        deepseek = _make_overlay(provider=LLMProvider.DEEPSEEK, assessment_fields={"confidence": 0.3})
        divergences = [
            Divergence(field="moat", qwen_view="wide", deepseek_view="narrow", severity="major"),
            Divergence(field="red_flags", qwen_view="low risk", deepseek_view="high risk", severity="major"),
            Divergence(field="pricing_power", qwen_view="strong", deepseek_view="weak", severity="major"),
        ]
        score = compute_agreement_score(qwen, deepseek, divergences, Tone.POSITIVE, Tone.NEGATIVE)
        assert score < 0.5
        assert agreement_level_from_score(score) == AgreementLevel.LOW

    def test_level_thresholds(self):
        assert agreement_level_from_score(0.80) == AgreementLevel.HIGH
        assert agreement_level_from_score(0.60) == AgreementLevel.MEDIUM
        assert agreement_level_from_score(0.30) == AgreementLevel.LOW


# ---------------------------------------------------------------------------
# Evidence gaps tests
# ---------------------------------------------------------------------------

class TestEvidenceGaps:
    def test_deduplicates_gaps(self):
        qwen = _make_overlay(assessment_fields={
            "missing_evidence": ["No real-time data", "No guidance"],
        })
        deepseek = _make_overlay(provider=LLMProvider.DEEPSEEK, assessment_fields={
            "missing_evidence": ["No real-time data", "No filings"],
        })
        gaps = collect_evidence_gaps(qwen, deepseek)
        assert len(gaps) == 3
        assert "No real-time data" in gaps
        assert "No guidance" in gaps
        assert "No filings" in gaps


# ---------------------------------------------------------------------------
# Sample loader tests
# ---------------------------------------------------------------------------

class TestSampleLoader:
    def test_list_tickers(self):
        tickers = list_available_tickers()
        assert "MA" in tickers
        assert "NVDA" in tickers

    def test_load_evidence_ma(self, ma_evidence):
        assert ma_evidence.ticker == "MA"
        assert ma_evidence.company_name is not None

    def test_load_evidence_nvda(self):
        ev = load_evidence("NVDA")
        assert ev.ticker == "NVDA"


# ---------------------------------------------------------------------------
# Full comparison tests (offline)
# ---------------------------------------------------------------------------

class TestComparisonOffline:
    @pytest.mark.asyncio
    async def test_run_comparison_ma(self):
        os.environ["DEMO_MODE"] = "offline"
        evidence = load_evidence("MA")
        result = await run_comparison(evidence)
        assert result.ticker == "MA"
        assert result.qwen_overlay.provider == LLMProvider.QWEN
        assert result.deepseek_overlay.provider == LLMProvider.DEEPSEEK
        assert 0.0 <= result.agreement_score <= 1.0
        assert isinstance(result.divergences, list)
        assert isinstance(result.evidence_gaps, list)

    @pytest.mark.asyncio
    async def test_run_comparison_nvda(self):
        os.environ["DEMO_MODE"] = "offline"
        evidence = load_evidence("NVDA")
        result = await run_comparison(evidence)
        assert result.ticker == "NVDA"
        assert result.qwen_overlay.assessment is not None
        assert result.deepseek_overlay.assessment is not None
        assert result.qwen_overlay.assessment.confidence > 0
        assert result.deepseek_overlay.assessment.confidence > 0
