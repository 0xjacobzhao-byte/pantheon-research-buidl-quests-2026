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

> The public **five-model cached cockpit** and **Research Ops / validation
> console** are now merged to `main` and are judge-runnable offline — see
> [`docs/five_model_llm_cockpit.md`](five_model_llm_cockpit.md) and
> [`docs/research_ops_validation.md`](research_ops_validation.md). They compare
> Claude, ChatGPT, Gemini, DeepSeek and Qwen over a hash-committed evidence pack
> with **no live paid call**. Live five-model paid calls remain private
> production; the Qwen + DeepSeek overlay below is the live-capable public path.

---

## Five developed LLM research modules

| Model | Role in Pantheon | Governance boundary |
|---|---|---|
| Claude | Qualitative overlay & risk reasoning (public cached cockpit) | Reads governed evidence; never trades |
| ChatGPT | Qualitative overlay & comparison (public cached cockpit) | Reads governed evidence; never trades |
| Gemini | Qualitative overlay (Google Cloud integration; public cached cockpit) | Reads governed evidence; never trades |
| DeepSeek | Qualitative overlay (public cached cockpit + live-capable overlay) | Reads governed evidence; never trades |
| Qwen | Qualitative overlay (Alibaba DashScope; public cached cockpit + live-capable overlay) | Reads governed evidence; never trades |

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

The open-source repository ships a **runnable five-model cached cockpit** (all
five providers compared over one hash-committed evidence pack, offline with no
live paid call) **plus** the live-capable Qwen + DeepSeek overlay:

| What to verify | File |
|---|---|
| Five-model cached cockpit | [`backend/app/llm_cockpit.py`](../backend/app/llm_cockpit.py) · [`backend/app/llm_five_model_comparison.py`](../backend/app/llm_five_model_comparison.py) |
| Provider registry / schema / cache | [`backend/app/llm_registry.py`](../backend/app/llm_registry.py) · [`backend/app/llm_schema.py`](../backend/app/llm_schema.py) · [`backend/app/llm_cached_store.py`](../backend/app/llm_cached_store.py) |
| Live-capable Qwen / DeepSeek overlays | [`backend/app/qwen_overlay.py`](../backend/app/qwen_overlay.py) · [`backend/app/deepseek_overlay.py`](../backend/app/deepseek_overlay.py) |
| Cross-model comparison engine | [`backend/app/comparison.py`](../backend/app/comparison.py) |
| Fail-closed handling (tests) | [`backend/tests/test_qwen_fail_closed.py`](../backend/tests/test_qwen_fail_closed.py) |

The public cockpit runs over **bundled/cached** model outputs — it declares no
winner and makes no live paid model call. **Live** five-model paid calls remain
in the private production repository; the public repo demonstrates the mechanism,
governance, and offline comparison, not live paid multi-provider inference.
