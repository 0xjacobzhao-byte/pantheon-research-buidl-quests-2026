# Research-Ops Mini (Data Quality)

Pantheon Research runs a private **Research-Ops** governance plane — coverage
diagnostics, freshness tracking, provider routing, forward-validation, and an
admin control surface. This repo ships a **deliberately small, public-safe
slice** of it so the demo reads as a governed research system, not an LLM
wrapper. No admin actions, secrets, or private datasets are exposed.

## Endpoint

```
GET /api/data-quality
```

Backed by [`backend/app/data_quality.py`](../backend/app/data_quality.py) and
rendered by [`DataQualityPanel.tsx`](../frontend/src/components/DataQualityPanel.tsx).

## What it reports

| Field | Meaning |
|-------|---------|
| `mode` | offline (bundled samples) vs live |
| `providers.qwen_configured` / `deepseek_configured` | credential presence (boolean only) |
| `providers.*_model` | active model id per provider |
| `alibaba_proof_reachable` | whether the deployment proof is served |
| `sample_evidence_coverage` | tickers, evidence packs present, healthy comparisons |
| `overlay_statuses[]` | per-ticker: qwen/deepseek status, `data_state`, agreement, review flag |
| `fail_closed_states` | the full enum of fail-closed provider statuses |

## Governance properties on display

- **Fail-closed accounting** — a `PARTIAL`/`BLOCKED` comparison is surfaced as
  such and flagged for human review; it is never counted as a healthy success.
- **Provenance** — every comparison carries the evidence pack's `sha256` hash.
- **No hollow success** — a missing sample yields `QWEN_NOT_GENERATED`, not an
  empty assessment.
- **Secret-free** — configuration is reported as booleans and model ids only.

## What is intentionally NOT here

The full admin plane (mutation endpoints, backfill/refresh jobs, provider
routing config, cost controls, the production coverage matrix) stays in the
private repo. This slice is read-only and computed from bundled samples.
