# Module Snapshots — Full System Scope

Pantheon Research is a **multi-asset research operating system**, not a single
Qwen demo. This public repo ships a **module snapshot grid** so a judge can see
the whole system's scope and — crucially — its *honest governance state* for each
module, without any proprietary engine, live feed, or secret being exposed.

- **Endpoint:** `GET /api/modules`
- **Backend:** [`backend/app/sample_modules.py`](../backend/app/sample_modules.py)
- **Frontend:** [`frontend/src/components/ModuleSnapshotGrid.tsx`](../frontend/src/components/ModuleSnapshotGrid.tsx)
- **Data:** [`data/redacted_traces/module_snapshots_redacted.json`](../data/redacted_traces/module_snapshots_redacted.json)

## The grid

| Module | Group | data_state | validation_state | Production surface |
|--------|-------|------------|------------------|--------------------|
| Macro Regime | Macro | `CONTEXT_ONLY` | `CONTEXT_ONLY` | `/macro` |
| Market Pulse / TA | Signal | `CONTEXT_ONLY` | `NOT_VALIDATED` | `/ta` |
| Commodity | FICC | `CONTEXT_ONLY` | `FORWARD_VALIDATION_PROSPECTIVE` | `/commodity` |
| Fixed Income | FICC | `CONTEXT_ONLY` | `FORWARD_VALIDATION_PENDING` | `/fi` |
| FX | FICC | `CONTEXT_ONLY` | `SIGNAL_ONLY` | `/fx` |
| Ticker Profile | Equity | `OFFLINE_SAMPLE` | `EVIDENCE_HASHED` | `/equity/ticker-profile` |
| Qwen vs DeepSeek | Signal | *live-computed* | `HUMAN_REVIEW_GATED` | overlay comparison |
| Data Quality | Research-Ops | `LIVE_IN_PROCESS` | `GOVERNANCE` | Research-Ops admin plane |

## Each card is honest about what it is

Every card carries six governance fields:

| Field | Meaning |
|-------|---------|
| `data_state` | Is this live, a bundled sample, or context-only? |
| `freshness` | As-of / how current the underlying data is |
| `validation_state` | Where it sits in the forward-validation lifecycle |
| `role` | What the module does + its production surface |
| `what_not_to_infer` | The explicit caveat — what a reader must **not** conclude |
| `sample_endpoint` | Where to see it in this repo |

## What is real vs illustrative

- **Live in-process (real state):** `qwen_vs_deepseek` and `data_quality` are
  computed at request time from the bundled samples — the grid shows their true
  `data_state`, agreement outcome, and coverage.
- **Context-only (illustrative):** `macro`, `market_pulse_ta`, `commodity`,
  `fixed_income`, `fx` are static, clearly-labelled snapshots that demonstrate
  the *shape* of each production module. They are **not** live nowcasts and carry
  no fair-value bands or trading signals.

## Why this matters for judging

It shows the Qwen overlay is one signal inside a **governed, multi-asset research
system** with an explicit data-state / validation taxonomy — the opposite of an
LLM wrapper. The honesty (context-only labels, "what not to infer", no fabricated
freshness) is itself the production-grade signal. The full engines behind each
module (market-data ingestion, scoring, forward-validation) stay private; see
[`production_architecture_mapping.md`](production_architecture_mapping.md) and
[`safe_claims.md`](safe_claims.md).
