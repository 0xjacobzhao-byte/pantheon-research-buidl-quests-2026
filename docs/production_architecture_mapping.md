# Production Architecture Mapping

This public repo is a **sanitized, reproducible vertical slice** of the private
production Pantheon Research system. It is deliberately small enough to run from
scratch in minutes, while faithfully mirroring the real Qwen integration. This
document maps each public file to its production counterpart and states what is
intentionally excluded and why.

## System at a glance

| Layer | Production (private) | This public repo |
| --- | --- | --- |
| Frontend | React + Vite SPA on **Vercel** (`pantheon-research.vercel.app`), ~40 route modules | React + Vite SPA, single Ticker-Profile comparison view |
| Backend | FastAPI on **Railway**, ~200 routers (equities, macro, BTC/ETH, FICC, research-ops) | FastAPI, the overlay + proof endpoints only |
| Database | **Railway Postgres** (`product_snapshots` + ~60 tables), 1,300+ equity overlays; an **Alibaba RDS** instance is provisioned (migration not asserted — see [`alibaba_deployment_parity.md`](alibaba_deployment_parity.md)) | none required — bundled sample JSON (offline) |
| LLM overlay | DeepSeek (primary) + **Qwen via Alibaba DashScope** (comparison), batch-generated, DB-persisted | Same two providers, request-time, offline samples by default |
| Cloud proof | **Alibaba Cloud ECS** (Nginx → Dockerized FastAPI) running the same backend image | The `alibaba_cloud_proof` + `qwen_overlay` modules, live at the ECS URL |

## File-by-file mapping

| Public file | Production counterpart | Notes |
| --- | --- | --- |
| `backend/app/qwen_overlay.py` | `backend_gateway/providers/qwen_client.py` + `services/equity_qwen_overlay.py` | Same DashScope OpenAI-compatible call (`dashscope-intl.aliyuncs.com/compatible-mode/v1`), same env-var resolution (`DASHSCOPE_API_KEY` / `QWEN_API_KEY`), same fail-closed + `PARSE_ERROR` handling. Production adds evidence-pack construction, prompt-versioning, and DB persistence. |
| `backend/app/deepseek_overlay.py` | `backend_gateway/providers/deepseek_client.py` | Symmetric DeepSeek path. |
| `backend/app/comparison.py` | `backend_gateway/services/equity_overlay_comparison.py` | Public repo uses tone/Jaccard heuristics; production compares persisted factor verdicts (`moat_pricing_power`, `red_flags`, …) across providers and emits `data_state` (`HEALTHY_REAL_DATA`, `QWEN_NOT_GENERATED`, …). |
| `backend/app/alibaba_cloud_proof.py` | `backend_gateway/routers/alibaba_cloud_proof.py` + `services/alibaba_qwen_client.py` | Production version is host-aware: on Railway it reports `host_runtime: "Railway"` / `alibaba_hosted: false`; on the ECS box `Alibaba Cloud ECS` / `true`. Both expose an admin-gated live `qwen-smoke`. |
| `frontend/.../OverlayComparison*` | `frontend/components/equity/OverlayComparisonPanel.tsx` | Production panel renders unconditionally inside the Ticker Profile cockpit and fetches `/api/equity/overlay-comparison/{market}/{ticker}`. |
| `backend/tests/*` | `backend_gateway/tests/test_overlay_comparison.py` + `test_qwen_cloud_provider.py` | Public repo: **56 tests** across proof / fail-closed / data-state / evidence-pack / comparison. |

## Intentionally excluded (and why)

- **Proprietary data pipelines** (market-data ingestion, evidence-pack builders,
  provider routing, scoring models) — the moat, and not needed to demonstrate the
  Qwen integration.
- **Production database + real overlay rows** — would require credentials and
  leak proprietary research. Replaced by realistic bundled samples.
- **Secrets / infra config** — no `.env`, no connection strings, no keys. Only
  `.env.example` with placeholders.
- **The other ~40 frontend modules and ~200 routers** — out of scope for a
  judging demo; they don't change the Qwen story.

## What is faithfully preserved

- The exact DashScope OpenAI-compatible call path and credential resolution.
- The two-provider (Qwen vs DeepSeek) comparison model with explicit,
  non-`SUCCESS` states for missing/failed generations.
- The Alibaba Cloud proof surface, live at a real ECS endpoint (see
  [`live_proof.md`](live_proof.md) and [`alibaba_deployment_parity.md`](alibaba_deployment_parity.md)).
