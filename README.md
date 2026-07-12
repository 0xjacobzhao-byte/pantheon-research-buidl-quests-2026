# Pantheon Research

> **Institutional-grade cross-asset research command center that transforms complex market noise into structured investment intelligence.**

Pantheon Research combines quantitative frameworks, risk-regime models, structured market data, deterministic signal engines, backtest analytics, narrative research and multi-model AI overlays across Global Macro, Equities, Crypto, DeFi and FICC.

> **AI should not replace the investor. AI should compound the investor's discipline.**

**BUIDL_QUESTS 2026 · OPC Hackathon Submission**

[![CI](https://github.com/0xjacobzhao-byte/pantheon-research-buidl-quests-2026/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/0xjacobzhao-byte/pantheon-research-buidl-quests-2026/actions/workflows/ci.yml)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Live Product](https://img.shields.io/badge/Live%20Product-pantheon--research.com-1f9d55)](https://pantheon-research.com)

---

## Product Links

| | |
|---|---|
| 🌐 Live Product | https://pantheon-research.com |
| 💻 Public GitHub Repository | https://github.com/0xjacobzhao-byte/pantheon-research-buidl-quests-2026 |
| 📋 Judge Evidence | [`docs/judge_evidence.md`](docs/judge_evidence.md) |
| 👤 Founder / X | https://x.com/0xjacobzhao |

---

## Project Introduction

Pantheon Research is an institutional-grade cross-asset research command center that transforms complex, fast-moving market noise into structured investment intelligence. It is built for sophisticated investors, research analysts, allocators, and crypto-native market participants who need disciplined decision support, not another disconnected data feed.

The platform combines quantitative frameworks, risk-regime models, structured market data, technical signals, valuation logic, narrative scanning, backtests, data-quality tooling, deterministic signal engines, and AI-powered research overlays with multi-model comparison — across Global Macro, US/China/Hong Kong/Singapore Equities, Bitcoin, Ethereum, DeFi, Technical Analysis, Commodities, Fixed Income, Currencies, narrative research, and Research Ops.

Pantheon Research is currently a decision-intelligence and research platform. Final investment decisions remain human-controlled, and the product does not currently perform autonomous trading.

---

## Architecture

> **Note:** the approved architecture diagram (`docs/assets/pantheon_research_high_level_architecture.png`) has not yet been added to this repository — see [`docs/assets/README.md`](docs/assets/README.md#approved-architecture-image-pending) for the pending drop-in path. No substitute or regenerated diagram is used in its place.

<!--
<p align="center">
  <img
    src="docs/assets/pantheon_research_high_level_architecture.png"
    alt="Pantheon Research high-level architecture showing the multi-asset research platform, five-model LLM layer, signal and trading layers, and Vercel Railway, Google Cloud, and Alibaba Cloud deployments"
    width="100%"
  />
</p>
-->

Pantheon Research combines a governed data platform, deterministic research engines, five-model LLM overlays, cross-asset information and signal layers, and completed deployments across Vercel + Railway, Google Cloud and Alibaba Cloud.

---

## The Problem Pantheon Solves

Financial information is fragmented, noisy, and fast-moving. Investors must monitor macro regimes, equities, crypto, DeFi, rates, commodities, currencies, narratives, and risk signals across a dozen disconnected tools. The problem is not a lack of information — it is a lack of structured decision intelligence. Pantheon Research turns market data, research evidence, and AI interpretation into a more disciplined and explainable research workflow.

---

## Product Coverage

| Macro & Rates | Equities | Digital Assets | Cross-Cutting |
|---|---|---|---|
| Global Macro | US Equities | Bitcoin | Technical Analysis |
| Fixed Income | China Equities | Ethereum | Narrative Research |
| Currencies (FX) | Hong Kong Equities | DeFi | Research Ops |
| Commodities | Singapore Equities | | |

---

## How Pantheon Uses AI

Pantheon combines two complementary approaches.

**Deterministic framework layer** — data normalization, framework rules, scores, market regimes, hard stops, signal candidates, backtests, data-quality states, and evidence provenance produce consistent, explainable research outputs.

**Multi-model LLM research-overlay layer** — Pantheon first builds structured evidence packs instead of asking an LLM for an unsupported investment opinion. Five LLM research modules have been developed — **Claude, ChatGPT, Gemini, DeepSeek, and Qwen** — each analyzing evidence using a consistent research schema covering business quality, moat, valuation, red flags, confidence, missing evidence, risk summary, and disagreement. Pantheon compares outputs across models and surfaces agreement, disagreement, confidence gaps, missing evidence, and human-review requirements.

The public repository contains a runnable, sanitized Qwen + DeepSeek comparison example — supporting evidence of the approach, not the full identity of Pantheon Research.

---

## Four-Layer Architecture and Current Progress

Pantheon Research is a live, web-based cross-asset research platform with
mobile / PWA support, Research Ops and data-quality tooling, and membership /
payment foundations for commercialization. A WeChat Mini Program and Telegram
signal / research-distribution workflows are in progress.

```text
Strategy → Information → Signal → Trading
```

1. **Strategy** — versioned investment frameworks across Macro, Equities, Crypto, DeFi, Technical Analysis, Fixed Income, FX, Commodities, Narrative Trading, and Prediction Markets. *Largely completed.*
2. **Information** — a database-first architecture (PostgreSQL, canonical observations, derived snapshots, evidence artifacts, data-quality labels) fed by APIs, filings, web data, on-chain data, social data, and provider integrations, following a fail-closed data-governance model where missing or stale data is labeled rather than silently guessed. *Largely completed.*
3. **Signal** — deterministic scoring engines, market regimes, hard stops, and signal candidates combined with LLM research overlays, disagreement detection, missing-evidence surfacing, human-review flags, and Telegram distribution/alerts. These are research and decision-intelligence outputs, not automatic trade execution. *In progress, actively developed.*
4. **Trading** — manual and human-controlled today. The roadmap may progress through paper trading, broker integration, approval-based execution, constraint-bound automation, and human override, contingent on backtesting, forward validation, and risk controls. *Staged roadmap, not currently live.*

---

## Why Pantheon Fits the OPC Model

Pantheon Research is built and submitted by **Jacob Zhao** as a one-person company. Jacob is an AI and crypto researcher, product builder, and investor with experience across public markets, digital assets, investment research, financial-market analysis, AI-native research infrastructure, product strategy, and hands-on software development — handling product design, investment-research methodology, system architecture, backend and frontend implementation, data operations, LLM evaluation, cloud deployment, business-model development, and GTM planning.

The platform was built using an AI-assisted, vibecoding workflow across tools and models including Claude Code, Codex, Trae, Qoder, OpenClaw, ChatGPT, Claude, Gemini, Qwen, and DeepSeek. The OPC relevance is not an autonomous-agent product — it is that AI allows one founder to perform work that traditionally requires a larger research, engineering, data, and product team, while retaining full product judgment and investment responsibility.

---

## Multi-Cloud Deployment

| Environment | Role | Main components |
|---|---|---|
| Vercel + Railway | Core production | Frontend, FastAPI backend, PostgreSQL |
| Google Cloud | Completed deployment | Cloud Run, Artifact Registry, Secret Manager, Cloud Logging, Gemini |
| Alibaba Cloud | Completed deployment | ECS/Nginx, Dockerized FastAPI, RDS selected mirror, DashScope/Qwen |

These deployments demonstrate completed multi-cloud deployment and provider-integration work. Automatic multi-cloud failover, active-active replication, and identical full production database clones are not claimed.

---

## Business Model

1. **Subscription Fees** — monthly and annual access to dashboards, strategy frameworks, AI research overlays, model comparisons, signal summaries, and premium market intelligence.
2. **Skills Marketplace** — Macro, US Equity, Bitcoin, Ethereum, DeFi Yield, Technical Analysis, Narrative Trading, and FX/Commodities skills.
3. **Paid Equity Evaluation and Market Data APIs** — company evaluations, evidence packs, model comparisons, valuation views, risk summaries, data-quality-labeled research artifacts, and cleaned/normalized market data.
4. **B2B / Institutional Research Licensing** — family offices, advisors, crypto funds, and small investment teams, via dashboard licensing, custom workflows, white-label reporting, and premium support.
5. **Trading Profit / Proprietary Strategy Upside** — long-term only, only after backtests, forward validation, and a real track record; not a current revenue claim.

The near-term sustainability plan is recurring software and research revenue first.

---

## Public Repository Scope

This repository is a sanitized, judge-runnable public slice of the broader private Pantheon Research production system. It includes representative evidence-pack, LLM-overlay, comparison, data-quality, Docker, and testing components without production secrets, proprietary strategy code, databases, or broker credentials.

---

## Three-Minute Judge Path

1. Open the live product — https://pantheon-research.com
2. Review the approved architecture (once added — see the note above) and [`docs/architecture.md`](docs/architecture.md)
3. Inspect the evidence-pack and comparison code — [`backend/app/evidence_pack.py`](backend/app/evidence_pack.py) · [`backend/app/comparison.py`](backend/app/comparison.py)
4. Run Docker and the smoke test (below)
5. Read [`docs/judge_evidence.md`](docs/judge_evidence.md)

---

## Quick Start and Verification

```bash
git clone https://github.com/0xjacobzhao-byte/pantheon-research-buidl-quests-2026
cd pantheon-research-buidl-quests-2026
docker compose up --build          # frontend :5173 · backend :8000
./scripts/judge_smoke.sh           # end-to-end smoke test (offline, no secrets)
```

```bash
cd backend && python -m pytest             # 84 backend tests
cd frontend && npm test -- --run           # 9 frontend tests
cd frontend && npm run build               # production build (tsc + vite)
```

<details>
<summary><b>Manual setup (no Docker)</b></summary>

**Backend** (Python 3.11–3.12):
```bash
cd backend && python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

**Frontend** (Node.js 18+):
```bash
cd frontend && npm install && npm run dev
```

| Service | URL |
|---------|-----|
| Frontend | http://localhost:5173 |
| Backend API | http://localhost:8000 |
| API Docs (Swagger) | http://localhost:8000/docs |

</details>

---

## Author and License

**Jacob Zhao** — [0xjacobzhao-byte](https://github.com/0xjacobzhao-byte) · [x.com/0xjacobzhao](https://x.com/0xjacobzhao)

**License:** Apache-2.0 — see [LICENSE](LICENSE).
