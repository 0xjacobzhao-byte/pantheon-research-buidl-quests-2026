# Strategy Stack — Frameworks, Not Prompts

Pantheon's strategy layer is a library of **versioned investment frameworks**.
Each framework encodes what matters in a domain, the conditions that invalidate a
view, and the risk constraints that govern exposure. This document gives a
public-safe overview; full thresholds, weights, and version history remain in the
private production repository and can be reviewed by judges under temporary
access.

> **Design principle:** a framework must be able to *refuse to conclude*. When
> data is missing or a hard stop is hit, the correct output is "no view," not a
> confident guess.

---

## Cross-asset framework map

| Domain | Core method | Primary output |
|---|---|---|
| Global Macro | Tiered indicators (liquidity, real yields, credit, volatility, cycle) → regime classification | Regime, hard stops, exposure guidance |
| US / CN / HK / SG Equities | Stage-gated evaluation, kill-fast screening, moat & cash-engine, valuation triangulation, macro permission | Company verdict, sizing, risk clusters |
| Narrative | Scarcity, lifecycle stage, reflexivity, liquidity gate | Capped-sizing, asymmetric-payoff calls |
| Technical Analysis | State-first: regime, normalized features, dynamic weights, synthesis | TA state, execution & portfolio risk budget |
| Bitcoin | Long-cycle bottom model + primary daily framework + short-horizon risk radar | Horizon-reconciled stance |
| Ethereum | Multi-quadrant valuation (settlement/security, monetary utility, network effect, revenue floor) | Valuation stance with kill switches |
| DeFi | Protocol risk scoring, organic-yield analysis, liquidity & exit, counterparty | Verdict: eligible / watch / avoid / data-gap |
| Fixed Income · FX · Commodities | Macro, valuation, positioning, structure, execution layers | Cross-asset allocation & carry views |
| Prediction Markets (where applicable) | Event probability, liquidity, and payoff structure | Asymmetric event exposure |

---

## Selected framework architectures

### Global Macro
A tiered indicator system spanning liquidity, real yields, credit, volatility,
and cycle. Indicators roll up into a regime classification that carries explicit
hard stops and exposure guidance, so every downstream engine inherits a
consistent macro permission rather than re-deriving one.

### Equities (stage-gated)
A funnel: kill-fast screening removes disqualified names early; survivors pass
through moat and cash-engine analysis, valuation triangulation, macro permission,
position sizing, portfolio risk clusters, and ongoing monitoring with
post-mortems. The gate structure means weak candidates fail cheaply and capital
concentrates on names that clear every stage.

### Narrative
Tracks scarcity, lifecycle stage, and reflexivity behind a liquidity gate.
Sizing is capped and payoff-asymmetric by design — narrative exposure is treated
as optionality, not conviction.

### Technical Analysis (state-first)
Market regime and normalized indicator features feed dynamic weights and a
synthesis step. Execution risk and the portfolio risk budget are kept distinct
from the signal itself, so a strong signal never overrides risk limits.

### Bitcoin (multi-horizon)
A long-cycle bottom model, a primary daily framework, and a short-horizon risk
radar operate together with explicit conflict resolution when the horizons
disagree — the framework states which horizon governs, rather than averaging.

### Ethereum (multi-quadrant)
Valuation across settlement/security, monetary utility, network effect, and
revenue floor, weighted by regime, with kill switches that suspend a view when a
quadrant breaks.

### DeFi (protocol & yield risk)
Protocol risk scoring, organic-yield analysis, liquidity and exit mechanics, and
counterparty/centralization checks resolve to an explicit verdict: eligible,
watch, avoid, or data-gap. "Data-gap" is a first-class outcome, not a silent
omission.

### FICC (Fixed Income · FX · Commodities)
Layered analysis — macro, valuation, positioning, structure, and execution — that
produces cross-asset allocation and carry views consistent with the macro regime.

---

## What stays private

Full formulas, thresholds, indicator weights, framework version numbers, and
production strategy implementations are **not** published here. They remain in
the private production repository. This document describes *architecture and
method*, which is sufficient to evaluate rigor without exposing proprietary IP.
