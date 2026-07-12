# BUIDL_QUESTS 2026 — OpenArena Submission Copy

Copy-ready text matching the OpenArena submission form. Fields requiring private
information use `[PLACEHOLDER]` markers — fill these in yourself; do not commit
private contact details or keys.

---

**Project Name**
Pantheon Research

**Project Introduction**
Pantheon Research is an AI-native, institutional-grade cross-asset investment
research command center for public markets — built for sophisticated investors,
research analysts, allocators, and crypto-native market participants who need
structured decision intelligence, not another data feed. It combines normalized
market data, institutional-style investment frameworks, deterministic signal
engines, backtest analytics, data-quality operations, and a five-model LLM
research layer (Claude, ChatGPT, Gemini, DeepSeek, and Qwen) across a
four-layer architecture — Strategy → Information → Signal → Trading. LLMs
interpret governed structured evidence rather than raw prompts, multiple models
are compared side-by-side to surface disagreement and missing evidence, and a
human retains final judgment at every step. It is built and operated by a
single founder.

**Core Team Background**
Solo founder — **Jacob Zhao** ([@0xjacobzhao](https://x.com/0xjacobzhao)) —
combining an investment background with AI and full-stack engineering. One
person owns research methodology, backend and frontend engineering, multi-cloud
deployment, data operations, model evaluation, and go-to-market, using
AI-assisted development to reach institutional breadth without a team. This is
the OPC / Super Individual thesis in practice: AI-multiplied founder execution,
not autonomous company control — the founder retains product judgment and
investment responsibility throughout.

**Project Innovation Related to AI**
Two deliberately separated layers: a **deterministic framework layer**
(normalized evidence, versioned scoring, signal logic, backtests, data-quality
labels, content-hash audit trails) and a **five-model LLM research-overlay
layer** (Claude, ChatGPT, Gemini, DeepSeek, and Qwen in production; a runnable
Qwen + DeepSeek slice in this public repository). Multiple models analyze the
*same* governed evidence pack, outputs are compared, and disagreements and
missing evidence are surfaced rather than smoothed over. Honest `data_state`
semantics and fail-closed provider handling mean the system never fabricates a
result — a missing key or bad model output yields an explicit blocked state,
never a hollow success.

**Pain Point Solved**
Investment research is fragmented across a dozen disconnected tools, and
single-model AI research is unaccountable — it blurs live output with cached
samples and hides failures. The issue is not a lack of information; it is a
lack of structured decision intelligence. Pantheon unifies cross-asset
evidence, adds a disciplined deterministic layer, compares multiple models, and
keeps a human in the loop — turning scattered data and raw LLM output into an
auditable research process a single operator can run.

**Current Development Progress**
Live web product (pantheon-research.com); the four-layer architecture across
Macro, US/CN/HK/SG Equities, Bitcoin, Ethereum, DeFi, Technical Analysis, Fixed
Income, Currencies, Commodities, and Research Ops; a completed five-model LLM
research layer; Research-Ops / data-quality tooling; core production on Vercel
+ Railway, with completed additional deployments on Google Cloud (Cloud Run +
Gemini) and Alibaba Cloud (ECS + DashScope/Qwen, each with a secret-free
deployment-proof endpoint); ongoing backtest and forward-validation work; PWA,
WeChat Mini Program, and Telegram distribution in progress. Roadmap items are
not claimed as complete.

**Expected Revenue Sources**
Subscription plans for individual investors; premium research tiers; paid
research / evaluation APIs; B2B / institutional licensing; reusable investment
"Skills"; a controlled execution layer only after rigorous validation. No
revenue, user, or AUM figures are claimed today — this is a staged business
model, not a current result.

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
