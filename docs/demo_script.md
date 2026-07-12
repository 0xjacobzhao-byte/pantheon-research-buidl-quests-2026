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
deterministic frameworks, and layers **multiple LLMs** that analyze the *same*
structured evidence — then compares them, surfaces disagreement and missing
evidence, and hands the final call to a human. This repo is a sanitized slice you
can run in one command; the live product is at pantheon-research.com."

Show: open http://localhost:5173, pick **NVDA**, and point at the overlay
comparison with its agreement score and honest `OFFLINE_SAMPLE` labels.

## 3-minute judge walkthrough

1. **Framing (20s).** One-founder, AI-native, cross-asset research OS. Not an
   autonomous-agent product — human-in-the-loop.
2. **Evidence (40s).** Open the evidence pack for NVDA; note the `sha256`
   content hash (provenance) — the same hash threads into the comparison.
3. **Multi-model overlay (40s).** Show Qwen and DeepSeek analyzing the same
   evidence; point at per-field divergence, the agreement score, and the
   `data_state` headline.
4. **Honesty & fail-closed (30s).** Every result is labelled `OFFLINE_SAMPLE`;
   explain that a missing key yields `BLOCKED_BY_MISSING_CREDENTIAL` and a bad
   model response yields `PARSE_ERROR` — never a fabricated success.
5. **Research-Ops (30s).** Open the data-quality / provider-health panel and the
   module snapshot grid (Macro / TA / FICC context-only).
6. **Close (20s).** Human-review gate; no autonomous trading; the live product is
   the broader system.

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
3. **Deployment proof (30s).** Explain `backend/app/alibaba_cloud_proof.py`:
   host-honest, secret-free, no external calls; the live ECS box is supporting
   evidence, not the project identity.
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
