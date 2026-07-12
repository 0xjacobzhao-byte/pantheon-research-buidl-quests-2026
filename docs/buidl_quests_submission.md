# BUIDL_QUESTS 2026 — OpenArena Submission Copy

Copy-ready text matching the OpenArena submission form, preserving the full
substance of the submitted hackathon answers. Fields requiring private
information use `[PLACEHOLDER]` markers — fill these in yourself; do not commit
private contact details or keys.

---

**Project Name**
Pantheon Research

**Project Introduction**
Pantheon Research is an institutional-grade cross-asset research command
center that transforms complex market noise into structured investment
intelligence. The product serves sophisticated investors, analysts, allocators,
and crypto-native market participants, covering Global Macro, US Equities,
China Equities, Hong Kong Equities, Singapore Equities, Bitcoin, Ethereum,
DeFi, Technical Analysis, Commodities, Fixed Income, Currencies, narrative
research, and Research Ops. It combines quantitative frameworks, risk-regime
models, structured market data, technical signals, valuation logic, narrative
scanning, backtests, data-quality tooling, deterministic signal engines, and
AI-powered research overlays with multi-model comparison. The product is
currently a decision-intelligence and research platform — final investment
decisions remain human-controlled, and it does not currently perform
autonomous trading.

**Core Team Background**
Pantheon Research is built and submitted by **Jacob Zhao**
([@0xjacobzhao](https://x.com/0xjacobzhao)) as a one-person company. Jacob is
an AI and crypto researcher, product builder, and investor with experience
across public markets, digital assets, investment research, financial-market
analysis, AI-native research infrastructure, product strategy, and hands-on
software development. Jacob handled product design, investment-research
methodology, system architecture, backend implementation, frontend
integration, data operations, LLM evaluation, cloud deployment, business-model
development, and GTM planning. The platform was built using an AI-assisted /
vibecoding workflow involving tools and models such as Claude Code, Codex,
Trae, Qoder, OpenClaw, ChatGPT, Claude, Gemini, Qwen, and DeepSeek. This is not
an autonomous-agent product claim — the OPC relevance is that AI allows one
founder to perform work that traditionally requires a larger research,
engineering, data, and product team.

**Project Innovation Related to AI**
Pantheon combines two complementary approaches. The **deterministic framework
approach** uses structured market data, macro indicators, technical signals,
valuation logic, risk-regime models, and explicit investment frameworks —
including data normalization, framework rules, scores, market regimes, hard
stops, signal candidates, backtests, data-quality states, and evidence
provenance — to produce consistent research outputs. The **multi-model LLM
research-overlay approach** first builds structured evidence packs instead of
asking an LLM for an unsupported investment opinion. Five LLM research modules
have been developed — Claude, ChatGPT, Gemini, DeepSeek, and Qwen — analyzing
evidence using a consistent research schema covering business quality, moat,
valuation, red flags, confidence, missing evidence, risk summary, and
disagreement. Pantheon compares outputs from different models and surfaces
agreement, disagreement, confidence gaps, missing evidence, and human-review
requirements. The public repository contains a runnable sanitized Qwen +
DeepSeek comparison example; that public example is supporting evidence, not
the full identity of Pantheon Research.

**Pain Point Solved**
Financial information is fragmented, noisy, and fast-moving. Investors must
monitor macro regimes, equities, crypto, DeFi, rates, commodities, currencies,
narratives, and risk signals across disconnected tools. The problem is not a
lack of information — it is a lack of structured decision intelligence.
Pantheon Research turns market data, research evidence, and AI interpretation
into a more disciplined and explainable research workflow.

**Current Development Progress**
*Product:* a live web-based cross-asset research platform; mobile / PWA
support; a WeChat Mini Program in progress; Research Ops and data-quality
tooling; Telegram signal and research-distribution workflows; membership and
payment foundations; commercialization and GTM preparation.
*Four-layer architecture:* Strategy Layer (largely completed) — versioned
investment frameworks across Macro, Equities, Crypto, DeFi, Technical
Analysis, Fixed Income, FX, Commodities, Narrative Trading, and Prediction
Markets. Information Layer (largely completed) — a database-first architecture
(PostgreSQL, canonical observations, derived snapshots, evidence artifacts,
data-quality labels) fed by APIs, filings, web data, on-chain data, social
data, and provider integrations, with a fail-closed data-governance model.
Signal Layer (in progress, actively developed) — deterministic scoring
engines, market regimes, hard stops, signal candidates, LLM research overlays,
disagreement detection, missing-evidence surfacing, human-review flags, and
Telegram distribution/alerts — research and decision-intelligence outputs, not
automatic trade execution. Trading Layer (staged roadmap) — manual and
human-controlled today; the roadmap may progress through paper trading, broker
integration, approval-based execution, constraint-bound automation, and human
override, contingent on backtesting, forward validation, and risk controls; not
currently live.
*Deployment:* core production on Vercel (frontend) + Railway (FastAPI backend
+ PostgreSQL); completed Google Cloud deployment work (Cloud Run, Artifact
Registry, Secret Manager, Cloud Logging, Gemini integration); completed
Alibaba Cloud deployment work (ECS/Nginx, Dockerized FastAPI, Alibaba RDS
PostgreSQL selected mirror, DashScope/Qwen integration). These are completed
multi-cloud deployment and validation work — not automatic multi-cloud
failover, active-active replication, identical full production database
clones, or seamless automatic traffic switching.

**Expected Revenue Sources**
1. *Subscription Fees* — monthly and annual access to dashboards, strategy
   frameworks, AI research overlays, model comparisons, signal summaries, and
   premium market intelligence.
2. *Skills Marketplace* — Macro, US Equity, Bitcoin, Ethereum, DeFi Yield,
   Technical Analysis, Narrative Trading, and FX/Commodities skills.
3. *Paid Equity Evaluation and Market Data APIs* — company evaluations,
   evidence packs, model comparisons, valuation views, risk summaries,
   data-quality-labeled research artifacts, and cleaned/normalized market data.
4. *B2B / Institutional Research Licensing* — family offices, advisors, crypto
   funds, small investment teams, via dashboard licensing, custom workflows,
   white-label reporting, and premium support.
5. *Trading Profit / Proprietary Strategy Upside* — long-term only, only after
   backtests, forward validation, and a real track record; not a current
   revenue claim.

The near-term sustainability plan is recurring software and research revenue
first. No revenue, user, or AUM figures are claimed today.

**Official Website**
https://pantheon-research.com

**GitHub Repository**
https://github.com/0xjacobzhao-byte/pantheon-research-buidl-quests-2026

**X (Twitter)**
https://x.com/0xjacobzhao

**Telegram**
`[PLACEHOLDER — add only if you have a verified handle]`

---

## Product integrity notes (for the submitter)

* Product name is **Pantheon Research** (not an "Agent" product).
* No autonomous research agents, agent orchestration runtime, or autonomous
  trade execution are claimed — the product is AI-assisted, human-in-the-loop.
* Five production LLM providers (Claude, ChatGPT, Gemini, DeepSeek, Qwen) vs.
  the public repo's runnable Qwen + DeepSeek slice are kept explicitly
  distinct — do not imply all five are independently runnable in the public repo.
* Multi-cloud deployment (Vercel+Railway, Google Cloud, Alibaba Cloud) is
  described as cloud portability and provider integration — not automatic
  failover or identical full-database replication.
* This public repository is a sanitized slice; the private production repository
  remains closed.

## Private form fields — fill in locally (do NOT commit real values)

* Contact email: `[PLACEHOLDER — your submission email]`
* Public wallet address (if required): `[PLACEHOLDER — your PUBLIC address, never a private key]`
* Demo video URL: `[PLACEHOLDER — optional; see docs/demo_script.md]`
* Pitch deck URL: `[PLACEHOLDER — optional]`

> OpenArena signing happens locally in your own wallet. Never paste a private key
> or seed phrase into any file in this repository.
