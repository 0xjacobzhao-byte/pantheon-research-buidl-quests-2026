# Judge Evidence Guide

**Pantheon Research — BUIDL_QUESTS 2026.** A reproducible verification path,
ordered so the product — not any single cloud or model provider — is the
identity under inspection.

> Pantheon is not presenting a feature checklist. It is presenting a governed
> path from investment methodology to data, signal, validation, commercial
> research products, and eventually controlled execution — see
> [`docs/commercial_model.md`](commercial_model.md) and [`docs/roadmap.md`](roadmap.md).
> The public repository is a sanitized review slice; the complete production
> system and proprietary strategy documentation remain private and can be made
> available to judges under temporary read-only access.

## 1. Product scope

Pantheon Research is an institutional-grade cross-asset research command
center: structured evidence, deterministic frameworks, and a five-model LLM
research layer (production), reduced here to a sanitized, judge-runnable
public slice. See [README → Executive Summary](../README.md#executive-summary)
and [README → Repository Access and Judge Review](../README.md#repository-access-and-judge-review).

## 2. Architecture

[`docs/architecture.md`](architecture.md) is the textual source of truth for
the high-level diagram (data sources → data platform → research engines →
deterministic + LLM layer → deployment footprint → signal layer → trading
layer), reproduced at the top of the [README](../README.md#architecture).

## 3. Evidence packs

Every evidence pack is committed to a `sha256` content hash before any model
sees it, so a stored comparison can be verified against an unmodified pack.

| What to verify | File |
|---|---|
| Evidence pack + provenance hashing | [`backend/app/evidence_pack.py`](../backend/app/evidence_pack.py) |
| Pydantic evidence/comparison models | [`backend/app/models.py`](../backend/app/models.py) |

## 4. Deterministic vs. LLM separation

The deterministic framework layer (scores, signals, evidence hashing) is
implemented independently of the LLM overlay layer — the LLM interprets
governed evidence, it does not generate the underlying scores. See
[README → Deterministic Research Meets Multi-Model AI](../README.md#deterministic-research-meets-multi-model-ai)
and [`docs/llm_research_layer.md`](llm_research_layer.md).

## 5. Five-model production coverage

Production Pantheon Research runs a five-model LLM research layer: **Claude,
ChatGPT, Gemini, DeepSeek, and Qwen**. This public repository does not bundle
all five as independently runnable integrations — see the next section for
exactly what is runnable here.

## 6. Public Qwen + DeepSeek implementation

The runnable public slice is the dual-LLM equity qualitative overlay: Qwen
(Alibaba Cloud DashScope) and DeepSeek independently assess the same evidence
pack.

| What to verify | File |
|---|---|
| Qwen / DashScope API call implementation | [`backend/app/qwen_overlay.py`](../backend/app/qwen_overlay.py) |
| DeepSeek API call implementation | [`backend/app/deepseek_overlay.py`](../backend/app/deepseek_overlay.py) |
| Dual-model comparison engine (agreement, divergence, tone) | [`backend/app/comparison.py`](../backend/app/comparison.py) |
| Fail-closed LLM handling | [`tests/test_qwen_fail_closed.py`](../backend/tests/test_qwen_fail_closed.py) |

**Default mode is offline** — no API key required; bundled samples serve the
demo end-to-end.

## 7. Data governance

| What to verify | File |
|---|---|
| Research-Ops / data-quality governance | [`backend/app/data_quality.py`](../backend/app/data_quality.py) |
| Module snapshot grid (per-module `data_state`) | [`backend/app/sample_modules.py`](../backend/app/sample_modules.py) |
| Provider health snapshot (secret-free) | [`backend/app/provider_health.py`](../backend/app/provider_health.py) |

## 8. Multi-cloud deployment evidence

Pantheon Research has been deployed and validated across **Vercel + Railway**
(core production), **Google Cloud** (Cloud Run + Gemini integration), and
**Alibaba Cloud** (ECS + DashScope/Qwen). The Alibaba deployment is the one
with a public, secret-free live proof endpoint:

```bash
curl -s http://8.222.191.152/api/proof/alibaba-cloud | jq
```

| What to verify | File |
|---|---|
| Deployment proof (host, services, secrets) | [`backend/app/alibaba_cloud_proof.py`](../backend/app/alibaba_cloud_proof.py) |
| Precise database claim (no overclaiming) | [`docs/live_proof.md`](live_proof.md) · [`docs/alibaba_deployment_parity.md`](alibaba_deployment_parity.md) |

**Non-claim:** these deployments demonstrate cloud portability and provider
integration — not automatic multi-cloud failover, and not identical
full-database replication. `database.production_data_migrated=false`,
`mirror_state=partial_selected_mirror`.

## 9. Tests and smoke

```bash
# Local offline demo — no secrets needed
docker compose up --build
./scripts/judge_smoke.sh

# Backend tests
cd backend && python -m pytest             # 84 tests

# Frontend tests + build
cd frontend && npm test -- --run && npm run build   # 9 tests

# Secret scan (should be clean)
grep -RInE "(sk-|AKIA|DASHSCOPE_API_KEY=|DEEPSEEK_API_KEY=|DATABASE_URL=postgres|x-admin-token|BEGIN PRIVATE KEY|github_pat_|ghp_)" . \
  --exclude-dir=.git --exclude-dir=node_modules --exclude-dir=.venv || true
```

## 10. Full production review (private repository)

The public slice is sufficient to verify Pantheon's mechanism and governance.
For the full production codebase and research documentation — proprietary
frameworks, provider integrations, operational infrastructure, and production
assets — the private repository
[`0xjacobzhao-byte/Pantheon-Research`](https://github.com/0xjacobzhao-byte/Pantheon-Research)
is available to BUIDL_QUESTS judges under **temporary read-only access upon
request**. A normal anonymous visitor cannot open it; this boundary is
deliberate IP and operational-security governance.

## 11. Non-claims (explicitly NOT asserted)

1. **Not claiming live paid five-model calls in this public repository** — the public five-model cockpit compares all five providers over **cached/bundled** outputs (offline, no live paid call); only Qwen + DeepSeek are live-capable. Live paid five-model inference remains private production.
2. **Not claiming automatic multi-cloud failover or identical full-database replication** across Vercel+Railway / Google Cloud / Alibaba Cloud.
3. **Alibaba RDS is NOT a full production database clone** — it is a selected evidence mirror (`mirror_state=partial_selected_mirror`).
4. **Not claiming autonomous trading or model-generated alpha.** LLMs never execute trades.
5. **Not exposing private production strategy code.**
6. **This public repository is a sanitized vertical slice**, not the full private production system.

---

## Reference material

| | |
|---|---|
| Live product | https://pantheon-research.com |
| Public code | https://github.com/0xjacobzhao-byte/pantheon-research-buidl-quests-2026 |
| Alibaba deployment (supporting evidence) | http://8.222.191.152 |
| Proof bundle (machine-readable) | [`data/judge_proof_bundle.json`](../data/judge_proof_bundle.json) |
| Prior Qwen Cloud technical demo/deck | [`docs/assets/README.md`](assets/README.md#prior-technical-evidence-not-the-current-buidl_quests-presentation) — historical reference, not this submission's media |

### Qwen coverage snapshot (public-slice supporting detail)

| Metric | Value |
|--------|-------|
| Qwen comparison-capable coverage | 312 tickers |
| Healthy comparisons | 312 / 312 |
| DeepSeek baseline universe | 1,331 |
| Markets | US 117 / CN 69 / HK 103 / SG 23 |
| Full-universe parity | not pursued; low-liquidity tail intentionally excluded |

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
