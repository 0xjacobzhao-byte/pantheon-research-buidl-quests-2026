"""Public-safe entity models + quality vocabulary for the canonical data platform.

A sanitized reimplementation of the production data platform's provenance layer.
The vocabulary and hashing method mirror production; all bundled values are
illustrative. No real database URLs, credentials, provider payloads, or
customer/operator identities are present.
"""

from __future__ import annotations

from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Quality vocabulary
# ---------------------------------------------------------------------------

class QualityState(str, Enum):
    UNKNOWN = "UNKNOWN"
    PROVIDER_REPORTED = "PROVIDER_REPORTED"
    MANUAL_VERIFIED = "MANUAL_VERIFIED"
    SYSTEM_DERIVED = "SYSTEM_DERIVED"
    RECONSTRUCTED_REVISED = "RECONSTRUCTED_REVISED"
    ESTIMATED = "ESTIMATED"


CANONICAL_QUALITY_STATES = {q.value for q in QualityState}


# ---------------------------------------------------------------------------
# Entities
# ---------------------------------------------------------------------------

class IngestRun(BaseModel):
    id: int
    job_name: str
    started_at: str
    finished_at: Optional[str] = None
    status: str = Field(..., description="running | success | partial | failed")
    metrics_ingested: int = 0
    series_fetched: int = 0
    duration_ms: Optional[int] = None
    errors: list[str] = Field(default_factory=list)


class ProviderHealth(BaseModel):
    provider: str
    last_success_at: Optional[str] = None
    last_failure_at: Optional[str] = None
    last_error_msg: Optional[str] = None
    consecutive_failures: int = 0
    daily_calls_used: int = 0
    daily_calls_limit: Optional[int] = None
    avg_latency_ms: Optional[int] = None
    status: str = Field("healthy", description="healthy | degraded | rate_limited | down")


class ExternalProviderRecord(BaseModel):
    id: int
    provider: str
    provider_family: str
    market: str
    ticker: Optional[str] = None
    instrument_id: Optional[str] = None
    source_url: str
    retrieved_at: str
    as_of: str
    currency: Optional[str] = None
    normalized_payload: dict[str, Any] = Field(default_factory=dict)
    dq_state: str = "OK"
    coverage_state: str = "FULL"
    content_hash: Optional[str] = None


class CanonicalObservation(BaseModel):
    id: int
    domain: str
    metric_id: str
    instrument_id: Optional[str] = None
    as_of_date: str
    value: float
    unit: str
    source: str
    ingested_at: str
    quality_state: QualityState = QualityState.UNKNOWN
    verified_by: Optional[str] = None
    verified_at: Optional[str] = None
    revision_sequence: int = 1
    content_hash: Optional[str] = None


class CanonicalObservationVersion(BaseModel):
    id: int
    canonical_observation_id: int
    domain: str
    metric_id: str
    instrument_id: Optional[str] = None
    as_of_date: str
    value: float
    unit: str
    source: str
    ingested_at: str
    vintage_at: str
    revision_sequence: int
    quality_state: QualityState = QualityState.UNKNOWN
    source_vintage: Optional[str] = Field(None, description="live_capture | reconstructed_revised")
    version_hash: str


class DerivedSnapshot(BaseModel):
    id: int
    snapshot_type: str
    as_of_date: str
    payload: dict[str, Any] = Field(default_factory=dict)
    created_at: str
    ingest_run_id: Optional[int] = None
    evidence_hash: Optional[str] = None
    consumed_observation_ids: list[int] = Field(default_factory=list)


class ProductSnapshot(BaseModel):
    id: int
    product: str
    version: str
    as_of_date: str
    payload: dict[str, Any] = Field(default_factory=dict)
    created_at: str
    ingest_run_id: Optional[int] = None
    evidence_hash: Optional[str] = None
    derived_snapshot_id: Optional[int] = None


# ---------------------------------------------------------------------------
# Lineage view
# ---------------------------------------------------------------------------

class LineageNode(BaseModel):
    layer: str
    entity: str
    id: Optional[int] = None
    key: str
    detail: dict[str, Any] = Field(default_factory=dict)


class LineageTrace(BaseModel):
    evidence_hash: str
    found: bool
    nodes: list[LineageNode] = Field(default_factory=list)
    llm_consumers: list[dict[str, Any]] = Field(default_factory=list)
    note: str = ""
