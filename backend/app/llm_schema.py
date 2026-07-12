"""Unified public-safe overlay schema for the five-model research cockpit.

The schema mirrors the production multi-provider overlay contract (factor
verdicts, evidence tiers, confidence, red flags, missing evidence) but carries
only sanitized, illustrative content — never raw proprietary model output.
"""

from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class LLMProvider(str, Enum):
    CLAUDE = "claude"
    CHATGPT = "chatgpt"
    GEMINI = "gemini"
    DEEPSEEK = "deepseek"
    QWEN = "qwen"


# Ordered, canonical provider list — exactly five.
PROVIDER_ORDER = [
    LLMProvider.CLAUDE,
    LLMProvider.CHATGPT,
    LLMProvider.GEMINI,
    LLMProvider.DEEPSEEK,
    LLMProvider.QWEN,
]


class LLMState(str, Enum):
    """Unified per-provider state vocabulary."""

    CACHED = "CACHED"
    OFFLINE = "OFFLINE"
    AVAILABLE = "AVAILABLE"
    BLOCKED_MISSING_CREDENTIAL = "BLOCKED_MISSING_CREDENTIAL"
    NOT_GENERATED = "NOT_GENERATED"
    SCHEMA_INVALID = "SCHEMA_INVALID"
    PROVIDER_ERROR = "PROVIDER_ERROR"
    UNAVAILABLE = "UNAVAILABLE"


# States that carry a usable, comparable assessment.
USABLE_STATES = {LLMState.CACHED, LLMState.AVAILABLE}


class FactorVerdict(str, Enum):
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"
    INSUFFICIENT_EVIDENCE = "insufficient_evidence"


class EvidenceTier(str, Enum):
    SOURCE_BACKED_STRONG = "SOURCE_BACKED_STRONG"
    SOURCE_BACKED_MODERATE = "SOURCE_BACKED_MODERATE"
    SOURCE_BACKED_BASIC = "SOURCE_BACKED_BASIC"
    SOURCE_LIMITED_BRIEF = "SOURCE_LIMITED_BRIEF"
    NO_USABLE_EVIDENCE = "NO_USABLE_EVIDENCE"


# The five comparable factors.
FACTOR_KEYS = [
    "business_quality",
    "moat",
    "pricing_power",
    "management_capital_allocation",
    "valuation_view",
]

WEAK_EVIDENCE_TIERS = {EvidenceTier.SOURCE_LIMITED_BRIEF, EvidenceTier.NO_USABLE_EVIDENCE}


class Factor(BaseModel):
    """A single factor verdict + short public-safe rationale."""

    verdict: FactorVerdict = FactorVerdict.INSUFFICIENT_EVIDENCE
    note: str = ""


class ModelOverlay(BaseModel):
    """One provider's overlay for one case (ticker)."""

    provider: LLMProvider
    model: str
    ticker: str
    market: str = "US"
    generated_at: str = ""
    data_state: LLMState
    evidence_hash: Optional[str] = None
    evidence_coverage: Optional[EvidenceTier] = None
    confidence: Optional[float] = Field(None, description="Model confidence 0–1 (None if not usable)")
    business_quality: Optional[Factor] = None
    moat: Optional[Factor] = None
    pricing_power: Optional[Factor] = None
    management_capital_allocation: Optional[Factor] = None
    valuation_view: Optional[Factor] = None
    red_flags: list[str] = Field(default_factory=list)
    missing_evidence: list[str] = Field(default_factory=list)
    risk_summary: str = ""
    tone: str = "neutral"
    human_review_required: bool = False
    source_refs: list[str] = Field(default_factory=list)
    error_message: Optional[str] = None

    def factor(self, key: str) -> Optional[Factor]:
        return getattr(self, key, None)

    def is_usable(self) -> bool:
        return self.data_state in USABLE_STATES and self.business_quality is not None
