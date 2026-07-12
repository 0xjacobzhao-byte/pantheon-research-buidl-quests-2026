# Architecture

## Production High-Level Architecture

This document is the **textual source of truth** for the approved architecture
diagram, `docs/assets/pantheon_research_high_level_architecture.png`, shown at
the top of the [README](../README.md#architecture).

<p align="center">
  <img
    src="assets/pantheon_research_high_level_architecture.png"
    alt="Pantheon Research high-level architecture showing the multi-asset research platform, five-model LLM layer, signal and trading layers, and Vercel Railway, Google Cloud, and Alibaba Cloud deployments"
    width="100%"
  />
</p>

The diagram is organized into seven layers plus a deployment column:

1. **External data sources** — macro/rates (FRED, ALFRED, GSEC, PBOC), equities
   (Longbridge, TuShare, Yahoo Finance), crypto/DeFi (Binance, CoinGecko,
   DeFiLlama, CoinMarketCap), social/alt data (BigQuant, StockTwits, X, Reddit),
   and positioning/market structure (CFTC, tick data).
2. **Data platform** — ingestion scheduler, provider health, validation /
   normalization, a PostgreSQL store (canonical observations, product snapshots,
   provider scores, ingest runs, derived snapshots, evidence artifacts),
   TTL/freshness checks, and data-quality labeling.
3. **Research engines** — Macro, Equity, Crypto, FICC, Technical Analysis,
   Narrative, Backtest/Validation, and Capital Flow Intelligence.
4. **Deterministic + LLM layer** — a deterministic engine (value/risk models,
   factor regressions, portfolio signals, event models, hard signals) and a
   five-model LLM research overlay (Source Pack Builder → Prompt Builder → Schema
   Validator → Overlay Comparison) across Claude, ChatGPT, Gemini, DeepSeek, and
   Qwen, producing qualitative overlays, confidence, red flags, missing evidence,
   disagreement detection, and human-review requirements — not trade execution.
5. **Information layer** — the Pantheon cross-asset dashboard (Overview, Global
   Macro, US/CN/HK/SG Equity, BTC, ETH, DeFi, Technical Analysis, Fixed Income,
   FX, Commodity, Research Ops).
6. **Signal layer** — Telegram bot, user feed, research alerts, LLM signal
   channels, and a human-review gate; signals and summaries are delivered, not
   traded.
7. **Trading layer** — manual execution today, then a staged roadmap through
   paper trading, broker integration, and constraint-bound execution with human
   override. No live autonomous trading.

**Deployment stacks** — current production on Vercel (frontend) + Railway
(FastAPI backend + PostgreSQL); a completed Google Cloud deployment (Cloud Run,
Artifact Registry, Secret Manager, Cloud Logging, Gemini); and a completed
Alibaba Cloud deployment (ECS/Nginx, Dockerized FastAPI, RDS PostgreSQL selected
mirror, DashScope/Qwen).

**Non-claims:** the three deployment stacks are independently verified, not an
active-active failover cluster; only the core Vercel + Railway production stack
and the Alibaba selected-evidence RDS mirror are described as connected to
runtime data — see [Multi-Cloud Deployment](../README.md#multi-cloud-deployment)
in the README and [`docs/alibaba_deployment_parity.md`](alibaba_deployment_parity.md)
for the precise breakdown.

---

## Public Repository Implementation

This repository is a sanitized, runnable slice of the production system above,
centered on the **Qwen + DeepSeek dual-LLM equity qualitative overlay**: a
system that takes quantitative equity evidence and produces structured
qualitative analysis from two independent LLM providers, then renders them
side-by-side for comparison with agreement scoring, tone classification, and
divergence detection.

## System Diagram

```
┌─────────────────────────────────────────────────────────┐
│                     Frontend (React)                     │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────────┐ │
│  │ Ticker      │  │ Evidence     │  │ Side-by-Side    │ │
│  │ Selector    │  │ Panel        │  │ Comparison Grid │ │
│  └─────────────┘  └──────────────┘  └────────────────┘ │
│         │                                    │           │
│         └────────────┬───────────────────────┘           │
│                      │ /api/*                            │
└──────────────────────┼──────────────────────────────────┘
                       │
┌──────────────────────┼──────────────────────────────────┐
│                Backend (FastAPI)                          │
│                      │                                   │
│  ┌───────────────────▼──────────────────────┐            │
│  │           main.py (FastAPI)               │            │
│  │  GET  /                                    │            │
│  │  GET  /health                              │            │
│  │  GET  /api/project                         │            │
│  │  GET  /api/evidence/{ticker}              │            │
│  │  GET  /api/overlay/qwen/{ticker}          │            │
│  │  GET  /api/overlay/deepseek/{ticker}     │            │
│  │  GET  /api/comparison/{ticker}           │            │
│  │  GET  /api/demo-flow                      │            │
│  │  GET  /api/alibaba/proof                   │            │
│  │  GET  /api/alibaba/qwen-config            │            │
│  └───┬───────┬──────────┬───────────────────┘            │
│      │       │          │                               │
│  ┌───▼──┐ ┌──▼───┐ ┌───▼────────────┐                  │
│  │Sample│ │Qwen  │ │DeepSeek         │                  │
│  │Loader│ │Overlay│ │Overlay          │                  │
│  │      │ │      │ │                 │                  │
│  │data/ │ │httpx │ │httpx            │                  │
│  └──────┘ └──┬───┘ └──┬──────────────┘                  │
│              │        │                                   │
│  ┌──────────▼────────▼──────────┐                        │
│  │      comparison.py            │                        │
│  │  Tone · Divergence · Score    │                        │
│  └───────────────────────────────┘                        │
└──────────────┼────────┼───────────────────────────────────┘
               │        │
    ┌──────────▼──┐  ┌──▼──────────────┐
    │  Qwen Cloud  │  │   DeepSeek API   │
    │ (DashScope)  │  │  (OpenAI-comp.)  │
    │ Alibaba Cloud│  │                  │
    └──────────────┘  └──────────────────┘
```

## Four-Layer Architecture

```
Strategy → Information → Signal → Trading
```

1. **Strategy** — Investment thesis and universe selection
2. **Information** — Evidence pack: quantitative metrics, fundamentals, and market data
3. **Signal** — Dual-LLM qualitative overlay generates structured assessment fields
4. **Trading** — Human-in-the-loop decision gate (LLMs never execute trades)

## Component Responsibilities

### Backend (`backend/`)

| Module                  | Responsibility                                         |
|-------------------------|--------------------------------------------------------|
| `main.py`               | FastAPI app, route definitions, CORS                  |
| `app/models.py`         | Pydantic models: EquityEvidence, OverlayAssessment, QualitativeOverlay, ComparisonResult |
| `app/sample_loader.py`  | Load sample JSON data from `data/`                     |
| `app/qwen_overlay.py`    | Qwen Cloud (DashScope) API integration                 |
| `app/deepseek_overlay.py`| DeepSeek API integration                              |
| `app/comparison.py`     | Tone classification, divergence detection, agreement scoring, full comparison |
| `app/alibaba_cloud_proof.py` | Alibaba Cloud deployment proof endpoints           |

### Frontend (`frontend/`)

| File            | Responsibility                                          |
|-----------------|---------------------------------------------------------|
| `main.tsx`      | React entry point                                       |
| `App.tsx`       | Main app: ticker selector, evidence panel, comparison   |
| `api.ts`        | Typed API client for backend calls                      |
| `style.css`     | Dark theme styling                                       |

## Data Flow

1. User selects a ticker (MA or NVDA)
2. Frontend calls `GET /api/comparison/{ticker}`
3. Backend loads evidence from `data/sample_equity_evidence_{ticker}.json`
4. Backend concurrently calls:
   - `run_qwen_overlay()` → Qwen Cloud `POST /chat/completions` (if `DEMO_MODE != offline`)
   - `run_deepseek_overlay()` → DeepSeek `POST /chat/completions` (if `DEMO_MODE != offline`)
5. If `DEMO_MODE=offline` (default), loads pre-generated sample outputs from `data/`
6. Backend runs comparison logic:
   - **Tone classification** — keyword-based analysis classifies each overlay's tone
   - **Divergence detection** — Jaccard similarity across assessment fields flags major/moderate divergences
   - **Agreement scoring** — weighted score from divergence penalties, tone distance, confidence proximity
   - **Evidence gaps** — merged, deduplicated list from both providers
7. Backend returns `ComparisonResult` with both overlays and comparison metadata
8. Frontend renders side-by-side comparison with badges, scores, and divergence details

## Comparison Fields

Each overlay produces these structured assessment fields:

| Field                  | Description                                    |
|------------------------|------------------------------------------------|
| `business_quality`     | Assessment of overall business quality         |
| `moat`                 | Assessment of moat & competitive advantage     |
| `pricing_power`        | Assessment of pricing power                    |
| `capital_allocation`   | Assessment of management & capital allocation  |
| `red_flags`            | Identified red flags & risks                    |
| `confidence`           | Model confidence (0–1)                         |
| `missing_evidence`     | List of evidence gaps identified by the model  |

## Comparison Output

```json
{
  "ticker": "MA",
  "agreement_score": 0.78,
  "agreement_level": "HIGH",
  "qwen_tone": "conservative_positive",
  "deepseek_tone": "positive",
  "divergences": [],
  "evidence_gaps": [],
  "human_review_required": false
}
```

## Concurrency

Both LLM calls are executed concurrently using `asyncio.gather()`, reducing total latency to the slower of the two providers rather than the sum.

## Error Handling

- Missing credentials → `BLOCKED_BY_MISSING_CREDENTIAL` status (truthful, not faked)
- API errors → `API_ERROR` status with error message
- Offline mode → `OFFLINE_SAMPLE` status
- All statuses are rendered in the frontend with colored badges
- Human review is flagged when agreement is LOW, major divergences exist, or either provider returns a non-SUCCESS status

## Full public migration — six governance modules

This repo now ships six public-safe, offline, judge-runnable modules, exposed via
top-level navigation and a unified demo endpoint (`GET /api/judge/full-demo`):

- Five-Model LLM Cockpit — [docs/five_model_llm_cockpit.md](five_model_llm_cockpit.md)
- Macro Risk Budget — [docs/macro_risk_budget.md](macro_risk_budget.md)
- Research Ops / Validation Console — [docs/research_ops_validation.md](research_ops_validation.md)
- Canonical Data Lineage — [docs/data_lineage.md](data_lineage.md)
- Paper / Shadow Trading Gateway (LIVE disabled) — [docs/paper_gateway.md](paper_gateway.md)
- BTC Three-Layer Decision Stack — [docs/btc_three_layer_stack.md](btc_three_layer_stack.md)

Verify every module in one command: `./scripts/judge_smoke.sh` (47 checks, all green).
