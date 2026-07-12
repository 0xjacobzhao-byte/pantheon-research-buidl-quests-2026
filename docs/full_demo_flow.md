# Unified Judge Demo Flow

One endpoint links every module in a single NVDA-anchored research flow plus a
BTC cross-asset flow, with a live status for each step:

```
GET /api/judge/full-demo
```

## Equity flow (NVDA)

1. Load provider & canonical market data — `/api/data-platform/observations`
2. Inspect observation versions & evidence hash — `/api/data-platform/lineage/{hash}`
3. Build evidence pack — `/api/evidence/NVDA`
4. Apply macro risk budget — `/api/macro/risk-budget`
5. Run five-model cached comparison — `/api/llm/comparison/NVDA`
6. Inspect agreement, red flags & missing evidence — `/api/llm/agreement/NVDA`
7. Check Research Ops readiness — `/api/research-ops/summary`
8. Create provenance-stamped paper intent — `/api/paper-gateway/intent/intent_nvda_001`
9. Run risk gate — `/api/paper-gateway/intent/intent_ma_002`
10. Human approves paper simulation — `/api/paper-gateway/intent/intent_nvda_001/approve`
11. Inspect append-only audit timeline — `/api/paper-gateway/audit`

## BTC flow

1. Load BTC L1/L2/L3 — `/api/btc/stack`
2. Apply macro risk context — `/api/macro/risk-budget`
3. Resolve layer conflict — `/api/btc/conflicts`
4. Produce research posture — `/api/btc/current-posture`
5. No automatic execution — `/api/paper-gateway/status`

## Reproduce locally

```bash
cd backend && pip install -r requirements.txt && uvicorn main:app --port 8000 &
./scripts/judge_smoke.sh    # 47 checks across every module, ALL GREEN
```

Everything is offline, deterministic, and secret-free. LLM outputs never execute
trades; a human remains the portfolio manager.
