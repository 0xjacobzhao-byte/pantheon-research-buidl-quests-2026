# Paper / Shadow Trading Gateway (paper-only, LIVE disabled)

A public-safe, **offline, paper-only** governance demo. It ports the production
gateway's governance layer — provenance, actor split, risk gate, human approval,
paper simulation, append-only audit — and **nothing** of its execution surface.

## LIVE disabled by construction

```
LIVE_ENABLED     = False
BROKER_CONNECTED = False
REAL_ORDER_PATH  = False
PAPER_ONLY       = True
```

There is **no broker adapter, no exchange adapter, no credential path, no TOTP,
and no real-order path** anywhere in this package. A test asserts the package
imports no broker/exchange SDK and calls no order path.

## Actor split — the LLM can propose but never execute

An LLM actor (`actor_type = llm`) can create a provenance-stamped intent, but it
can **never approve or fill** one. Only a human operator approves, and approval
unlocks **only a paper simulation**. `live-disabled-proof` reports
`llm_actor_auto_executed_without_approval = 0`: every paper fill is preceded by a
human `approval_approved` event in the audit chain.

## Flow

```
Research Verdict → Macro Risk Budget → Provenance-Stamped Intent → Risk Gate
  → Human Approval Card → Paper Fill → Append-Only Audit Timeline
```

## Provenance + audit hash

The immutable provenance stamp carries `source_module, source_verdict_ref,
validation_maturity, macro_risk_budget_ref, data_freshness_state,
kill_switch_snapshot, risk_policy_snapshot, actor_identity, actor_type,
created_by_surface, audit_hash`. The `audit_hash` is a SHA-256 over the canonical
intent-body + provenance; tampering with any committed field (e.g. quantity)
invalidates it and is caught by the gate (`audit_hash_invalid`). The audit log is
hash-chained (each event commits the previous event's hash) and append-only.

## Risk rejection taxonomy

`macro_hard_stop, macro_budget_exceeded, kill_switch_triggered,
kill_switch_feed_expired, data_hard_stale, data_missing, validation_not_ready,
provenance_missing, audit_hash_invalid, single_name_cap, asset_class_cap,
sector_cap, drawdown_cap, daily_loss_cap, daily_trade_count_cap,
insufficient_cash, market_closed, risk_policy_blocked, operator_approval_missing,
live_disabled, legacy_intent_ineligible, unknown_fail_closed`. The gate is
fail-closed: any unexpected condition maps to `unknown_fail_closed`.

## APIs

```
POST /api/paper-gateway/intent
GET  /api/paper-gateway/intent/{intent_id}
POST /api/paper-gateway/intent/{intent_id}/approve
POST /api/paper-gateway/intent/{intent_id}/reject
POST /api/paper-gateway/intent/{intent_id}/simulate
GET  /api/paper-gateway/audit
GET  /api/paper-gateway/provenance-completeness
GET  /api/paper-gateway/status
GET  /api/paper-gateway/live-disabled-proof
```

## Backend / data

`backend/app/paper_gateway/{models,provenance,risk_gate,paper_simulator,
audit_log,approval_card,service}.py`. Fixtures:
`data/paper_gateway/seed_intents.json` (a clean approve-and-fill flow plus
macro-hard-stop, validation-not-ready, single-name-cap, and operator-reject
rejections).

## Not ported

Broker/exchange adapters, credential code, TOTP, live execution, real order
code, account configuration, and personal risk limits (illustrative caps only).
