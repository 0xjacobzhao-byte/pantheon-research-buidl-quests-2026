"""Pydantic models for equity evidence, LLM qualitative overlay, and dual-provider comparison."""

from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class LLMProvider(str, Enum):
    """Supported LLM providers."""

    QWEN = "qwen"
    DEEPSEEK = "deepseek"


class OverlayStatus(str, Enum):
    """Per-provider status of a single LLM overlay response.

    This is the provider-level status. It is deliberately explicit so callers
    can never mistake a silently-empty response for a real assessment.
    """

    SUCCESS = "SUCCESS"
    OFFLINE_SAMPLE = "OFFLINE_SAMPLE"
    BLOCKED_BY_MISSING_CREDENTIAL = "BLOCKED_BY_MISSING_CREDENTIAL"
    API_ERROR = "API_ERROR"
    PARSE_ERROR = "PARSE_ERROR"
    QWEN_NOT_GENERATED = "QWEN_NOT_GENERATED"


# States that carry a usable, structured assessment.
USABLE_STATUSES = {OverlayStatus.SUCCESS, OverlayStatus.OFFLINE_SAMPLE}


class DataState(str, Enum):
    """Comparison-level data state — the honest headline for a comparison.

    Derived from the two provider statuses. It tells a judge, at a glance,
    whether they are looking at a live dual-model result, bundled samples, a
    single-sided result, or a fail-closed state — never a hollow SUCCESS.
    """

    LIVE_DUAL = "LIVE_DUAL"            # both providers returned live SUCCESS
    OFFLINE_SAMPLE = "OFFLINE_SAMPLE"  # both overlays from bundled samples
    MIXED = "MIXED"                    # one live, one sample
    PARTIAL = "PARTIAL"                # exactly one provider usable
    BLOCKED = "BLOCKED"                # neither provider usable (fail-closed)


class AgreementLevel(str, Enum):
    """Agreement level between two providers."""

    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    NOT_COMPARABLE = "NOT_COMPARABLE"


class Tone(str, Enum):
    """Tone classification for an overlay."""

    POSITIVE = "positive"
    CONSERVATIVE_POSITIVE = "conservative_positive"
    CAUTIOUS = "cautious"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"


# ---------------------------------------------------------------------------
# Evidence
# ---------------------------------------------------------------------------

class EquityEvidence(BaseModel):
    """Quantitative evidence data for a stock ticker."""

    ticker: str = Field(..., description="Stock ticker, e.g. MA, NVDA")
    company_name: str = Field(..., description="Full company name")
    exchange: str = Field(..., description="Exchange, e.g. NYSE, NASDAQ")
    sector: str = Field(..., description="GICS sector")
    industry: str = Field(..., description="GICS industry")
    market_cap_usd: float = Field(..., description="Market cap in USD")
    pe_ratio: Optional[float] = Field(None, description="P/E ratio (TTM)")
    pb_ratio: Optional[float] = Field(None, description="P/B ratio")
    roic_pct: Optional[float] = Field(None, description="ROIC (%)")
    fcf_ttm_usd: Optional[float] = Field(None, description="FCF TTM (USD)")
    revenue_growth_yoy_pct: Optional[float] = Field(None, description="Revenue growth YoY (%)")
    gross_margin_pct: Optional[float] = Field(None, description="Gross margin (%)")
    net_margin_pct: Optional[float] = Field(None, description="Net margin (%)")
    dividend_yield_pct: Optional[float] = Field(None, description="Dividend yield (%)")
    debt_to_equity: Optional[float] = Field(None, description="Debt-to-equity")
    summary: str = Field(..., description="Business description")


class EvidenceSource(BaseModel):
    """A sanitized provenance label for a slice of the evidence pack.

    Only public-safe labels are ever emitted — never a provider key, private
    URL, or account id.
    """

    group: str = Field(..., description="Evidence group, e.g. 'fundamentals'")
    label: str = Field(..., description="Human-readable source label")
    origin: str = Field(..., description="Sanitized origin, e.g. 'bundled_sample'")
    as_of: str = Field(..., description="As-of date (ISO) for this slice")


class EvidenceProvenance(BaseModel):
    """Provenance envelope committing an evidence pack to a content hash."""

    evidence_schema_version: str = Field(..., description="Evidence schema version")
    evidence_hash: str = Field(..., description="SHA-256 of the canonical evidence JSON")
    generated_at_utc: str = Field(..., description="Pack build timestamp (UTC ISO)")
    sources: list[EvidenceSource] = Field(default_factory=list, description="Per-group provenance")
    redaction_note: str = Field(
        "Public demo evidence is bundled and sanitized; no private datasets are included.",
        description="Redaction disclosure",
    )


class EvidencePack(BaseModel):
    """Evidence + provenance, returned by /api/evidence/{ticker}."""

    evidence: EquityEvidence = Field(..., description="Quantitative evidence")
    provenance: EvidenceProvenance = Field(..., description="Provenance & content hash")


# ---------------------------------------------------------------------------
# Overlay assessment
# ---------------------------------------------------------------------------

COMPARISON_FIELDS = [
    "business_quality",
    "moat",
    "pricing_power",
    "capital_allocation",
    "red_flags",
    "confidence",
    "missing_evidence",
]
"""Standardized comparison fields shared across all providers."""


class OverlayAssessment(BaseModel):
    """Structured assessment fields produced by an LLM overlay."""

    business_quality: str = Field("", description="Assessment of business quality")
    moat: str = Field("", description="Assessment of moat & competitive advantage")
    pricing_power: str = Field("", description="Assessment of pricing power")
    capital_allocation: str = Field("", description="Assessment of management & capital allocation")
    red_flags: str = Field("", description="Identified red flags & risks")
    confidence: float = Field(0.5, description="Model confidence (0–1)")
    missing_evidence: list[str] = Field(default_factory=list, description="Evidence gaps identified by the model")


class TokenUsage(BaseModel):
    """Optional token/cost metadata when the provider returns it."""

    prompt_tokens: Optional[int] = Field(None, description="Prompt tokens")
    completion_tokens: Optional[int] = Field(None, description="Completion tokens")
    total_tokens: Optional[int] = Field(None, description="Total tokens")
    estimated_cost_usd: Optional[float] = Field(None, description="Estimated cost (USD), placeholder")


# ---------------------------------------------------------------------------
# Overlay
# ---------------------------------------------------------------------------

class QualitativeOverlay(BaseModel):
    """Full qualitative overlay output from one LLM provider."""

    provider: LLMProvider = Field(..., description="LLM provider")
    model: str = Field(..., description="Model identifier")
    ticker: str = Field(..., description="Stock ticker")
    status: OverlayStatus = Field(..., description="Provider-level response status")
    takeaway: str = Field("", description="One-paragraph LLM takeaway")
    assessment: Optional[OverlayAssessment] = Field(None, description="Structured assessment fields")
    error_message: Optional[str] = Field(None, description="Error if status is not usable")
    latency_ms: Optional[int] = Field(None, description="Response latency (ms)")
    attempts: int = Field(1, description="Number of provider attempts (incl. retries)")
    prompt_version: Optional[str] = Field(None, description="Prompt template version")
    output_schema_version: Optional[str] = Field(None, description="Expected output schema version")
    usage: Optional[TokenUsage] = Field(None, description="Token/cost metadata if returned")


# ---------------------------------------------------------------------------
# Divergence
# ---------------------------------------------------------------------------

class Divergence(BaseModel):
    """A single point of divergence between two providers."""

    field: str = Field(..., description="Comparison field name")
    qwen_view: str = Field("", description="Qwen's position")
    deepseek_view: str = Field("", description="DeepSeek's position")
    severity: str = Field("minor", description="minor | moderate | major")


# ---------------------------------------------------------------------------
# Comparison result
# ---------------------------------------------------------------------------

class ComparisonResult(BaseModel):
    """Side-by-side comparison of Qwen and DeepSeek overlays."""

    ticker: str = Field(..., description="Stock ticker")
    data_state: DataState = Field(DataState.OFFLINE_SAMPLE, description="Headline comparison data state")
    qwen_status: OverlayStatus = Field(..., description="Qwen provider status")
    deepseek_status: OverlayStatus = Field(..., description="DeepSeek provider status")
    evidence: EquityEvidence = Field(..., description="Underlying evidence")
    evidence_hash: Optional[str] = Field(None, description="Evidence content hash used for this comparison")
    qwen_overlay: QualitativeOverlay = Field(..., description="Qwen overlay")
    deepseek_overlay: QualitativeOverlay = Field(..., description="DeepSeek overlay")
    agreement_score: Optional[float] = Field(None, description="Agreement score 0–1 (None if not comparable)")
    agreement_level: AgreementLevel = Field(AgreementLevel.MEDIUM, description="HIGH / MEDIUM / LOW / NOT_COMPARABLE")
    qwen_tone: Tone = Field(Tone.NEUTRAL, description="Qwen tone classification")
    deepseek_tone: Tone = Field(Tone.NEUTRAL, description="DeepSeek tone classification")
    divergences: list[Divergence] = Field(default_factory=list, description="Divergences between providers")
    evidence_gaps: list[str] = Field(default_factory=list, description="Combined evidence gaps")
    human_review_required: bool = Field(False, description="Whether human review is needed")
    human_review_reason: Optional[str] = Field(None, description="Why human review was flagged")


# ---------------------------------------------------------------------------
# Project info
# ---------------------------------------------------------------------------

class ProjectInfo(BaseModel):
    """Project metadata for the /api/project endpoint."""

    name: str = "Pantheon Research — BUIDL_QUESTS 2026"
    description: str = (
        "AI-native investment research operating system for public markets: "
        "structured evidence packs, deterministic signals, and multi-model "
        "LLM research overlays with side-by-side comparison and a human-review gate."
    )
    author: str = "Jacob Zhao"
    github: str = "https://github.com/0xjacobzhao-byte/pantheon-research-buidl-quests-2026"
    license: str = "Apache-2.0"
    version: str = "1.0.0"
    demo_mode: str = "offline"
    architecture_layers: list[str] = Field(
        default_factory=lambda: ["Strategy", "Information", "Signal", "Trading"]
    )
    safety_statement: str = (
        "Pantheon Research is not an autonomous trading bot. "
        "It is a framework-first, data-governed, human-in-the-loop "
        "AI research operating system."
    )


# ---------------------------------------------------------------------------
# Alibaba Cloud proof (v2) & Qwen config
# ---------------------------------------------------------------------------

class DatabaseProof(BaseModel):
    """Precise, non-overclaiming database representation.

    Distinguishes RDS *provisioning* from full production-data *migration*, and
    never asserts live connectivity from an endpoint that makes no external
    calls.
    """

    provider: str = Field(..., description="Target database engine descriptor")
    configured: bool = Field(..., description="Whether DATABASE_URL is set in this runtime")
    connected: Optional[bool] = Field(None, description="Live connectivity — null when not probed")
    role: str = Field(..., description="What the database is used for (or 'not asserted')")
    mirror_state: str = Field(
        "partial_selected_mirror",
        description="Mirror scope: 'partial_selected_mirror' means only selected evidence tables are mirrored, not the full production database",
    )
    production_data_migrated: bool = Field(False, description="Whether full prod data is asserted migrated")
    full_production_clone_verified: bool = Field(
        False,
        description="Whether a full production-database clone has been verified via row counts and API read-path checks",
    )
    note: str = Field(..., description="Precise disclosure separating provisioning from migration")


class AlibabaCloudProof(BaseModel):
    """Alibaba Cloud deployment proof v2 — public-safe, secret-free, honest host.

    Credentials are reported as booleans only. The compute *host* is reported
    honestly (``alibaba_hosted``): the same image runs on Railway and on an
    Alibaba Cloud ECS box, and this proof never claims Alibaba compute when it
    is not on it. The Qwen *AI provider* is always Alibaba Cloud DashScope.
    """

    schema_version: str = "alibaba-proof-2.0"
    project: str = "Pantheon Research"
    cloud_provider: str = "Alibaba Cloud"
    host_runtime: str = "local/unknown"
    alibaba_hosted: bool = False
    backend_runtime: str = "Dockerized FastAPI"
    reverse_proxy: str = "Nginx"
    frontend_source: str = "React + TypeScript + Vite (static build)"
    qwen_provider: str = "Alibaba Cloud DashScope (Model Studio)"
    qwen_base_url: str = "https://dashscope-intl.aliyuncs.com/compatible-mode/v1"
    qwen_model: str = "qwen-plus"
    qwen_configured: bool = False
    dashscope_api_key_configured: bool = False
    demo_mode: str = "offline"
    region: str = "ap-southeast-1"
    git_sha: str = "unknown"
    timestamp_utc: str = ""
    alibaba_services: dict = Field(
        default_factory=dict,
        description="Structured Alibaba Cloud service map: compute, AI, database (secret-free)",
    )
    proof_endpoints: dict = Field(default_factory=dict)
    database: DatabaseProof
    safe_claims: list[str] = Field(default_factory=list)
    non_claims: list[str] = Field(default_factory=list)
    judge_evidence: dict = Field(
        default_factory=dict,
        description="Quick-reference map for judges: proof code paths, live URLs, verification doc",
    )
    attestation: dict = Field(
        default_factory=dict,
        description="Explicit attestation: no external calls, no credential values returned, host detection source",
    )
    runtime_mode: dict = Field(
        default_factory=dict,
        description="Runtime context: public_repo_default vs live_alibaba_ecs, external call policy, live call location",
    )


class QwenConfig(BaseModel):
    """Qwen / DashScope configuration (no secrets)."""

    provider: str = "Alibaba Cloud DashScope (Model Studio)"
    base_url: str = "https://dashscope-intl.aliyuncs.com/compatible-mode/v1"
    model: str = "qwen-plus"
    integration_type: str = "OpenAI-compatible chat completions"
    prompt_version: str = ""
    output_schema_version: str = ""
    credential_configured: bool = False
    demo_mode: str = "offline"
