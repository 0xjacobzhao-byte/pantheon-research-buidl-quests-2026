# Research Ops / Validation Console

Reports each research module's **governance** state — readiness, validation
method, record kind, PIT policy, and public-performance eligibility — under a
hard honesty contract:

> **No alpha, return, or performance claim is made for modules without mature,
> eligible outcomes.**

Performance fields (`hit_rate`, `avg_return_pct`, `sharpe`, `max_drawdown_pct`)
are **always `null` with an explicit reason** in the public repo. No returns,
Sharpe ratios, hit rates, or sample counts are invented.

## Modules (14)

`btc, eth, macro, us-stock, cn-stock, hk-stock, sg-stock, commodity, fi, forex,
defi, narrative, guru-council, ta`.

## Vocabulary

- **readiness** — `ready | ready_for_internal_diagnostics | partial |
  signal_only | warming_up | blocked`.
- **record_kind** — `live | validation_only | reconstructed | signal_only |
  warming_up`.
- **pit_policy** — `PIT | MIXED | REVISED`.
- **outcome status** — `WIN | LOSS | FLAT | OPEN | INSUFFICIENT_DATA |
  UNSUPPORTED`.

## Eligibility discipline

Only `record_kind = live` modules (btc, eth) are `public_performance_eligible`.
Validation-only equities are explicitly **not** eligible (admin diagnostics
only). Reconstructed modules are surfaced separately and never summed into public
performance. The summary confirms `modules_with_public_performance = 0`.

## Fields per module

`module, display_name, readiness, validation_method, sample_count,
outcome_maturity, record_kind, pit_policy, public_performance_eligible,
limitations, next_action`.

## APIs

```
GET /api/research-ops/readiness
GET /api/research-ops/validation
GET /api/research-ops/outcomes
GET /api/research-ops/summary
```

## Backend / data

`backend/app/research_ops.py`, `research_validation.py`, `research_outcomes.py`.
Fixtures: `data/research_ops/{readiness,validation,outcomes}.json`.
