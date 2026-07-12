# Signal and Delivery Layer

Pantheon distributes research through two complementary mechanisms, kept
architecturally distinct because they optimize for different properties. Both
pass through a **human-review gate**, and neither executes a trade.

---

## Deterministic delivery

Scheduled research, alerts, and structured signals that carry provider and
data-quality states. This channel maximizes **reproducibility and
auditability**: the same inputs produce the same output, and every signal is
traceable to governed evidence.

- scheduled research runs;
- structured signals with `data_state`;
- alerts on state transitions;
- reproducible, audit-friendly output.

## LLM-assisted delivery

Research briefs, synthesis, contextual explanation, Q&A, and cross-model
comparison. This channel maximizes **breadth and contextual depth**: it explains
*why*, reconciles perspectives, and surfaces missing evidence.

- research briefs and synthesis;
- contextual explanation and Q&A;
- model comparison and disagreement summaries.

## Why both

Deterministic systems are the record of truth; LLM systems are the interpreter.
A deterministic signal without explanation is hard to act on; an LLM narrative
without a reproducible signal is hard to trust. Pantheon delivers both, clearly
labeled, so the reader always knows which is which.

---

## Delivery channels

| Channel | Purpose |
|---|---|
| Web dashboard & user feed | Primary cross-asset research surface |
| Research alerts | Notify on material state changes |
| Telegram distribution | Push research and signals to subscribers |
| LLM signal channels | Summaries + insights with model comparison |
| Human-review gate | Approval / triage before anything is delivered |

Channels are described at the level verified in the product; no distribution
volume, subscriber, or bot-count figures are claimed.

---

## The delivery boundary

> Signals and summaries are delivered. Nothing is auto-executed.

The signal layer ends at delivery and human review. Execution is a separate,
staged layer — see [`docs/roadmap.md`](roadmap.md). This separation is a core
Pantheon design principle: *signal is not a trade.*
