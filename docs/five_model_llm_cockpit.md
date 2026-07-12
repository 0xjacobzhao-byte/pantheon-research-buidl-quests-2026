# Five-Model LLM Research Cockpit

A public-safe, **offline / cached** cockpit that compares five independent LLM
providers over one shared, hash-committed evidence pack — surfacing agreement,
disagreement, red flags, and evidence gaps **without ever declaring a winner**.

## Providers

Exactly five, public model family names only, offline-cached by default (no
credential required, **no live paid LLM call is ever made**):

| Provider | Model (public) |
|---|---|
| Claude | `claude-3-5-sonnet` |
| ChatGPT | `gpt-4o` |
| Gemini | `gemini-2.5-pro` |
| DeepSeek | `deepseek-chat` |
| Qwen | `qwen-plus` |

## State vocabulary

`CACHED`, `OFFLINE`, `AVAILABLE`, `BLOCKED_MISSING_CREDENTIAL`, `NOT_GENERATED`,
`SCHEMA_INVALID`, `PROVIDER_ERROR`, `UNAVAILABLE`.

A provider with no public-safe cached artifact for a case reports an **explicit
state** (e.g. `NOT_GENERATED`) — a completed analysis is never fabricated. The
bundled BTC case deliberately ships Gemini as `NOT_GENERATED` to demonstrate
this honestly.

## Unified overlay schema

`provider, model, ticker, market, generated_at, data_state, evidence_hash,
evidence_coverage, confidence, business_quality, moat, pricing_power,
management_capital_allocation, valuation_view, red_flags, missing_evidence,
risk_summary, tone, human_review_required, source_refs`.

Each factor carries a verdict — `positive | neutral | negative |
insufficient_evidence` — plus a short public-safe rationale.

## Comparison logic (deterministic)

- **Agreement matrix** — per factor, verdicts across usable providers; a factor
  is comparable when ≥2 providers scored it; `agreement_score = agreements /
  comparisons` (or `null` when no factor is comparable — never coerced).
- **Disagreement matrix** — the divergent factors with each provider's verdict.
- **Confidence spread** — `max − min` model confidence across providers.
- **Red flags** — shared themes vs. provider-unique risks (theme-clustered so
  differently-worded mentions of the same risk collapse). A unique risk ⇒
  `material_risk_disagreement`.
- **Missing evidence** — per-provider and shared gaps.
- **Evidence-coverage spread** — tier rank spread + weak-evidence providers.
- **Human review** — required when any of: `insufficient_comparable_providers`,
  `no_comparable_factors`, `low_agreement` (<0.7), `high_confidence_dispersion`
  (>0.34), `weak_evidence`, `material_risk_disagreement`.

**No winner is ever declared.** The output is disciplined disagreement
surfacing, not model ranking.

## Cases

`NVDA`, `MA`, `BTC`. NVDA/MA evidence hashes match `/api/evidence/{ticker}` and
the data-lineage explorer, so a judge can trace a provider record all the way to
the five overlays.

## APIs

```
GET /api/llm/providers
GET /api/llm/cases
GET /api/llm/case/{case_id}
GET /api/llm/comparison/{case_id}
GET /api/llm/agreement/{case_id}
```

The pre-existing Qwen and DeepSeek endpoints (`/api/overlay/qwen/{ticker}`,
`/api/overlay/deepseek/{ticker}`, `/api/comparison/{ticker}`) continue to work.

## Backend

`backend/app/llm_registry.py`, `llm_schema.py`, `llm_cached_store.py`,
`llm_five_model_comparison.py`, `llm_provider_status.py`, `llm_cockpit.py`.
Fixtures: `data/llm/cases.json` and `data/llm/{NVDA,MA,BTC}/{provider}.json`.

## Safety

No proprietary prompts, no raw private model responses, no API keys. Overlay
content is sanitized and illustrative. Cached/offline by default.
