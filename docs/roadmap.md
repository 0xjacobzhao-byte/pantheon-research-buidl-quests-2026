# Roadmap — From Research OS to Controlled Execution

## 1. Roadmap Principle

> Strategy first. Information second. Signal third. Execution last.

Execution is intentionally the final stage. Each phase must clear explicit
**gates** (Section 7) before the next begins. This is a governed institutional
development plan, not a feature wishlist, and it uses **phase-based sequencing —
no calendar dates** are claimed. Nothing below is presented as live unless
explicitly labeled.

## 2. Current Baseline (Phase 0)

**Status: `CURRENT / BUILT / VALIDATION`.**

- **Product:** live cross-asset web product with mobile / PWA support — Overview,
  Macro, US/CN/HK/SG Equity, BTC, ETH, DeFi, Technical Analysis, FICC, Research Ops.
- **Strategy:** versioned deterministic frameworks, the four-layer architecture,
  hard stops, fail-closed states, human-controlled decisions.
- **Data:** PostgreSQL, canonical observations, snapshots, evidence artifacts,
  provider health, data-quality labels.
- **AI:** five developed LLM modules (Claude, ChatGPT, Gemini, DeepSeek, Qwen),
  structured evidence-based overlays, and model comparison.
- **Deployment:** Vercel + Railway, plus completed Google Cloud and Alibaba Cloud
  deployments.
- **Commercial:** product live; membership / payment foundations; early GTM and
  packaging.

> **Qualification:** the public repository is a sanitized runnable slice (a Qwen +
> DeepSeek comparison, evidence packs, data-quality, proof artifacts). It does
> **not** contain complete production parity with the private system.

## 3. Phase 1 — Product Hardening and Validation

**Status: `NOW / ACTIVE`.**

**Objective:** raise product, data, signal, and AI quality to a reliable,
sellable standard.

- **Product deliverables:** close frontend parity gaps; improve mobile; module
  consistency; refine Overview and information hierarchy; strengthen browser-level
  smoke tests; performance and reliability.
- **Data deliverables:** provider fallback; freshness monitoring; data-gap
  remediation; vintage / point-in-time tracking; cross-market source quality;
  provider cost control; Research Ops dashboards.
- **Strategy / validation deliverables:** expand backtests; separate reconstructed
  from live results; forward validation; outcome capture; benchmark comparison;
  attribution; confidence calibration; multiple-testing discipline (e.g. BH-FDR)
  where applicable.
- **AI deliverables:** expand five-model coverage and provider parity; improve
  source-pack quality; model-comparison diagnostics; disagreement measurement;
  cost control; bilingual / market-specific prompts; event-driven refresh.
- **Distribution deliverables:** signal history; Telegram / alert reliability;
  state-transition monitoring; alert deduplication; relevance thresholds; evidence
  links; human-review routing.
- **Execution deliverables:** none — manual only.
- **Commercial deliverables:** pricing experiments; subscription packaging;
  premium research digest; paid equity evaluation; design-partner interviews; GTM
  testing.
- **Entry criteria:** Phase 0 baseline live and inspectable.
- **Exit criteria:** stable provider health; sufficient forward samples; clear
  data-quality state; reproducible signal history; stable user workflow; pricing
  evidence; no critical security or reliability gaps.
- **Not included:** any broker connection or execution.

## 4. Phase 2 — Research-to-Execution Control Plane

**Status: `NEXT`.**

**Objective:** turn signals into an auditable, human-approved paper→broker
workflow — without autonomous execution.

- **Paper-trade harness:** every signal becomes
  `Signal → Research Ticket → Framework Sleeve → Paper Fill → P&L Journal →
  Attribution`. One sleeve per framework; paper fills; fee/slippage assumptions;
  outcome tracking; signal-to-fill linkage; weekly attribution; failure analysis;
  drawdown monitoring.
- **Broker read-only integration:** positions, balances, orders, fills,
  reconciliation — **no write permission** initially. Potential brokers (e.g.
  Interactive Brokers, Moomoo / Futu, OKX, regional brokers) are candidates, not
  committed integrations.
- **Approval-based execution:** a human approval card with single-use approval,
  expiry, provenance, macro budget, kill-switch state, risk limits, expected cost,
  and paper-vs-live comparison.
- **AI deliverables:** evidence-linked signals; human-review routing.
- **Commercial deliverables:** advisor and family-office workflow pilots; team
  plans; API pilots; white-label research reports.
- **Entry criteria:** Phase 1 exit criteria met.
- **Exit criteria:** paper attribution record; reconciliation accuracy; approval
  audit; no double execution; clear risk-rejection taxonomy; provider and broker
  reliability; compliance review.
- **Not included:** unattended or constraint-bound automatic execution.

## 5. Phase 3 — Constraint-Bound Automation

**Status: `LATER / CONDITIONAL`.** This is **constraint-bound execution**, not
"autonomous trading."

**Objective:** allow automatic execution only inside pre-approved constraints,
with full human override.

- **Required controls:** strategy-specific position caps; portfolio-level limits;
  exposure budget; macro hard stops; kill switches; validation-maturity gates;
  instrument eligibility; freshness gates; daily loss cap; drawdown cap;
  order-rate limits; liquidity checks; slippage limits; human override; full audit
  trail.
- **Execution capabilities:** staged entries; TWAP; order routing; reconciliation;
  P&L attribution; rejected-order analysis; incident response.
- **Human boundary:** large or unusual orders require human approval;
  model-generated research never bypasses deterministic gates; operators retain
  halt and override authority; automation operates only inside pre-approved
  constraints.
- **Commercial deliverables:** strategy licensing; managed workflows;
  institutional execution support; proprietary-capital experiments — only after
  validation.
- **Entry criteria:** Phase 2 exit criteria met.
- **Exit criteria:** validated source strategy; adequate sample size; stable
  forward performance; low operational error; complete audit and risk controls;
  legal / regulatory review; operator sign-off.
- **Not included:** unbounded or discretionary automated trading.

## 6. Phase 4 — Multi-Account Infrastructure

**Status: `LONG TERM`.** Not currently active.

**Objective:** research and (validated) execution across multiple accounts and
mandates.

- **Capabilities:** personal and family-office accounts; segregated strategy
  sleeves; source-level P&L; account-level risk budget; cross-account
  reconciliation; jurisdiction-aware constraints; tax and reporting integration;
  multi-currency operations; role-based permissions.
- **Institutional layer:** advisor console; team workflow; investment-committee
  review; client reporting; white-label interface; API access; custom mandates.
- **Commercial models:** annual enterprise license; per-account fee; workflow
  implementation fee; strategy licensing; managed-research service;
  performance-linked structures where legally permitted.
- **Entry criteria:** Phase 3 validated and operating reliably.
- **Not included:** any implication that this phase is active today.

## 7. Roadmap Gates

Every phase transition must clear these gates; a failed gate blocks progression.

| Gate | Question | Evidence Required | Failure Result |
|---|---|---|---|
| Data | Is the data usable? | freshness, coverage, provenance, provider health | fail closed |
| Framework | Is the methodology frozen? | versioned rules, tests, hard stops | research only |
| Validation | Does the signal have evidence? | backtest, forward sample, benchmark, attribution | no execution influence |
| Operational | Can the system run reliably? | monitoring, reconciliation, audit trail | manual only |
| Risk | Can loss be bounded? | caps, kill switches, macro budget, drawdown controls | blocked |
| Commercial | Will users pay? | pilots, retention, pricing evidence | continue research product |
| Regulatory | Is the operating model permitted? | legal review, jurisdiction, disclosures | no launch |

## 8. Critical Dependencies

Data rights and provider reliability; point-in-time history; forward-sample
maturity; model cost; cloud cost; broker API reliability; compliance and
regulatory scope; user willingness to pay; security and access control; operator
capacity.

## 9. Principal Risks

| Risk | Impact | Mitigation |
|---|---|---|
| Data contamination | Corrupts research & backtests | Point-in-time discipline; provenance; data-quality states; fail-closed governance |
| Backtest overfitting | False confidence | Reconstructed-vs-live separation; forward validation; multiple-testing discipline |
| Model drift | Degraded overlays | Schema validation; disagreement monitoring; periodic re-evaluation |
| Provider outage | Missing data / stale signals | Provider routing & fallback; freshness gates; explicit `BLOCKED` states |
| Hallucination | Unsupported narrative | Evidence-first packs; schema validation; `PARSE_ERROR` fail-closed; human review |
| Execution error | Financial loss | Approval cards; caps; kill switch; reconciliation; audit trail |
| Regulatory risk | Blocked launch | Regulatory gate; legal review before any execution |
| Premature automation | Loss + reputational damage | Validation-maturity gates; constraint-bound only after Phase 2/3 exit |
| Weak product-market fit | Stalled revenue | Stage-1 pricing experiments; design partners; workflow lock-in |
| One-founder concentration | Key-person risk | AI-assisted operation; documentation; automation; audit trails |

## 10. Success Metrics

Metric *categories* (no numerical targets are claimed until they exist in
verified documentation):

- **Product** — active usage, repeat usage, module adoption, alert engagement,
  retention.
- **Data** — provider success rate, freshness compliance, coverage, data-gap rate,
  revision transparency.
- **Research** — sample count, signal stability, benchmark-relative outcomes,
  calibration, attribution coverage.
- **AI** — schema-valid rate, evidence coverage, disagreement rate,
  missing-evidence detection, cost per completed analysis.
- **Operations** — deployment reliability, smoke-test pass rate, incident rate,
  recovery time.
- **Commercial** — paid conversion, annual commitment, expansion, API usage,
  design partners.
- **Execution** — paper-fill accuracy, reconciliation, slippage, gate-rejection
  quality, zero unauthorized execution.

## 11. Deferred Work

Full-universe coverage of low-liquidity tail assets; broad public API SLAs;
white-label billing; a public five-model runnable cockpit; and any live execution
are deferred until their gates are met.

## 12. Explicit Non-Claims

- No live autonomous trading and no unattended execution.
- No performance, return, or AUM claims.
- No calendar commitments — phases are gated by evidence, not dates.
- No claim that the public repository contains full production parity.
