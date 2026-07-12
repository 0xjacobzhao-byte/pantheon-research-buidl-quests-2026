# Safe Claims & Non-Claims

A single, explicit ledger of what this repository **does** and **does not**
claim — so judges (human or AI) never have to guess, and nothing here is an
overclaim.

## Safe claims (defensible, verifiable)

1. **Qwen is called live** via Alibaba Cloud DashScope (Model Studio),
   OpenAI-compatible endpoint, when live mode is enabled
   (`DEMO_MODE=live` + `DASHSCOPE_API_KEY`). The integration is implemented in
   [`backend/app/qwen_overlay.py`](../backend/app/qwen_overlay.py) and is invoked
   by overlay endpoints (not by the proof endpoint itself, which makes no external
   calls). The live Alibaba ECS deployment also exposes an admin-gated
   `/api/proof/qwen-smoke` endpoint that performs a real Qwen smoke call.
2. **The backend runs live on Alibaba Cloud ECS** (Nginx → Dockerized FastAPI),
   reachable at `http://8.222.191.152`, with a public proof endpoint and an
   admin-gated live Qwen smoke. See [`live_proof.md`](live_proof.md).
3. **Host reporting is honest.** The proof exposes `alibaba_hosted`; the same
   image runs on Railway (`false`) and Alibaba ECS (`true`). It never claims
   Alibaba compute when not on it.
4. **Dual-model comparison is real.** Two independent providers (Qwen, DeepSeek)
   assess the same evidence pack; agreement / divergence / tone are computed, not
   assumed. Fail-closed states are explicit; low agreement or major divergence
   routes to human review.
5. **Evidence is provenance-committed.** Each evidence pack is bound to a
   `sha256` content hash threaded through every comparison.
6. **The system is multi-asset.** Macro, Technical, FICC (FI/FX/Commodity), and
   Equity modules exist in production; the public repo surfaces their scope via a
   context-only module grid ([`module_snapshots.md`](module_snapshots.md)).
7. **Offline mode is fully functional** with bundled samples and **no secrets**.

## Non-claims (explicitly NOT asserted)

1. **No autonomous trading.** LLMs never execute trades; every signal passes a
   human-review gate.
2. **No alpha / performance claim.** The overlay is a tracked research signal, not
   an oracle; forward validation is required first
   ([`validation_methodology.md`](validation_methodology.md)).
3. **No production-data migration to Alibaba RDS.** An Alibaba RDS instance is
   provisioned as part of the architecture, but RDS provisioning/connection is
   distinguished from full production-data migration, which is **not** claimed
   without row-count + API read-path verification
   ([`alibaba_deployment_parity.md`](alibaba_deployment_parity.md)).
4. **The context-only module cards are not live nowcasts.** Macro/TA/FICC cards
   are illustrative bundled snapshots; they carry no fair-value bands and no
   trading signals.
5. **No proprietary internals are published.** Market-data pipelines, scoring
   models, provider routing, the production database and its rows, the full
   universe, and the admin plane stay in the private repo.
6. **Live production numbers are withheld**, not fabricated — see
   [`qwen_coverage_report.md`](qwen_coverage_report.md).

## How to verify each claim

| Claim | Verify |
|-------|--------|
| Live Qwen on Alibaba | `curl -s http://8.222.191.152/api/proof/alibaba-cloud \| jq` |
| Dual-model + fail-closed | `./scripts/judge_smoke.sh` · `backend/tests/test_qwen_fail_closed.py` |
| Evidence hashing | `GET /api/evidence/NVDA` → `provenance.evidence_hash` |
| Multi-asset scope | `GET /api/modules` · [`module_snapshots.md`](module_snapshots.md) |
| Alibaba service map | `GET /api/proof/alibaba-cloud` → `alibaba_services{}` (compute/ai/database) |
| No secrets | CI `secret-scan-lite` job · `docs/data_safety.md` |

## Primary proof files

The primary deployment-proof file is
[`backend/app/alibaba_cloud_proof.py`](../backend/app/alibaba_cloud_proof.py).
It proves the host/runtime, secret-free credential state, Alibaba
ECS/RDS/DashScope service map, and safe/non-claims.

The actual Qwen / DashScope API call implementation lives in
[`backend/app/qwen_overlay.py`](../backend/app/qwen_overlay.py).
