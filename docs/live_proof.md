# Live Proof — Alibaba Cloud + Qwen

This document ties the sanitized code in this repo to a **live Alibaba Cloud
deployment** so judges can verify the integration end-to-end, not just read code.

- **Public demo repo (this repo):** https://github.com/0xjacobzhao-byte/pantheon-research-buidl-quests-2026
- **Live Alibaba Cloud endpoint (ECS + Nginx + Dockerized FastAPI):** `http://8.222.191.152`
- **Qwen integration source:** [`backend/app/qwen_overlay.py`](../backend/app/qwen_overlay.py)
- **Alibaba proof source:** [`backend/app/alibaba_cloud_proof.py`](../backend/app/alibaba_cloud_proof.py)

> The full production system (Vercel + Railway + Postgres, 1,300+ equities with
> DeepSeek overlays and a DeepSeek-vs-Qwen comparison UI) is a **private** repo.
> This repo is a sanitized, reproducible vertical slice. The Alibaba box above
> runs the same FastAPI backend image and is the public, judge-facing proof that
> Qwen is called live from Alibaba Cloud infrastructure.

## 1. Public-safe deployment proof (no auth, no secrets)

```bash
curl -s http://8.222.191.152/api/proof/alibaba-cloud | jq
```

Live response (`alibaba-proof-v2`, values are booleans/descriptors only — never
secrets). Abridged; the full captured payload is committed at
[`docs/assets/alibaba_live_proof.json`](assets/alibaba_live_proof.json):

```json
{
  "schema_version": "alibaba-proof-v2",
  "project": "Pantheon Research",
  "status": "ok",
  "cloud_provider": "Alibaba Cloud",
  "qwen_provider": "Alibaba Cloud Model Studio / DashScope",
  "host_runtime": "Alibaba Cloud ECS",
  "alibaba_hosted": true,
  "backend_runtime": "Dockerized FastAPI",
  "reverse_proxy": "Nginx",
  "qwen_model": "qwen3.7-plus",
  "qwen_configured": true,
  "dashscope_api_key_configured": true,
  "database_url_configured": true,
  "alibaba_services": {
    "compute": {
      "service": "Alibaba Cloud ECS",
      "evidence": "host_runtime + alibaba_hosted runtime marker",
      "host_runtime": "Alibaba Cloud ECS",
      "alibaba_hosted": true
    },
    "ai": {
      "service": "Alibaba Cloud Model Studio / DashScope",
      "base_url": "https://dashscope-intl.aliyuncs.com/compatible-mode/v1",
      "model": "qwen3.7-plus",
      "credential_configured": true,
      "live_smoke_endpoint": "/api/proof/qwen-smoke",
      "actual_call_implementation": "backend/app/qwen_overlay.py"
    },
    "database": {
      "service": "Alibaba RDS PostgreSQL-compatible",
      "role": "selected evidence mirror",
      "mirror_state": "partial_selected_mirror",
      "production_data_migrated": false,
      "full_production_clone_verified": false
    }
  },
  "database": {
    "provider": "Alibaba RDS PostgreSQL-compatible",
    "configured": true,
    "connected": true,
    "role": "selected evidence mirror",
    "mirror_state": "partial_selected_mirror",
    "production_data_migrated": false,
    "full_production_clone_verified": false,
    "note": "Alibaba RDS is deployed and connected as a selected evidence mirror. Full production-data migration is not claimed without core table row counts and API read-path verification."
  },
  "timestamp_utc": "2026-07-02T22:50:30Z"
}
```

The `alibaba_services` block is a structured, secret-free service map covering
compute (ECS), AI (Model Studio / DashScope), and database (RDS). Each service
entry names the Alibaba Cloud product, the evidence type, and the relevant
configuration state — never a credential value.

On the live ECS box the RDS block reports `connected: true` (an operator-attested
session). The public offline backend in *this* repo makes no probe, so its own
`/api/proof/alibaba-cloud` reports `connected: null` — both are honest about what
they actually verified.

`runtime` reports the **actual** host (`Alibaba Cloud ECS`). In the private
production repo the same endpoint is environment-aware: on Railway it reports
`host_runtime: "Railway"` / `alibaba_hosted: false`, so no deployment ever
pretends to be hosted somewhere it is not. The Qwen **AI provider** is Alibaba
Cloud Model Studio (DashScope) on every host.

`database_url_configured: true` is a **boolean signal only** — a database URL is
set on the box. The `database{}` block is precise: RDS is a **selected evidence
mirror** (`mirror_state: partial_selected_mirror`), not a full production clone.
`production_data_migrated` and `full_production_clone_verified` are both **false**
— migration is not claimed without core-table row counts and API read-path
verification. See [`alibaba_deployment_parity.md`](alibaba_deployment_parity.md)
for the full provisioning-vs-migration breakdown.

> **Proof v2 (live).** Both the live ECS box and this repo's backend serve the
> **v2** proof shape
> ([`backend/app/alibaba_cloud_proof.py`](../backend/app/alibaba_cloud_proof.py)):
> `schema_version`, `alibaba_hosted`, a structured `database{}` block
> (`connected`, `role`, `mirror_state`, `production_data_migrated`,
> `full_production_clone_verified`), `safe_claims`, and `non_claims`. The private
> production backend that runs on the box was source-controlled so a rebuild
> preserves the honest v2 wording; the safer RDS semantics
> (`production_data_migrated: false`, selected evidence mirror) are the source of
> truth.

## 2. Live Qwen call (admin-gated smoke test)

The smoke endpoint performs a **real** Qwen chat-completion via Alibaba Cloud
Model Studio's OpenAI-compatible endpoint
(`https://dashscope-intl.aliyuncs.com/compatible-mode/v1`). It is gated by an
admin token and fails closed (503) when no token is configured.

```bash
# ADMIN_TOKEN is held only on the server; the operator runs this during the demo.
curl -s -X POST http://8.222.191.152/api/proof/qwen-smoke \
  -H "Content-Type: application/json" \
  -H "x-admin-token: $ADMIN_TOKEN" \
  -d '{"prompt": "In two sentences, describe Pantheon Research."}' | jq
```

Live response (captured 2026-07-02, ~14s round-trip — `qwen3.7-plus` is a
reasoning-class model, allow up to ~30s):

```json
{
  "project": "Pantheon Research",
  "status": "ok",
  "cloud_provider": "Alibaba Cloud",
  "ai_platform": "Alibaba Cloud Model Studio / Qwen",
  "qwen_model": "qwen3.7-plus",
  "prompt": "In two sentences, describe Pantheon Research.",
  "summary": "Pantheon Research is an independent, multi-asset market research platform that provides institutional investors with in-depth macroeconomic and financial analysis. The firm delivers actionable insights, forecasting, and strategic advice across global asset classes to help clients navigate complex market environments.",
  "timestamp_utc": "2026-07-02T11:57:03Z"
}
```

A redacted copy of a live smoke response is committed at
[`data/qwen_live_smoke_sample_redacted.json`](../data/qwen_live_smoke_sample_redacted.json)
(no API key, no auth headers).

Auth behaviour (verified live):

| Request | Result |
| --- | --- |
| No `x-admin-token` | `401` |
| `ADMIN_TOKEN` unset on server | `503` (fails closed — never public) |
| Valid token, `DASHSCOPE_API_KEY` set | `200` + live Qwen summary |

## 3. How the Qwen call works in code

[`backend/app/qwen_overlay.py`](../backend/app/qwen_overlay.py) posts to the
DashScope OpenAI-compatible `/chat/completions` endpoint with
`Authorization: Bearer $DASHSCOPE_API_KEY` and `model = $QWEN_MODEL`. Two modes:

- **Offline (default, `DEMO_MODE=offline`):** returns bundled sample overlays so
  the repo runs with zero credentials.
- **Live (`DEMO_MODE=live` + `DASHSCOPE_API_KEY`):** calls Qwen for real. Missing
  key → structured `BLOCKED_BY_MISSING_CREDENTIAL`; non-JSON model output →
  explicit `PARSE_ERROR` (never a hollow `SUCCESS`).

`backend/app/deepseek_overlay.py` is the symmetric DeepSeek path, and
`backend/app/comparison.py` computes tone / divergence / agreement between the
two providers.

## 4. What judges can safely conclude

- The backend runs on **Alibaba Cloud ECS** (Nginx reverse proxy → Dockerized
  FastAPI), reachable at the URL above.
- **Qwen is called live** via Alibaba Cloud Model Studio (DashScope) — provable
  with the smoke endpoint.
- No secrets are exposed anywhere in the repo or the proof responses.

## 5. Primary proof files

The primary deployment-proof file is:

[`backend/app/alibaba_cloud_proof.py`](../backend/app/alibaba_cloud_proof.py)

It proves the host/runtime, secret-free credential state, Alibaba ECS/RDS/DashScope
service map, and safe/non-claims.

The actual Qwen / DashScope API call implementation lives in:

[`backend/app/qwen_overlay.py`](../backend/app/qwen_overlay.py)
