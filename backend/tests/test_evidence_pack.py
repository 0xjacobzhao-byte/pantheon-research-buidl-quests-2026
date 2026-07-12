"""Tests for the provenance-committed evidence pack."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.evidence_pack import (
    build_evidence_pack,
    canonical_evidence_json,
    compute_evidence_hash,
)
from app.schemas.evidence import EVIDENCE_SCHEMA_VERSION
from app.sample_loader import load_evidence


def test_hash_is_deterministic():
    ev = load_evidence("NVDA")
    assert compute_evidence_hash(ev) == compute_evidence_hash(ev)


def test_hash_prefixed_and_changes_with_content():
    ev = load_evidence("NVDA")
    h1 = compute_evidence_hash(ev)
    assert h1.startswith("sha256:")
    ev2 = ev.model_copy(update={"pe_ratio": (ev.pe_ratio or 0) + 1.0})
    assert compute_evidence_hash(ev2) != h1


def test_canonical_json_is_sorted():
    ev = load_evidence("MA")
    blob = canonical_evidence_json(ev)
    # Sorted keys → company_name appears before ticker in the serialized form.
    assert blob.index('"company_name"') < blob.index('"ticker"')


def test_pack_has_schema_version_and_sources():
    pack = build_evidence_pack(load_evidence("MA"))
    assert pack.provenance.evidence_schema_version == EVIDENCE_SCHEMA_VERSION
    assert pack.provenance.evidence_hash.startswith("sha256:")
    assert len(pack.provenance.sources) >= 1
    for src in pack.provenance.sources:
        assert src.origin == "bundled_sample"


def test_pack_contains_no_secrets():
    blob = json.dumps(build_evidence_pack(load_evidence("NVDA")).model_dump())
    for needle in ("api_key", "sk-", "postgresql://", "password", "secret"):
        assert needle not in blob.lower()


def test_pack_round_trips_evidence():
    ev = load_evidence("NVDA")
    pack = build_evidence_pack(ev)
    assert pack.evidence.ticker == "NVDA"
    assert pack.evidence.company_name == ev.company_name
