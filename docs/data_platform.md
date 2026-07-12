# Information Layer — Data as Research Infrastructure

Pantheon is **database-first**: research reads from governed, point-in-time
observations, not from ad-hoc API calls made at request time. Data is treated as
research infrastructure, with provenance, freshness, and quality attached to
every field.

---

## Data flow

```text
Providers / APIs / Filings / Web / On-chain / Social
        ↓
Ingestion + Provider Routing        (scheduler, provider health, fallback)
        ↓
Validation + Normalization          (schema, units, sanity checks)
        ↓
Canonical Observations              (single normalized record per data point)
        ↓
Derived Snapshots + Product Snapshots   (pre-computed, frontline-ready payloads)
        ↓
Evidence Artifacts                  (structured, hashable evidence packs)
        ↓
Research Engines + LLM Context      (deterministic engines + overlay context)
        ↓
Dashboard / Alerts / APIs           (product surfaces)
```

---

## Core concepts

| Concept | What it is | Why it matters |
|---|---|---|
| Canonical observations | The single normalized record of each governed data point | One source of truth; reproducible research |
| Provider routing & fallback | Selection and failover across data providers | Resilience without silent gaps |
| Ingestion runs | Recorded, auditable ingestion jobs | Traceability of what was loaded, when |
| Derived snapshots | Computed views over canonical data | Consistent inputs for engines |
| Product snapshots | Frontline-ready research payloads | Fast, uniform product surfaces |
| Evidence artifacts | Structured, hashable evidence packs | A model output can be verified against a specific pack |
| Point-in-time discipline | Data as it was known at a moment | No lookahead in research or backtests |
| Freshness / TTL | Age and expiry on every field | Stale data is labeled, not trusted blindly |
| Quality labels & `data_state` | Explicit quality/state per field and module | Fail-closed governance |
| Provider health | Live view of provider configuration & coverage | Operational trust in the surface |
| Data-gap audits & Research Ops | Systematic detection of missing coverage | Gaps are surfaced, never hidden |

---

## Fail-closed governance

Pantheon never manufactures a value it does not have. Missing, stale, or degraded
data is **labeled** and propagated as an explicit state; downstream research and
LLM overlays receive that state and can decline to conclude. This is the data
counterpart of the strategy principle that a framework must be able to refuse to
conclude.

---

## What the public slice implements

The open-source repository demonstrates this discipline end-to-end, with no
secrets:

| Capability | Public implementation |
|---|---|
| Evidence pack + `sha256` provenance | [`backend/app/evidence_pack.py`](../backend/app/evidence_pack.py) |
| Evidence / comparison schemas | [`backend/app/models.py`](../backend/app/models.py) · [`backend/app/schemas/`](../backend/app/schemas/) |
| Research-Ops / data-quality snapshot | [`backend/app/data_quality.py`](../backend/app/data_quality.py) |
| Module-level `data_state` grid (Macro/TA/FICC/Equity) | [`backend/app/sample_modules.py`](../backend/app/sample_modules.py) |
| Provider health (secret-free) | [`backend/app/provider_health.py`](../backend/app/provider_health.py) |
| Validation methodology / timeline | [`backend/app/validation_stub.py`](../backend/app/validation_stub.py) · [`backend/app/validation_timeline.py`](../backend/app/validation_timeline.py) |

Full production data infrastructure — providers, credentials, schemas, and the
production database — remains private. Public samples are bundled and labeled;
see [`docs/data_safety.md`](data_safety.md).
