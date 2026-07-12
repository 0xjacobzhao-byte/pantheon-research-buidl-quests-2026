# Project Story — Pantheon Research

## Why Pantheon Research was created

Serious investment research is fragmented. A single view on one asset requires
pulling structured market data, fundamentals, macro context, technical signals,
and cross-asset read-through from a dozen disconnected tools — then reconciling
them by hand. Institutions solve this with large teams and expensive terminals.
Individuals and small shops are left stitching spreadsheets together.

Pantheon Research was created to compress that fragmented workflow into one
**AI-native investment research operating system for public markets**: structured
evidence in, disciplined frameworks and multi-model interpretation on top, and a
human making the final call.

## The problem it solves

* **Fragmentation** — data, frameworks, and narrative live in separate places.
* **Unaccountable AI** — single-model "AI research" blurs live results with
  cached samples, hides failures, and offers no provenance.
* **No discipline layer** — raw LLM output is not a research process.

Pantheon answers each: one platform for cross-asset evidence; honest
`data_state` labels and fail-closed handling; a deterministic framework layer
separated from LLM interpretation; and a human-review gate.

## The four-layer architecture

```
Strategy ──▶ Information ──▶ Signal ──▶ Trading
```

* **Strategy** — research frameworks and investment hypotheses.
* **Information** — normalized data, evidence packs, APIs, dashboards.
* **Signal** — deterministic signals plus LLM interpretation of structured
  evidence.
* **Trading** — a future/staged, human-gated layer. Not autonomous execution.

## The founder's background

Pantheon Research is built and operated by **Jacob Zhao**, a solo founder
combining an investment background with hands-on AI and software engineering.
The whole stack — research methodology, backend, frontend, cloud deployment,
data operations, and go-to-market — is carried by one person.

## The OPC workflow

Being a one-person company is only possible because AI multiplies the founder's
capacity:

* AI coding tools accelerate engineering and refactoring;
* a **five-model LLM research layer** (Claude, ChatGPT, Gemini, DeepSeek, and
  Qwen) interprets structured evidence at breadth — one founder now gets the
  equivalent of a multi-analyst research desk;
* multiple models are compared to surface disagreement and missing evidence;
* the platform has been deployed and validated across **three cloud
  footprints** — Vercel + Railway (core production), Google Cloud, and
  Alibaba Cloud — demonstrating that one person can also own multi-cloud
  operations, not just a single deployment target;
* documentation and operations are AI-assisted.

Crucially, this is **AI-assisted operation**, not an autonomous-agent product.
There is no agent orchestration runtime and no autonomous trading. The founder
retains investment judgment and accountability.

## Why AI-assisted development matters

The gap between "a solo builder" and "an institutional-grade research platform"
used to be a team of engineers and analysts. AI-assisted development collapses
that gap: one disciplined operator can now design, build, deploy, and run a
cross-asset research system — which is precisely the Super Individual / OPC
thesis this submission demonstrates.

## Current stage and future direction

* **Now:** a live web product, multi-asset research modules, a completed
  five-model LLM research layer, Research-Ops tooling, core production on
  Vercel + Railway, and completed additional deployments on Google Cloud
  (Cloud Run + Gemini) and Alibaba Cloud (ECS + DashScope/Qwen), each with a
  secret-free proof endpoint.
* **In progress:** backtest / forward-validation, PWA / mobile, WeChat Mini
  Program, Telegram distribution, and commercialization.
* **Future (not claimed as done):** broader coverage, richer validation, and —
  only after rigorous validation — a controlled execution layer. The full,
  gated staging is in [`docs/roadmap.md`](roadmap.md).

No revenue, users, AUM, or investment-performance figures are claimed. The
commercial architecture behind this stage is in
[`docs/commercial_model.md`](commercial_model.md).
