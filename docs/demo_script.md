# Demo Script

Three timed walkthroughs of the public Pantheon Research slice. Everything runs
**offline with no API keys**.

## Setup (once)

```bash
docker compose up --build      # frontend :5173 · backend :8000
```

---

## 60-second explanation

"Pantheon Research is an AI-native investment research operating system for public
markets, built and run by one founder. It unifies cross-asset evidence, applies
deterministic frameworks, and — in production — layers **five LLMs** (Claude,
ChatGPT, Gemini, DeepSeek, Qwen) that analyze the *same* structured evidence —
then compares them, surfaces disagreement and missing evidence, and hands the
final call to a human. This repo is a sanitized, judge-runnable slice — a
five-model **cached** cockpit plus six offline governance modules; the live
product at pantheon-research.com runs the full live five-model layer across
Vercel + Railway, Google Cloud, and Alibaba Cloud."

Show: open http://localhost:5173, point at the architecture diagram and module
grid, pick **NVDA**, and point at the overlay comparison with its agreement
score and honest `OFFLINE_SAMPLE` labels.

## 3-minute judge walkthrough

1. **Framing (20s).** One-founder, AI-native, cross-asset research OS. Not an
   autonomous-agent product — human-in-the-loop.
2. **Architecture (20s).** Point at the architecture diagram: data sources →
   data platform → research engines → deterministic + five-model LLM layer →
   signal layer → trading (human-gated, no live autonomous execution).
3. **Evidence (30s).** Open the evidence pack for NVDA; note the `sha256`
   content hash (provenance) — the same hash threads into the comparison.
4. **Multi-model overlay (40s).** Show Qwen and DeepSeek analyzing the same
   evidence (the public repo's runnable slice of the five-model layer); point at
   per-field divergence, the agreement score, and the `data_state` headline.
5. **Honesty & fail-closed (30s).** Every result is labelled `OFFLINE_SAMPLE`;
   explain that a missing key yields `BLOCKED_BY_MISSING_CREDENTIAL` and a bad
   model response yields `PARSE_ERROR` — never a fabricated success.
6. **Research-Ops (20s).** Open the data-quality / provider-health panel and the
   module snapshot grid (Macro / TA / FICC context-only).
7. **Close (20s).** Human-review gate; no autonomous trading; the live product
   runs the full system across three cloud footprints.

## 5-minute technical walkthrough

1. Everything in the 3-minute walkthrough.
2. **API tour (60s).** In a terminal:
   ```bash
   curl -s localhost:8000/api/evidence/NVDA | python3 -m json.tool | head
   curl -s localhost:8000/api/comparison/NVDA | python3 -m json.tool | head -40
   curl -s localhost:8000/api/proof/alibaba-cloud | python3 -m json.tool | head -30
   ```
   Point out the evidence hash, the `data_state`, `human_review_required`, and
   that the proof endpoint returns booleans only.
3. **Multi-cloud deployment (30s).** Explain the three-stack footprint: Vercel +
   Railway (core production), Google Cloud (Cloud Run + Gemini), and Alibaba
   Cloud (ECS + DashScope/Qwen) — cloud portability and provider integration,
   not automatic failover. `backend/app/alibaba_cloud_proof.py` is host-honest
   and secret-free; the live ECS box is supporting evidence, not the project
   identity.
4. **Tests (30s).**
   ```bash
   cd backend && python -m pytest        # 84 tests
   cd ../frontend && npm test -- --run    # 9 tests
   ```
5. **Smoke test (30s).**
   ```bash
   ./scripts/judge_smoke.sh               # 18 checks, offline
   ```
6. **Safety boundary (30s).** LLM outputs are not investment advice; missing data
   fails closed; humans retain judgment; no autonomous execution; no secrets in
   the repo.

---

## Expected outputs (offline)

| Action | Expected |
|--------|----------|
| `GET /api/evidence/NVDA` | evidence pack + `provenance.evidence_hash` (`sha256:…`) |
| `GET /api/comparison/NVDA` | `data_state: OFFLINE_SAMPLE`, agreement score, divergences |
| `GET /api/proof/alibaba-cloud` | booleans only; `host_runtime` honest; `production_data_migrated: false` |
| `./scripts/judge_smoke.sh` | `PASS=18  FAIL=0  ALL GREEN` |

## Contingency: no provider keys

This is the **default** path — everything above runs offline with bundled
samples labelled `OFFLINE_SAMPLE`. For live mode, set `DEMO_MODE=live` and a
provider key; without a key the provider fails closed
(`BLOCKED_BY_MISSING_CREDENTIAL`) rather than faking output.

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
