"""Lineage traversal.

Given an evidence hash, walk the chain a judge needs to audit:

    Provider Record → Canonical Observation → Version History →
    Derived Snapshot → Evidence Pack Hash → LLM Overlay(s)
"""

from __future__ import annotations

import json
from typing import Any

from .models import LineageNode, LineageTrace
from .store import DataPlatformStore


def _loads(text: Any) -> Any:
    if not text:
        return {}
    if isinstance(text, (dict, list)):
        return text
    try:
        return json.loads(text)
    except (json.JSONDecodeError, TypeError):
        return {}


def trace_evidence(store: DataPlatformStore, evidence_hash: str) -> LineageTrace:
    """Build a top-down lineage trace anchored on an evidence hash."""
    nodes: list[LineageNode] = []

    # 1. Product snapshot(s) carrying this evidence hash (page-ready layer).
    products = [p for p in store.product_snapshots() if p.get("evidence_hash") == evidence_hash]

    # 2. Derived snapshot(s) carrying this evidence hash.
    derived = [d for d in store.derived_snapshots() if d.get("evidence_hash") == evidence_hash]
    # also pull derived referenced by product
    for p in products:
        dsid = p.get("derived_snapshot_id")
        if dsid:
            for d in store.derived_snapshots():
                if d["id"] == dsid and d not in derived:
                    derived.append(d)

    # 3. Consumed canonical observations -> their version history + provider records.
    consumed_ids: list[int] = []
    for d in derived:
        consumed_ids.extend(_loads(d.get("consumed_observation_ids_json")))
    consumed_ids = sorted(set(consumed_ids))

    all_provider_records = store._rows("SELECT * FROM external_provider_records ORDER BY id")

    for obs_id in consumed_ids:
        obs = store.observation(obs_id)
        if not obs:
            continue
        # Provider record(s): matched by instrument key (macro rows have a null
        # instrument, matched against provider records with a null ticker).
        obs_key = obs.get("instrument_id")
        matches = [
            r for r in all_provider_records
            if r.get("ticker") == obs_key or r.get("instrument_id") == obs_key
        ]
        for r in matches:
            nodes.append(LineageNode(
                layer="provider_record", entity="ExternalProviderRecord", id=r["id"],
                key=f"{r['provider']}:{r.get('ticker') or r.get('instrument_id') or r['market']}",
                detail={
                    "provider": r["provider"], "market": r["market"], "as_of": r["as_of"],
                    "content_hash": r["content_hash"], "dq_state": r["dq_state"],
                },
            ))
        nodes.append(LineageNode(
            layer="canonical_observation", entity="CanonicalObservation", id=obs["id"],
            key=f"{obs['domain']}:{obs['metric_id']}:{obs.get('instrument_id') or 'GLOBAL'}:{obs['as_of_date']}",
            detail={
                "value": obs["value"], "unit": obs["unit"], "quality_state": obs["quality_state"],
                "source": obs["source"], "revision_sequence": obs["revision_sequence"],
            },
        ))
        for v in store.observation_versions(obs["id"]):
            nodes.append(LineageNode(
                layer="observation_version", entity="CanonicalObservationVersion", id=v["id"],
                key=f"rev{v['revision_sequence']}:{v['source']}",
                detail={
                    "revision_sequence": v["revision_sequence"], "value": v["value"],
                    "source": v["source"], "quality_state": v["quality_state"],
                    "source_vintage": v["source_vintage"], "version_hash": v["version_hash"],
                    "vintage_at": v["vintage_at"],
                },
            ))

    for d in derived:
        nodes.append(LineageNode(
            layer="derived_snapshot", entity="DerivedSnapshot", id=d["id"],
            key=f"{d['snapshot_type']}:{d['as_of_date']}",
            detail={
                "snapshot_type": d["snapshot_type"], "evidence_hash": d.get("evidence_hash"),
                "payload": _loads(d.get("payload_json")), "ingest_run_id": d.get("ingest_run_id"),
            },
        ))

    for p in products:
        nodes.append(LineageNode(
            layer="product_snapshot", entity="ProductSnapshot", id=p["id"],
            key=f"{p['product']}:{p['as_of_date']}",
            detail={"product": p["product"], "version": p["version"], "evidence_hash": p.get("evidence_hash")},
        ))

    nodes.append(LineageNode(
        layer="evidence_pack_hash", entity="EvidenceHash", id=None, key=evidence_hash,
        detail={"evidence_hash": evidence_hash},
    ))

    llm = store.llm_consumers(evidence_hash)
    for c in llm:
        nodes.append(LineageNode(
            layer="llm_overlay", entity="LLMOverlay", id=c["id"],
            key=f"{c['provider']}:{c.get('ticker')}",
            detail={"provider": c["provider"], "model": c.get("model"),
                    "overlay_ref": c.get("overlay_ref"), "prompt_version": c.get("prompt_version")},
        ))

    found = bool(derived or products or llm)
    return LineageTrace(
        evidence_hash=evidence_hash,
        found=found,
        nodes=nodes,
        llm_consumers=llm,
        note=(
            "Full lineage: provider record → canonical observation → append-only "
            "version history → derived snapshot → evidence hash → LLM overlay. "
            "LLM overlays are display-only consumers; they never feed the "
            "deterministic signal core."
            if found else f"No lineage found for evidence hash {evidence_hash}."
        ),
    )
