# Macro Risk Budget

A **pure, deterministic** macro risk-budget extractor: same input → same output,
no clock, no network, no secrets. It is a public-safe reimplementation of the
production contract; all thresholds, ladders and multipliers here are
**illustrative**, not the proprietary production values.

## Regime taxonomy (four-quadrant growth × inflation)

`REFLATION` (growth↑ inflation↓), `OVERHEAT` (growth↑ inflation↑),
`STAGFLATION` (growth↓ inflation↑), `DEFLATION` (growth↓ inflation↓).

## Output contract

```
version, score, regime, confirmed_regime, regime_confidence, coverage,
hard_stops_active, hard_stops_triggered, final_exposure, exposure_cap_pct,
anomaly_flags, as_of, freshness, hysteresis, degraded_reason
```

- **score** — illustrative 0–100 (growth-favorable up, inflation-hot down).
- **confirmed_regime** — hysteresis-smoothed regime (below).
- **coverage** — `OK | PARTIAL | DEGRADED` from data-quality summary.
- **hard_stops** — `HS1..HS6`; any active hard stop forces `exposure_cap_pct` to
  `0.0` and `final_exposure` to `NONE` (fail-closed).
- **final_exposure** — bucket `FULL | HIGH | MODERATE | LOW | MINIMAL | NONE`
  (or `UNKNOWN` when degraded).
- **freshness** — `FRESH | STALE | DEGRADED` from the snapshot source label.
- **degraded_reason** — populated only on the fail-closed path.

## Hysteresis / confirmed regime

The confirmed regime only flips after a new raw regime persists for
`OBSERVATIONS_REQUIRED = 3` consecutive observations **and** the growth/inflation
scores are outside a buffer band around the 0.5 boundary (avoids flip-flopping).
The `/api/macro/history` endpoint replays the bundled 17-point history so the
DEFLATION→REFLATION transition and its confirmation lag are visible.

## Fail-closed behavior

Any missing/malformed snapshot, or a hard-degraded freshness source, returns a
conservative degraded budget (`score 0`, empty regime, `exposure_cap_pct 0.0`,
`final_exposure UNKNOWN`, `anomaly_flags [macro_unavailable]`) rather than
raising or fabricating a value.

## Scenarios (`/api/macro/scenarios`)

1. `valid_full` — REFLATION, no hard stops → full exposure.
2. `hard_stop_stress` — STAGFLATION + hard stops → exposure forced to zero.
3. `stale_degraded` — hard-stale freshness → conservative degraded output.
4. `missing_malformed` — missing scores → fail-closed degraded output.

## APIs

```
GET /api/macro/risk-budget
GET /api/macro/history
GET /api/macro/scenarios
```

## Backend / data

`backend/app/macro_risk_budget.py`, `macro_sample_loader.py`.
Fixtures: `data/macro/current_snapshot.json`, `history.json`, `scenarios.json`.

## Not ported

Real hard-stop thresholds, score→exposure cutoffs, regime multipliers, TTL
values, scoring weights, and any FRED/vendor keys. No live FRED connection is
required.
