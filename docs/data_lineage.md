# Canonical Data Platform + Vintage Provenance

A public-safe, **SQLite-backed** (stdlib `sqlite3`, in-memory, seeded from
bundled JSON) reimplementation of the production data platform's provenance
layer: idempotent ingest, content hashing, append-only vintage history, and
end-to-end lineage traversal.

## Entities

`IngestRun`, `ProviderHealth`, `ExternalProviderRecord`, `CanonicalObservation`,
`CanonicalObservationVersion`, `DerivedSnapshot`, `ProductSnapshot` (+ an
`llm_consumers` link table).

## Quality vocabulary

`UNKNOWN`, `PROVIDER_REPORTED`, `MANUAL_VERIFIED`, `SYSTEM_DERIVED`,
`RECONSTRUCTED_REVISED`, `ESTIMATED`. Invalid states are rejected on write
(fail-closed); a routine system re-write never silently downgrades a
`MANUAL_VERIFIED` row.

## Provenance primitives

- **Idempotent ingest** — provider records are keyed on a `content_hash`
  (SHA-256 over canonical, wall-clock-excluded material); an identical re-ingest
  updates fetch metadata in place and creates no duplicate.
- **Append-only vintage history** — when a provider revises a value, the CURRENT
  `canonical_observations` row is updated and a new immutable
  `canonical_observation_versions` row is appended with an incremented
  `revision_sequence`. The originally-observed value is never destroyed.
- **as_of vs ingested_at** — `as_of_date` is the business date a value is valid
  for (point-in-time); `ingested_at` is the wall-clock write/revision time.

## Lineage a judge can trace

```
Provider Record
  → Canonical Observation
  → Observation Version History
  → Derived Snapshot
  → Evidence Pack Hash
  → LLM Overlay
```

The bundled NVDA chain uses the real evidence hash
`sha256:b1b1a99d…` (matches `/api/evidence/NVDA`): a vendor revenue record
(78.5B, `PROVIDER_REPORTED`) is revised by a filing (79.0B, `MANUAL_VERIFIED`),
both preserved in the version history, feeding a derived evidence pack whose hash
is consumed by all five LLM overlays.

## APIs

```
GET /api/data-platform/ingest-runs
GET /api/data-platform/provider-health
GET /api/data-platform/observations
GET /api/data-platform/observation/{id}
GET /api/data-platform/versions/{observation_id}
GET /api/data-platform/lineage/{evidence_hash}
```

## Backend / data

`backend/app/data_platform/{models,store,lineage,seed}.py`.
Fixtures: `data/lineage/*.json`.

## Not ported

Real database URLs, credentials, admin tokens, real customer/operator
identities, real provider payloads, internal source URLs, or proprietary vendor
data. Vocabulary, hashing method, and clearly-illustrative values only.
