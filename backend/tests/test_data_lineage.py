"""Data platform tests: idempotency, revision append, hashing, lineage."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest

from app.data_platform.seed import build_seeded_store
from app.data_platform.lineage import trace_evidence
from app.data_platform.store import DataPlatformStore

NVDA_HASH = "sha256:b1b1a99dc8d5e218d93487c23166a804c3b69684e3781c6fa10f5117efdce4c9"


def test_seed_builds_entities():
    s = build_seeded_store()
    assert len(s.ingest_runs()) >= 1
    assert len(s.provider_health()) >= 1
    assert len(s.observations()) >= 2


def test_idempotent_observation_insert():
    s = DataPlatformStore()
    row = {
        "domain": "macro", "metric_id": "vix", "instrument_id": None,
        "as_of_date": "2026-07-11", "value": 14.5, "unit": "index",
        "source": "ref", "ingested_at": "2026-07-12T00:00:00Z",
        "quality_state": "PROVIDER_REPORTED",
    }
    oid1, ins1 = s.upsert_observation(dict(row))
    oid2, ins2 = s.upsert_observation(dict(row))
    assert ins1 is True and ins2 is False
    assert oid1 == oid2
    # No spurious version rows for an identical re-ingest.
    assert len(s.observation_versions(oid1)) == 1


def test_revision_appends_version_and_no_silent_overwrite():
    s = DataPlatformStore()
    base = {
        "domain": "equity", "metric_id": "rev", "instrument_id": "NVDA",
        "as_of_date": "2026-Q1", "value": 78.5, "unit": "USD", "source": "vendor",
        "ingested_at": "2026-05-01T00:00:00Z", "quality_state": "PROVIDER_REPORTED",
    }
    oid, _ = s.upsert_observation(dict(base))
    revised = dict(base)
    revised.update(value=79.0, source="filing", quality_state="MANUAL_VERIFIED",
                   ingested_at="2026-07-12T00:00:00Z")
    s.upsert_observation(revised)
    versions = s.observation_versions(oid)
    assert len(versions) == 2
    assert versions[0]["revision_sequence"] == 1 and versions[0]["value"] == 78.5
    assert versions[1]["revision_sequence"] == 2 and versions[1]["value"] == 79.0
    # CURRENT row is the revised value (append-only history preserves the original).
    assert s.observation(oid)["value"] == 79.0
    assert s.observation(oid)["quality_state"] == "MANUAL_VERIFIED"


def test_content_hash_stable():
    s = DataPlatformStore()
    row = {"provider": "p", "provider_family": "f", "market": "US", "ticker": "NVDA",
           "instrument_id": "NVDA", "source_url": "u", "as_of": "2026-Q1", "currency": "USD",
           "normalized_payload": {"x": 1}, "dq_state": "OK", "coverage_state": "FULL"}
    h1 = s.content_hash_for_provider_record(dict(row))
    h2 = s.content_hash_for_provider_record(dict(row))
    assert h1 == h2 and h1.startswith("sha256:")


def test_invalid_quality_state_fails_closed():
    s = DataPlatformStore()
    with pytest.raises(ValueError):
        s.upsert_observation({
            "domain": "macro", "metric_id": "x", "instrument_id": None,
            "as_of_date": "2026-07-11", "value": 1.0, "unit": "u", "source": "s",
            "ingested_at": "t", "quality_state": "NOT_A_STATE",
        })


def test_lineage_traversal_end_to_end():
    s = build_seeded_store()
    trace = trace_evidence(s, NVDA_HASH)
    assert trace.found is True
    layers = [n.layer for n in trace.nodes]
    for expected in ("provider_record", "canonical_observation", "observation_version",
                     "derived_snapshot", "evidence_pack_hash", "llm_overlay"):
        assert expected in layers, expected
    # All five LLM providers consume the evidence hash.
    assert len(trace.llm_consumers) == 5


def test_unknown_evidence_hash_not_found():
    s = build_seeded_store()
    trace = trace_evidence(s, "sha256:deadbeef")
    assert trace.found is False
