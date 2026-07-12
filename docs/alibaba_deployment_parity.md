# Alibaba Cloud Deployment Parity

This document states precisely what runs on Alibaba Cloud, so the deployment
claim can be verified and is not overstated.

## Live endpoint

- **Alibaba Cloud ECS:** `http://8.222.191.152` (Nginx reverse proxy → Dockerized FastAPI backend)
- **Live product:** `https://pantheon-research.com` (full production frontend)

## What IS on Alibaba Cloud

| Component | Status | Evidence |
| --- | --- | --- |
| Compute | **Alibaba Cloud ECS**, Nginx + Dockerized FastAPI (same backend image as Railway) | `GET /health` → 200; `GET /api/proof/alibaba-cloud` → `runtime: "Alibaba Cloud ECS"` |
| AI provider | **Alibaba Cloud Model Studio / DashScope (Qwen)** | `POST /api/proof/qwen-smoke` returns a live Qwen-generated summary |
| Frontend | Full production SPA, built from private `master` (parity target: Vercel) | served at `/` by Nginx |

### Alibaba service map (structured, secret-free)

The v2 proof endpoint also returns a structured `alibaba_services` map covering
three Alibaba Cloud products:

| Service | Product | Evidence |
| --- | --- | --- |
| **Compute** | Alibaba Cloud ECS | `host_runtime` + `alibaba_hosted` runtime marker |
| **AI** | Alibaba Cloud Model Studio / DashScope | `base_url`, `model`, `credential_configured`, `live_smoke_endpoint`, `actual_call_implementation` |
| **Database** | Alibaba RDS PostgreSQL-compatible | `role: selected evidence mirror`, `mirror_state: partial_selected_mirror` |

The actual Qwen / DashScope API call implementation lives in
[`backend/app/qwen_overlay.py`](../backend/app/qwen_overlay.py).

The proof endpoint reports **booleans only** for configuration
(`qwen_configured`, `dashscope_api_key_configured`, `database_url_configured`) —
never secret values — and honestly labels the host runtime.

## Database — RDS provisioning vs data migration (precise, no overclaiming)

The distinction that matters for judges:

| Question | State | How it's known |
| --- | --- | --- |
| RDS **provisioned/deployed**? | **Yes** | An Alibaba RDS PostgreSQL-compatible instance is part of the Alibaba Cloud architecture |
| RDS **configured** on the ECS box? | `database.configured: true` | Live proof boolean (a DB URL is set; never the value) |
| RDS **connected** (live read path)? | **Yes — selected evidence mirror** | Live v2 proof `database.connected: true`, `role: "selected evidence mirror"`, `mirror_state: "partial_selected_mirror"` (operator-attested session; the public offline demo endpoint performs no probe and reports `connected: null`) |
| Full production data **migrated** to RDS? | **Not claimed** | `production_data_migrated: false`, `full_production_clone_verified: false` — would require core-table row-count + API read-path proof; not asserted |

The production data platform (1,300+ equity overlays) currently lives in
**Railway Postgres**; the rich DeepSeek-vs-Qwen **comparison data** is served
from there (via Vercel/Railway). The Alibaba box's proven role today is the
**live-hosted backend + live Qwen call**. RDS provisioning is **not** conflated
with full production-data migration.

> **Proof v2 (live).** The live proof endpoint serves the v2 shape (host-honest
> fields + an explicit `database{}` block with `connected`, `role`,
> `mirror_state`, `production_data_migrated`, `full_production_clone_verified`).
> RDS is deployed and connected as a **selected evidence mirror**; full
> production-data migration is **not** claimed without core-table row counts and
> API read-path proof.

The public offline demo needs **no database** at all — it runs on bundled samples.

## How to verify (no secrets needed for the public parts)

```bash
curl -s http://8.222.191.152/health
curl -s http://8.222.191.152/api/proof/alibaba-cloud | jq
# admin-gated live Qwen call (operator supplies the box-local token):
curl -s -X POST http://8.222.191.152/api/proof/qwen-smoke \
  -H "Content-Type: application/json" -H "x-admin-token: $ADMIN_TOKEN" \
  -d '{"prompt":"In one sentence, what is Pantheon Research?"}' | jq
```

See [`live_proof.md`](live_proof.md) for captured real responses.

## Safe claim

> "The Pantheon Research backend is deployed on Alibaba Cloud ECS (Nginx →
> Dockerized FastAPI) and calls Qwen live via Alibaba Cloud Model Studio /
> DashScope, provable at a public proof endpoint. The proof code lives in
> [`backend/app/alibaba_cloud_proof.py`](../backend/app/alibaba_cloud_proof.py)
> and the Qwen call implementation in
> [`backend/app/qwen_overlay.py`](../backend/app/qwen_overlay.py). An Alibaba
> RDS PostgreSQL-compatible instance is provisioned as part of the architecture
> as a **selected evidence mirror** (`mirror_state: partial_selected_mirror`),
> but RDS **provisioning/connection is distinguished from full production-data
> migration** — migration is claimed only when row counts and API read-path are
> verified. The production research-data platform remains on Railway/Vercel."
