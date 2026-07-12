"""Evidence provenance schema — versioned, hashable, and public-safe.

This module is the single source of truth for the evidence-pack contract:
the schema version, the provenance models, and the sanitized source-label map.
It intentionally contains no private provider names, keys, URLs, or dataset
identifiers — only public-safe labels a judge can read.
"""

from __future__ import annotations

# Bump when the evidence pack shape or hashing rule changes.
EVIDENCE_SCHEMA_VERSION = "evidence-1.0"

# Re-export the provenance models so callers can import them from one place.
from ..models import (  # noqa: E402  (re-export)
    EquityEvidence,
    EvidencePack,
    EvidenceProvenance,
    EvidenceSource,
)

# Which evidence fields belong to which provenance group. In the public demo all
# groups resolve to a bundled sample; in production these map to distinct
# governed providers (kept private).
EVIDENCE_GROUPS: dict[str, list[str]] = {
    "identity": ["ticker", "company_name", "exchange", "sector", "industry", "summary"],
    "valuation": ["pe_ratio", "pb_ratio", "market_cap_usd"],
    "quality": ["roic_pct", "gross_margin_pct", "net_margin_pct", "debt_to_equity"],
    "growth_cashflow": ["revenue_growth_yoy_pct", "fcf_ttm_usd", "dividend_yield_pct"],
}

# Public-safe origin label for every group in this demo.
PUBLIC_DEMO_ORIGIN = "bundled_sample"

__all__ = [
    "EVIDENCE_SCHEMA_VERSION",
    "EVIDENCE_GROUPS",
    "PUBLIC_DEMO_ORIGIN",
    "EquityEvidence",
    "EvidencePack",
    "EvidenceProvenance",
    "EvidenceSource",
]
