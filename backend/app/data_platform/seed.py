"""Seed the in-memory data platform from bundled JSON fixtures."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

from .store import DataPlatformStore

DATA_DIR = Path(__file__).resolve().parents[3] / "data" / "lineage"


def _load(name: str) -> list:
    path = DATA_DIR / name
    if not path.exists():
        return []
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def build_seeded_store() -> DataPlatformStore:
    store = DataPlatformStore()

    for run in _load("ingest_runs.json"):
        store.insert_ingest_run(run)
    for health in _load("provider_health.json"):
        store.upsert_provider_health(health)
    for rec in _load("provider_records.json"):
        store.upsert_provider_record(rec)

    # Canonical observations: each fixture may carry a "revisions" list that is
    # replayed in order to exercise the append-only vintage history.
    for obs in _load("canonical_observations.json"):
        revisions = obs.pop("revisions", [])
        base = dict(obs)
        store.upsert_observation(base)
        for rev in revisions:
            merged = dict(base)
            merged.update(rev)
            store.upsert_observation(merged)

    # Some fixtures explicitly declare pre-built version rows; if present and the
    # observation table already versioned them, they are skipped as idempotent.
    for ds in _load("derived_snapshots.json"):
        store.insert_derived_snapshot(ds)
    for ps in _load("product_snapshots.json"):
        store.insert_product_snapshot(ps)
    for c in _load("llm_consumers.json"):
        store.insert_llm_consumer(c)

    return store


_store: Optional[DataPlatformStore] = None


def get_store() -> DataPlatformStore:
    global _store
    if _store is None:
        _store = build_seeded_store()
    return _store


def reset_store() -> DataPlatformStore:
    global _store
    _store = build_seeded_store()
    return _store
