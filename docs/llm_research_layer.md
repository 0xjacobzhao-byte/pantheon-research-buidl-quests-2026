# Deterministic + Multi-Model AI Layer

Pantheon draws a strict boundary between **deterministic computation** and **LLM
interpretation**. The deterministic layer is the record of truth; the LLM layer
is the interpreter. They are not interchangeable, and the LLM never generates a
position.

---

## The boundary

**Deterministic engines own:**
normalized inputs · scores · market regimes · valuation outputs · hard stops ·
signal candidates · risk constraints · reproducibility · audit trails.

**LLM research modules own:**
qualitative interpretation · contradiction detection · evidence-gap discovery ·
cross-model comparison · source-backed narratives · confidence assessment · risk
explanation · bilingual research where applicable.

The deterministic layer is reproducible and auditable by construction; the LLM
layer adds breadth and contextual depth. Keeping them separate means an LLM can
be wrong without corrupting the score of record.

---

## Two Research Lanes

Every research output belongs to exactly one of two lanes, and the two are never
allowed to blur.

### Evidence-backed

Grounded in source packs, with:

- provenance and an explicit evidence tier;
- content-hash / source references;
- data-quality and freshness state.

A conclusion is only *eligible* to be presented as evidence-backed when those
requirements pass. If provenance, tier, or freshness fails, the conclusion cannot
be served as sourced fact.

### Model-inferred / AI-prior

Explicit model reasoning that goes beyond the available evidence. It is:

- **always labelled** as inference;
- **never** presented as sourced fact;
- unable to mutate a deterministic rating;
- unable to execute;
- able only to raise a **verification task** or a **human-review requirement**.

> An AI prior can never masquerade as source-backed evidence.

This separation is enforced as governance, not convention: the evidence tier and
label travel with the output, so a downstream surface (dashboard, alert, API)
always knows whether it is showing sourced research or labelled inference.

---

## Research governance in practice

| Governance capability | Pantheon implementation |
|---|---|
| Evidence provenance | Source packs and evidence artifacts bound to hashes / references |
| Fail-closed states | Missing, stale, blocked, parse, and provider errors stay visible |
| Schema validation | Structured model output validated before it is served |
| Multi-model comparison | Agreement and divergence surfaced provider by provider |
| Evidence hierarchy | Source-backed research separated from AI-prior inference |
| Human review | Disagreement and missing evidence create review requirements |
| Research Ops | Coverage, provider health, maturity, and audit surfaces |
| Signal separation | AI research does not directly execute trades |

---

## Product availability vs. validation maturity

A research surface can be **live** while its **forward-return validation** is
still immature. Pantheon tracks these separately:

- **product availability** — is the surface shipped and usable;
- **framework maturity** — is the methodology frozen and versioned;
- **validation maturity** — are there enough forward samples and attribution;
- **public-performance eligibility** — may any performance claim be made.

BTC is among the more mature validation tracks; equity forward samples are still
accumulating. Reconstructed results and live forward results are kept separate,
and **validation-only data is not a public alpha claim.** No performance numbers
are published until they are real and verifiable.

> When the public five-model cockpit and Research Ops console are merged to the
> public `main`, this document will reference their exact public files and routes.
> Until then, the five-model layer is described as private production capability
> and the public runnable evidence is the Qwen + DeepSeek slice below.

---

## Five developed LLM research modules

| Model | Role in Pantheon | Governance boundary |
|---|---|---|
| Claude | Qualitative overlay & risk reasoning | Reads governed evidence; never trades |
| ChatGPT | Qualitative overlay & comparison | Reads governed evidence; never trades |
| Gemini | Qualitative overlay (Google Cloud integration) | Reads governed evidence; never trades |
| DeepSeek | Qualitative overlay (public runnable slice) | Reads governed evidence; never trades |
| Qwen | Qualitative overlay (Alibaba DashScope; public runnable slice) | Reads governed evidence; never trades |

Roles above are stated at the level verified by code and documentation. No
comparative model-performance claims are made.

---

## Evidence-first overlay workflow

```text
Structured Evidence Pack
        ↓
Provider-Specific Prompt / Context      (Source Pack → Prompt Builder)
        ↓
Schema-Validated Model Output           (Schema Validator)
        ↓
Cross-Model Comparison                  (Overlay Comparison)
        ↓
Agreement / Disagreement / Missing Evidence
        ↓
Human Review
```

Pantheon builds a **structured evidence pack first**, then asks each model to
interpret that governed evidence — it does not ask an LLM for an unsupported
market opinion. Model output is schema-validated before it is trusted, and the
comparison step surfaces where models agree, where they diverge, and what
evidence is missing.

---

## Explicit, fail-closed provider states

The public slice makes provider state honest and inspectable:

| Situation | State |
|---|---|
| Live model call succeeded | `SUCCESS` |
| Bundled sample used (default offline demo) | `OFFLINE_SAMPLE` |
| Live mode without a credential | `BLOCKED_BY_MISSING_CREDENTIAL` |
| Upstream/API failure | `API_ERROR` |
| Non-JSON / malformed model output | `PARSE_ERROR` |

The comparison headline `data_state` (`LIVE_DUAL` / `OFFLINE_SAMPLE` / `MIXED` /
`PARTIAL` / `BLOCKED`) never reports a hollow success: if a provider fails, the
comparison is marked `NOT_COMPARABLE` and human review is required rather than a
fabricated agreement score.

---

## Public vs. production

The open-source repository ships a **runnable Qwen + DeepSeek vertical slice** of
this layer:

| What to verify | File |
|---|---|
| Qwen / DashScope overlay | [`backend/app/qwen_overlay.py`](../backend/app/qwen_overlay.py) |
| DeepSeek overlay | [`backend/app/deepseek_overlay.py`](../backend/app/deepseek_overlay.py) |
| Cross-model comparison engine | [`backend/app/comparison.py`](../backend/app/comparison.py) |
| Fail-closed handling (tests) | [`backend/tests/test_qwen_fail_closed.py`](../backend/tests/test_qwen_fail_closed.py) |

The full five-model production layer (Claude, ChatGPT, Gemini, DeepSeek, Qwen)
lives in the private production repository. This distinction is intentional: the
public repo demonstrates the mechanism and governance; it does not bundle all
five providers as independently runnable integrations.
