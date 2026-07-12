# BTC Three-Layer Decision Stack

A public-safe, offline reconstruction of the BTC decision stack: three
independent layers, each with its own as-of timestamp and misuse guardrail,
combined with the macro risk budget into one **research posture** — never a live
order.

## Layers

- **L1 — Bottom Model** (long-cycle accumulation anchor). `state`
  (`NONE/WEAK/MODERATE/STRONG/EXTREME/DATA_INSUFFICIENT`), `coverage_ratio`,
  `confidence`, `rating_capped`, `primary_signal`, `source_timestamp`. Raises
  long-term accumulation willingness only; never authorizes same-day entry.
- **L2 — Guardian / Hunter / Architect** (mid-cycle direction under a macro
  gate). Guardian is the macro gatekeeper (`GREEN/YELLOW/RED`, `long_gate`,
  `short_gate`); Hunter is direction (`hunter_state/score`); Architect is sizing
  (`risk_multiplier`, `architect_state/score`). Plus `macro_score`, `vol_scalar`,
  `regime`, `final_signal_score`, `final_signal_direction/conviction`,
  `missing_fields`. A closed long gate (macro RED) zeroes a bullish signal.
- **L3 — Risk Radar** (tactical risk gate). `state` (`GREEN/AMBER/RED/
  DEGRADED_AMBER`), `risk_label_raw`, `risk_score`, `confidence`, `mode`,
  `high_alert_mode`, `degraded_mode`, `posture_72h`, `triggers_fired_72h`,
  `metric_triggers`, `conditions_fired`. Modulates pace/leverage only; never
  flips direction.

## Conflict resolution → posture

Deterministic precedence (public-safe, structural — not a proprietary formula):

1. Degraded freshness anywhere (L1 `DATA_INSUFFICIENT`, L2 `missing_fields`, L3
   `degraded_mode`) → **RESEARCH_ONLY**.
2. Macro hard stop OR Guardian RED (long gate closed) → **NO_TRADE**.
3. Directional L2 signal, scaled down by L3: RED/high-alert → **RISK_THROTTLE**;
   AMBER/GREEN → **SLOW_SCALE** (staged, never a live order).
4. No dominant signal → **WAIT**; truly no signal → **NO_TRADE**.

Outcomes: `NO_TRADE, WAIT, SLOW_SCALE, RISK_THROTTLE, RESEARCH_ONLY`. Five
bundled conflict examples (L1-strong/L3-red, L1-weak/L2-positive, macro
hard-stop, missing-L2-input, high-conviction/degraded-freshness) each resolve to
their documented expected outcome.

## History

`/api/btc/history` serves 209 weekly rows (~4 years) with per-layer state and a
per-row quality label (`reconstructed` vs `native_retained`). Missing data stays
missing; timestamps are preserved.

## APIs

```
GET /api/btc/stack
GET /api/btc/history
GET /api/btc/conflicts
GET /api/btc/current-posture
```

## Backend / data

`backend/app/btc_stack.py`, `btc_history.py`, `btc_conflict_resolution.py`.
Fixtures: `data/btc/{current,history_weekly,conflict_examples}.json`.

## Not ported

Proprietary indicator thresholds, rating cutoffs, gate/multiplier tables, regime
blend weights, and confidence-penalty magnitudes. Vocabulary and structural
logic only; all numbers are illustrative. No direct live order instruction is
ever emitted.
