"""Build a provenance-committed evidence pack from raw equity evidence.

The evidence hash lets a judge (or a downstream store) verify that a given
comparison was produced against a specific, unmodified evidence pack — the same
integrity discipline the private production system uses, reduced to a
self-contained, secret-free form.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from typing import Optional

from .models import EquityEvidence, EvidencePack, EvidenceProvenance, EvidenceSource
from .schemas.evidence import (
    EVIDENCE_GROUPS,
    EVIDENCE_SCHEMA_VERSION,
    PUBLIC_DEMO_ORIGIN,
)


def canonical_evidence_json(evidence: EquityEvidence) -> str:
    """Deterministic JSON for hashing — sorted keys, no insignificant whitespace."""
    return json.dumps(
        evidence.model_dump(),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    )


def compute_evidence_hash(evidence: EquityEvidence) -> str:
    """Return ``sha256:<hex>`` over the canonical evidence JSON."""
    digest = hashlib.sha256(canonical_evidence_json(evidence).encode("utf-8")).hexdigest()
    return f"sha256:{digest}"


def _build_sources(as_of: str) -> list[EvidenceSource]:
    """Emit one sanitized provenance row per evidence group."""
    labels = {
        "identity": "Company identity & business description",
        "valuation": "Valuation multiples",
        "quality": "Returns, margins & leverage",
        "growth_cashflow": "Growth, free cash flow & yield",
    }
    return [
        EvidenceSource(
            group=group,
            label=labels.get(group, group),
            origin=PUBLIC_DEMO_ORIGIN,
            as_of=as_of,
        )
        for group in EVIDENCE_GROUPS
    ]


def build_evidence_pack(
    evidence: EquityEvidence, as_of: Optional[str] = None
) -> EvidencePack:
    """Wrap raw evidence in a provenance envelope with a content hash."""
    now = datetime.now(timezone.utc).isoformat()
    as_of = as_of or now[:10]
    provenance = EvidenceProvenance(
        evidence_schema_version=EVIDENCE_SCHEMA_VERSION,
        evidence_hash=compute_evidence_hash(evidence),
        generated_at_utc=now,
        sources=_build_sources(as_of),
    )
    return EvidencePack(evidence=evidence, provenance=provenance)
