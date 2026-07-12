# Security & Sanitization

How this public BUIDL_QUESTS repository is kept safe to publish and honest to
judges.

## What was copied from the public Qwen repository

This repository is a dedicated BUIDL_QUESTS adaptation of the already-public and
already-sanitized `pantheon-research-qwen-hackathon` slice. Inherited, public-safe
components include:

* `backend/` — FastAPI app: evidence pack + provenance hashing, provider overlays
  (Qwen, DeepSeek), the comparison engine, Research-Ops / data-quality, module
  snapshots, ticker profiles, validation timeline, and the secret-free
  deployment-proof endpoint.
* `frontend/` — React + TypeScript demo UI (overlay comparison, data-quality,
  module grid, provider health, mini panels).
* `data/` — sanitized sample evidence and redacted traces (labelled samples only).
* `docs/`, `scripts/`, Docker files, `.github/workflows/`, `.gitignore`,
  `LICENSE`, and dependency manifests.

Only presentation-level changes were made for BUIDL_QUESTS: repository naming,
project metadata, public links, event framing, and the judge-facing README/docs.
No new product functionality was invented.

## What remains private

The full production repository
([`0xjacobzhao-byte/Pantheon-Research`](https://github.com/0xjacobzhao-byte/Pantheon-Research))
is private and closed-source, and was **not** the source of this public
submission. It contains the full production codebase and research documentation —
proprietary frameworks and strategy logic, provider integrations, production
infrastructure, operational runbooks, and production data — none of which appear
here. This boundary is deliberate IP and operational-security governance.
**Temporary read-only access can be granted to BUIDL_QUESTS judges upon
request**; a normal anonymous visitor cannot open the private repository.

## What data samples are included

* `data/sample_equity_evidence_{ma,nvda}.json` — sanitized quantitative evidence.
* `data/sample_{qwen,deepseek}_output_{ma,nvda}.json` — bundled model samples
  (served as `OFFLINE_SAMPLE`).
* `data/redacted_traces/*` and `data/*_redacted.json` — redacted illustrative
  traces.
* `data/judge_proof_bundle.json`, `data/ticker_profiles.json` — public-safe
  demo fixtures.

## What credentials are excluded

Never included: API keys, access tokens, cookies, private keys, database
credentials, cloud service-account credentials, `.env` files, production
environment files, database dumps, user records, admin tokens, broker/trading
credentials, or proprietary provider contracts. Only `.env.example` with empty
placeholders is committed.

## Offline-demo behavior

* Default mode is **offline** — the full demo runs with **no secrets**.
* Provider overlays return `OFFLINE_SAMPLE` from bundled data; no live call is
  claimed.
* Comparison-level `data_state` (`OFFLINE_SAMPLE` / `MIXED` / `PARTIAL` /
  `BLOCKED`) never reports a hollow live result.
* Live mode is gated behind `DEMO_MODE=live` plus provider keys supplied via
  environment variables that no endpoint ever returns.

## Production / public separation

* pantheon-research.com and the Alibaba ECS deployment run the broader production
  system.
* This repository is the self-contained, offline-runnable public slice.
* The secret-free `/api/proof/alibaba-cloud` endpoint reports host/runtime and
  credential state as **booleans only**, makes no external calls, and never
  claims connectivity it did not verify.

## Secret-scan methodology

Before every push, scan the working tree (excluding `.git`, `node_modules`,
`.venv`, `dist`, and `*.example`) for high-signal patterns:

```bash
grep -rEn --binary-files=without-match \
  --exclude-dir=.git --exclude-dir=node_modules --exclude-dir=.venv \
  --exclude-dir=dist --exclude='*.example' \
  'sk-[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|LTAI[A-Za-z0-9]{12,}|-----BEGIN [A-Z ]*PRIVATE KEY-----|postgres(ql)?://[^[:space:]]+:[^[:space:]]+@|ghp_[A-Za-z0-9]{30,}|xox[baprs]-[A-Za-z0-9-]+' .

# Ensure no real .env is tracked
git ls-files | grep -E '(^|/)\.env$' && echo "FAIL" || echo "OK: no committed .env"
```

CI additionally runs the project's own checks on every push and PR to `main`.

## Financial safety boundary

* **No autonomous trade execution.** The product produces research artifacts;
  it does not place orders.
* **No performance, return, AUM, revenue, or user claims.**
* LLM outputs are informational research, **not investment advice**.
* Missing or unusable data fails closed; humans retain final judgment.

## Full public migration — what is and is not ported

The six governance modules are sanitized vertical slices. **Ported** (public-safe
shape, vocabulary, and clearly-illustrative values only): field/enum contracts,
deterministic control flow, hashing methods, fail-closed behavior, and bundled
fixtures.

**Never ported / never copied:**

* `.env`, API keys, database URLs, admin tokens, service-account JSON, Telegram
  bot tokens, broker credentials, TOTP code.
* Broker/exchange adapters, live-execution or real-order paths, live-enablement
  write paths, account configuration, personal risk limits.
* Full proprietary thresholds, strategy formulas, scoring weights, regime/gate
  multipliers, and TTL constants.
* Raw private model responses, proprietary prompts, production database dumps,
  real customer/operator identities, internal-only URLs, and real vendor payloads.
* Real performance numbers (returns, Sharpe, hit rates) — Research Ops keeps all
  performance fields `null` with an explicit reason.

**Structural safety proofs in the public repo:**

* `GET /api/paper-gateway/status` and `/live-disabled-proof` report
  `live_enabled=false`, `broker_connected=false`, `real_order_path=false`,
  `paper_only=true`, and `llm_actor_auto_executed_without_approval=0`.
* A backend test asserts the paper-gateway package imports no broker/exchange SDK
  and calls no order path.
* All bundled LLM overlay content is sanitized illustrative text, not raw model
  output; no live paid LLM call is made.
