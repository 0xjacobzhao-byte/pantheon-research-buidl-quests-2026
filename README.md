# Pantheon Research — BUIDL_QUESTS 2026

> **AI-native investment research operating system for public markets.**

Pantheon Research combines structured market data, institutional-style
investment frameworks, deterministic signal engines, backtest analytics,
data-quality tooling and LLM-powered research overlays in one cross-asset
research platform.

> **Core belief:** AI should not replace the investor. AI should compound the
> investor's discipline.

Built and operated by **one founder** — the BUIDL_QUESTS / OPC relevance is that
a single person designs the research methodology, engineers the platform,
deploys the cloud infrastructure, runs data operations, and drives go-to-market,
using AI-assisted development and multi-model research workflows to multiply that
capacity. Final investment judgment stays human. No autonomous trade execution is
claimed.

> **Judges:** start with [`docs/judge_evidence.md`](docs/judge_evidence.md) for a
> reproducible verification path, and [`docs/buidl_quests_submission.md`](docs/buidl_quests_submission.md)
> for the OpenArena submission copy.

---

## Submission Links

| | |
|---|---|
| 🌐 Live Product | https://pantheon-research.com |
| 💻 Public Code (this repo) | https://github.com/0xjacobzhao-byte/pantheon-research-buidl-quests-2026 |
| 👤 Founder / X | https://x.com/0xjacobzhao |
| ☁️ Live Deployment Proof (secret-free) | http://8.222.191.152/api/proof/alibaba-cloud |

> A demo video and pitch deck can be attached in the OpenArena form — see
> "Remaining actions" at the end of this document. Prior hackathon media is not
> reused here unless it accurately represents this submission.

---

## Judge Note

* The **live website** (pantheon-research.com) is the broader **production
  product**.
* **This repository** is a **sanitized, public, self-contained review slice** —
  clone it and run it in minutes with no secrets.
* The **private production repository** contains proprietary strategy logic,
  production infrastructure, and operational assets, and remains closed.
* This public repository exists so judges can inspect and run representative
  components safely.

---

## 3-Minute Judge Path

1. **Open the live product** — https://pantheon-research.com
2. **Read the architecture & module overview** — [below](#what-pantheon-research-does)
   and [`docs/architecture.md`](docs/architecture.md)
3. **Inspect the evidence-pack + multi-model comparison** —
   [`backend/app/evidence_pack.py`](backend/app/evidence_pack.py) ·
   [`backend/app/comparison.py`](backend/app/comparison.py)
4. **Run the offline demo**
   ```bash
   docker compose up --build          # frontend :5173 · backend :8000
   ```
5. **Run the smoke test**
   ```bash
   ./scripts/judge_smoke.sh           # offline, no secrets
   ```
6. **Read the evidence guide** — [`docs/judge_evidence.md`](docs/judge_evidence.md)

---

## What Pantheon Research Does

Pantheon Research is a **cross-asset** research operating system. The production
product spans these domains:

| Domain | | Domain | |
|---|---|---|---|
| Global Macro | Bitcoin | Commodities | Technical Analysis |
| US Equities | Ethereum | Fixed Income | Research Ops |
| China Equities | DeFi | Currencies (FX) | |
| Hong Kong Equities | Singapore Equities | | |

**In the production product:** all domains above are covered with structured
frameworks, data feeds, and dashboards.

**In this public repository slice:** the runnable demo focuses on the **equities
qualitative-overlay** feature (MA, NVDA) plus **context-only** mini panels for
Macro, Market Pulse / TA, and FICC (FI/FX/Commodity), a Research-Ops / data
quality view, and a module snapshot grid. Not every production module is copied
into this public slice — the demo is representative, not a full clone.

---

## Four-Layer Investment Stack

```text
Strategy ──▶ Information ──▶ Signal ──▶ Trading
```

| Layer | Role |
|-------|------|
| **Strategy** | Research frameworks and investment hypotheses; universe selection |
| **Information** | Normalized market data, evidence packs, APIs, and dashboards |
| **Signal** | Deterministic signals **plus** LLM research interpretation of structured evidence |
| **Trading** | Future / staged layer — **not active autonomous execution**; a human-in-the-loop decision gate |

**Safety:** LLMs do not execute trades. Every signal passes a human-review gate.
Pantheon Research is not an autonomous trading bot.

---

## AI Innovation

Pantheon separates a **deterministic framework layer** from an **LLM
research-overlay layer** — the LLM interprets governed evidence, it does not
free-associate from raw prompts.

**Deterministic framework layer**
* structured market inputs and evidence packs;
* scoring and signal logic;
* backtests;
* data-quality labels and `data_state` honesty;
* audit trails via content hashing.

**LLM research-overlay layer**
* LLMs analyze a structured evidence pack, not a bare prompt;
* multiple models examine the **same** evidence;
* model outputs are compared side-by-side;
* disagreements and missing evidence are surfaced;
* human review remains central.

This is AI-assisted research, not autonomous agents: there is no agent
orchestration runtime and no autonomous execution.

---

## Why This Is Not Just an LLM Wrapper

Every capability below points to a real file in this repository.

| Capability | Implementation |
|------------|---------------|
| **Fail-closed model states** — missing key → `BLOCKED_BY_MISSING_CREDENTIAL`, bad JSON → `PARSE_ERROR`, missing sample → `QWEN_NOT_GENERATED` | [`qwen_overlay.py`](backend/app/qwen_overlay.py) · [`models.py`](backend/app/models.py) |
| **Evidence hashing** — every pack committed to a `sha256` content hash threaded into each comparison | [`evidence_pack.py`](backend/app/evidence_pack.py) |
| **Multi-model agreement & divergence** — independent models, per-field divergence, `data_state` (`LIVE_DUAL` / `OFFLINE_SAMPLE` / `MIXED` / `PARTIAL` / `BLOCKED`) | [`comparison.py`](backend/app/comparison.py) |
| **Human-review gate** — low agreement or major divergence flags `human_review_required`; fail-closed yields `NOT_COMPARABLE` | [`comparison.py`](backend/app/comparison.py) · [`OverlayComparisonPanel.tsx`](frontend/src/components/equity/OverlayComparisonPanel.tsx) |
| **Multi-asset scope** — Macro · TA · FICC · Equity module grid with per-module `data_state` | [`sample_modules.py`](backend/app/sample_modules.py) · [`ModuleSnapshotGrid.tsx`](frontend/src/components/ModuleSnapshotGrid.tsx) |
| **Research-Ops panel** — governance snapshot: provider config, coverage, per-ticker state | [`data_quality.py`](backend/app/data_quality.py) · [`DataQualityPanel.tsx`](frontend/src/components/DataQualityPanel.tsx) |
| **Validation methodology** — the overlay is a tracked signal, not an alpha oracle | [`docs/validation_methodology.md`](docs/validation_methodology.md) |
| **Secret-free deployment proof** — host-honest proof endpoint, booleans only | [`alibaba_cloud_proof.py`](backend/app/alibaba_cloud_proof.py) · [`docs/live_proof.md`](docs/live_proof.md) |

---

## Why This Fits the OPC Model

Pantheon Research is a **one-person company**:

* one founder coordinates product design, research methodology, engineering,
  cloud deployment, data operations, and go-to-market;
* AI-assisted development (LLM coding tools) and multi-model research workflows
  make this breadth achievable solo;
* structured deterministic frameworks stay separate from LLM interpretation;
* the human founder retains product judgment and investment responsibility.

This is the Super Individual thesis in practice — not an autonomous-agent product,
but a single operator whose research, engineering, and operational capacity are
multiplied by AI.

---

## Current Progress

Reported honestly (roadmap items are not claimed as complete):

* **Live web product** at pantheon-research.com;
* multi-asset research modules across the domains listed above;
* multi-model LLM research overlays with side-by-side comparison;
* Research-Ops / data-quality tooling;
* a live cloud deployment (Alibaba ECS) with a secret-free proof endpoint;
* ongoing backtest and forward-validation work (methodology documented; not an
  alpha claim);
* commercialization preparation (in progress).

---

## Business Model

* subscription plans for individual investors;
* premium research tiers;
* paid research / evaluation APIs;
* B2B / institutional licensing;
* reusable investment "Skills";
* controlled execution **only after** validation — not today.

No revenue, user, or AUM figures are claimed.

---

## Repository Scope

**This repository is:** sanitized · self-contained · representative · public for
hackathon review.

**This repository is not:** a full production clone · a database dump · the
complete proprietary strategy library · a live-trading system.

See [`docs/security_and_sanitization.md`](docs/security_and_sanitization.md).

---

## Quick Start

```bash
git clone https://github.com/0xjacobzhao-byte/pantheon-research-buidl-quests-2026
cd pantheon-research-buidl-quests-2026
docker compose up --build          # frontend :5173 · backend :8000
./scripts/judge_smoke.sh           # end-to-end smoke test (offline, no secrets)
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

## Tests

Verified in this repository:

```bash
cd backend && python -m pytest             # 84 backend tests
cd frontend && npm test -- --run           # 9 frontend tests
cd frontend && npm run build               # production build (tsc + vite)
docker compose config                      # validate compose file
./scripts/judge_smoke.sh                   # end-to-end smoke (18 checks, offline)
```

---

## Safety Boundary

* AI **assists** research; LLM outputs are **not investment advice**.
* Missing or unusable data **fails closed** — never a fabricated result.
* Humans retain investment judgment; every signal passes a human-review gate.
* Pantheon Research does **not** currently execute autonomous trades.
* No private data, secrets, or broker credentials are included in this repository.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | FastAPI · Python 3.11–3.12 |
| Frontend | React 18 · TypeScript · Vite 6 |
| LLM providers | Qwen (Alibaba DashScope) · DeepSeek — both OpenAI-compatible |
| Database | PostgreSQL (Alibaba RDS-compatible) — production only |
| Deploy | Docker Compose · Alibaba ECS (Nginx → FastAPI) |
| Tests | pytest (backend) · vitest + Testing Library (frontend) |

---

## Author & License

**Jacob Zhao** — [0xjacobzhao-byte](https://github.com/0xjacobzhao-byte) ·
[x.com/0xjacobzhao](https://x.com/0xjacobzhao)

**License:** Apache-2.0 — see [LICENSE](LICENSE).

No API keys, private user data, live trading credentials, production secrets, or
private financial records are included in this repository.
