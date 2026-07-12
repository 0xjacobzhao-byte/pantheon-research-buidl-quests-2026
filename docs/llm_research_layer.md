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
