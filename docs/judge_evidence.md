# Judge Evidence Guide

**Pantheon Research — BUIDL_QUESTS 2026.** A reproducible verification path for
the public repository slice: evidence packs, the multi-model overlay comparison,
fail-closed model handling, Research-Ops governance, and a local offline smoke
test. The Alibaba ECS / DashScope-Qwen deployment and RDS selected mirror are
included as **supporting evidence** of a real live deployment — not as the
identity of the project.

## 1. What to inspect first

| Question | Evidence |
|---|---|
| Is the backend running on Alibaba Cloud? | Live proof endpoint + [`backend/app/alibaba_cloud_proof.py`](../backend/app/alibaba_cloud_proof.py) |
| Is Qwen / DashScope actually integrated? | [`backend/app/qwen_overlay.py`](../backend/app/qwen_overlay.py) + qwen-smoke endpoint |
| Is this more than an API wrapper? | Evidence hash, comparison engine, fail-closed states, human-review gate |
| Is RDS overclaimed? | `database.production_data_migrated=false`, `mirror_state=partial_selected_mirror` |
| Can I run it locally? | `docker compose up --build` + `./scripts/judge_smoke.sh` |

## 2. Live URLs

| What | URL |
|------|-----|
| Live product | https://pantheon-research.com |
| Alibaba deployment | http://8.222.191.152 |
| Deployment proof | http://8.222.191.152/api/proof/alibaba-cloud |
| Demo video | https://www.youtube.com/watch?v=68lceOACLKo |
| Deck | [Google Slides](https://docs.google.com/presentation/d/1E72ORBmaiL2QPbmL1CPBqrbSLLOsAVEnDxdo76IPJqs/edit?usp=sharing) |
| Public code | https://github.com/0xjacobzhao-byte/pantheon-research-buidl-quests-2026 |

## 3. Code evidence

| What to verify | File |
|---|---|
| Deployment proof (host, services, secrets) | [`backend/app/alibaba_cloud_proof.py`](../backend/app/alibaba_cloud_proof.py) |
| Qwen / DashScope API call implementation | [`backend/app/qwen_overlay.py`](../backend/app/qwen_overlay.py) |
| Dual-model comparison engine | [`backend/app/comparison.py`](../backend/app/comparison.py) |
| Evidence pack + provenance hashing | [`backend/app/evidence_pack.py`](../backend/app/evidence_pack.py) |
| Data quality / Research-Ops | [`backend/app/data_quality.py`](../backend/app/data_quality.py) |
| Pydantic models (proof schema) | [`backend/app/models.py`](../backend/app/models.py) |
| Fail-closed LLM handling | [`backend/app/qwen_overlay.py`](../backend/app/qwen_overlay.py) · [`tests/test_qwen_fail_closed.py`](../backend/tests/test_qwen_fail_closed.py) |

## 4. Verification commands

```bash
# Live deployment proof (no auth required)
curl -s http://8.222.191.152/api/proof/alibaba-cloud | jq

# Live comparison data_state
curl -s http://8.222.191.152/api/equity/overlay-comparison/US/NVDA | jq '.data_state'

# Local smoke (no secrets needed)
docker compose up --build
./scripts/judge_smoke.sh

# Backend tests
cd backend && python -m pytest

# Frontend tests + build
cd frontend && npm test -- --run && npm run build

# Secret scan (should be clean)
grep -RInE "(sk-|AKIA|DASHSCOPE_API_KEY=|DEEPSEEK_API_KEY=|DATABASE_URL=postgres|x-admin-token|BEGIN PRIVATE KEY|github_pat_|ghp_)" . \
  --exclude-dir=.git --exclude-dir=node_modules --exclude-dir=.venv || true
```

## 5. Safe claims (defensible, verifiable)

1. **Backend deployment proof is served by a Dockerized FastAPI app behind Nginx.**
2. **The live Alibaba ECS box reports `alibaba_hosted=true` and `host_runtime=Alibaba Cloud ECS`.**
3. **Qwen integration uses Alibaba Cloud Model Studio / DashScope in OpenAI-compatible mode.**
4. **Actual Qwen API call implementation is in [`backend/app/qwen_overlay.py`](../backend/app/qwen_overlay.py).**
5. **Public proof endpoint makes no external calls and returns no secrets.**
6. **Admin-gated qwen-smoke endpoint performs a real Qwen smoke call on the live ECS host.**
7. **Alibaba RDS is connected as a selected evidence mirror on the live ECS deployment.**
8. **Dual-model comparison is real.** Two independent providers (Qwen, DeepSeek) assess the same evidence pack; agreement / divergence / tone are computed.
9. **Evidence is provenance-committed.** Each evidence pack is bound to a `sha256` content hash.
10. **Offline mode is fully functional** with bundled samples and no secrets.

## 6. Non-claims (explicitly NOT asserted)

1. **Alibaba RDS is NOT a full production database clone.**
2. **Alibaba RDS is NOT a byte-for-byte production migration.**
3. **Not claiming all APIs read from Alibaba RDS.**
4. **Not claiming autonomous trading or model-generated alpha.** LLMs never execute trades.
5. **Not exposing private production strategy code.**
6. **This public repository is a sanitized vertical slice**, not the full private production system.

## 7. Qwen coverage snapshot

| Metric | Value |
|--------|-------|
| Qwen comparison-capable coverage | 312 tickers |
| Healthy comparisons | 312 / 312 |
| DeepSeek baseline universe | 1,331 |
| Markets | US 117 / CN 69 / HK 103 / SG 23 |
| Full-universe parity | not pursued; low-liquidity tail intentionally excluded |

## 8. Proof bundle

A machine-readable proof bundle is committed at
[`data/judge_proof_bundle.json`](../data/judge_proof_bundle.json) — same facts
as above, structured for programmatic inspection.

## 9. What judges can safely conclude in 3 minutes

1. `curl` the live proof endpoint → confirms Alibaba ECS host + DashScope configured + RDS selected mirror.
2. Open [`backend/app/alibaba_cloud_proof.py`](../backend/app/alibaba_cloud_proof.py) → confirms proof code structure, secret-free design, and service map.
3. Open [`backend/app/qwen_overlay.py`](../backend/app/qwen_overlay.py) → confirms actual Qwen API call implementation.
4. Run `./scripts/judge_smoke.sh` → confirms offline demo works end-to-end with no secrets.
