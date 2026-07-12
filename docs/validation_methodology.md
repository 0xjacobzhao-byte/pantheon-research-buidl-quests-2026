# Validation Methodology

## The core stance

**An LLM qualitative overlay is a tracked research signal — not an alpha oracle.**

Pantheon Research does not claim that a Qwen or DeepSeek assessment predicts
returns. Each overlay is treated as a *governed artifact* that feeds a
human-review workflow, and any performance statement must wait for out-of-sample
forward validation.

## What is tracked

Every overlay is stored with the metadata needed to reproduce and audit it:

- `provider` + `model` — which model produced it.
- `prompt_version` + `output_schema_version` — the exact contract it ran under.
- `evidence_hash` — a `sha256` over the canonical evidence pack (see
  [`backend/app/evidence_pack.py`](../backend/app/evidence_pack.py)), so a
  signal is bound to the exact inputs it saw.
- `status` — an explicit fail-closed state, never a hollow success.

## How agreement feeds review (not trading)

1. Two **independent** models assess the same evidence pack.
2. The comparison engine computes agreement, tone, and per-field divergence —
   it does not assume agreement.
3. **Low agreement** or a **major divergence** routes the case to a human-review
   queue. See `human_review_required` / `human_review_reason` in
   [`backend/app/comparison.py`](../backend/app/comparison.py).
4. When one side fails closed, the comparison is marked `NOT_COMPARABLE`
   (`data_state = PARTIAL`/`BLOCKED`) and **no agreement score is fabricated**.

The NVDA sample in this repo is a live demonstration: the two models diverge on
pricing power and valuation risk, agreement lands `LOW`, and the human-review
gate engages — see
[`data/redacted_traces/nvda_comparison_redacted.json`](../data/redacted_traces/nvda_comparison_redacted.json).

## Forward validation (prospective, no-lookahead)

Before any performance claim:

- Signals are **frozen at decision time** with their evidence hash and versions.
- They are scored only against **subsequently realized** data (no lookahead).
- Sample sizes must clear a significance gate before results are reported.

## Explicit non-claims

- No backtested or live alpha is claimed by this repository.
- The illustrative summary in
  [`data/redacted_traces/sample_validation_summary.json`](../data/redacted_traces/sample_validation_summary.json)
  contains **no production outcome data** and is not statistically significant.
- The production forward-validation ledger (cohorts, matured signals, realized
  outcomes) lives in the private repo and is intentionally not published here.

## Where the code lives

- Methodology stub + illustrative summary: [`backend/app/validation_stub.py`](../backend/app/validation_stub.py)
  (served at `GET /api/validation`).
- Comparison / review gate: [`backend/app/comparison.py`](../backend/app/comparison.py).
