"""Deterministic provenance + audit hashing.

The audit hash is a SHA-256 over a canonical (sorted-key, separator-normalized)
JSON projection of the immutable intent body + provenance stamp. It deliberately
excludes mutable lifecycle fields (state, approvals, fills) so the *origin* of an
intent is committed once and can be re-verified for tamper detection.
"""

from __future__ import annotations

import hashlib
import json
from typing import Any

from .models import IntentProvenance, PaperIntent

# Fields of the intent body that are committed into the provenance hash.
_HASHED_INTENT_FIELDS = (
    "intent_id",
    "ticker",
    "asset_class",
    "sector",
    "side",
    "quantity",
    "limit_price",
    "notional_usd",
    "created_at",
)

# Provenance fields committed into the hash (audit_hash itself is excluded).
_HASHED_PROVENANCE_FIELDS = (
    "source_module",
    "source_verdict_ref",
    "validation_maturity",
    "macro_risk_budget_ref",
    "data_freshness_state",
    "kill_switch_snapshot",
    "risk_policy_snapshot",
    "actor_identity",
    "actor_type",
    "created_by_surface",
)

REQUIRED_PROVENANCE_FIELDS = (
    "source_module",
    "validation_maturity",
    "data_freshness_state",
    "kill_switch_snapshot",
    "risk_policy_snapshot",
    "actor_identity",
    "actor_type",
    "created_by_surface",
)


def _canonical(obj: dict[str, Any]) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), default=str)


def compute_audit_hash(intent: PaperIntent) -> str:
    """Compute the canonical audit hash for an intent + its provenance stamp."""
    body = {f: getattr(intent, f, None) for f in _HASHED_INTENT_FIELDS}
    prov = {f: getattr(intent.provenance, f, None) for f in _HASHED_PROVENANCE_FIELDS}
    # Enums -> their value for stable hashing.
    for d in (body, prov):
        for k, v in list(d.items()):
            if hasattr(v, "value"):
                d[k] = v.value
    payload = {"intent": body, "provenance": prov}
    digest = hashlib.sha256(_canonical(payload).encode("utf-8")).hexdigest()
    return f"sha256:{digest}"


def stamp_provenance(intent: PaperIntent) -> PaperIntent:
    """Attach the computed audit hash to the intent's provenance (in place)."""
    intent.provenance.audit_hash = compute_audit_hash(intent)
    return intent


def provenance_completeness(prov: IntentProvenance) -> tuple[bool, list[str]]:
    """Return (complete, missing_fields) for a provenance stamp."""
    missing: list[str] = []
    for field in REQUIRED_PROVENANCE_FIELDS:
        val = getattr(prov, field, None)
        if val is None or (isinstance(val, str) and not val.strip()):
            missing.append(field)
    return (not missing), missing


def verify_audit_hash(intent: PaperIntent) -> bool:
    """True iff the stored audit hash matches a fresh recomputation."""
    stored = intent.provenance.audit_hash
    if not stored:
        return False
    return stored == compute_audit_hash(intent)
