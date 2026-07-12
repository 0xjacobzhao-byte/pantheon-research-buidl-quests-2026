# Multilingual Research Workflow

> Sanitized skeleton of Pantheon Research's bilingual research workflow.
> No proprietary prompt library is included. This document illustrates *why*
> Qwen via Alibaba Cloud Model Studio / DashScope is a natural fit for
> Chinese-language equity context, and shows the shape of the prompt/evidence
> structure without disclosing production prompts.

## Why Qwen for Chinese-Language Equity Context

Pantheon Research covers equities across US, China (A-share), Hong Kong, and
Singapore markets. A significant portion of the evidence — filings, analyst
reports, management commentary, regulatory announcements — is in Chinese
(Mandarin / Cantonese) or bilingual (CN/EN).

**Qwen via Alibaba Cloud Model Studio / DashScope** is purpose-built for this:

| Advantage | Detail |
|-----------|--------|
| Chinese-native | Qwen models are trained with strong Chinese-language corpora; they understand A-share filings, HKEX announcements, and CSRC regulatory language natively. |
| Bilingual fluency | Qwen handles code-switching between English and Chinese naturally — essential when evidence packs mix EN metrics with CN qualitative notes. |
| Structured output | OpenAI-compatible API mode produces JSON-structured overlays that slot into the same comparison pipeline as DeepSeek. |
| DashScope infrastructure | Alibaba Cloud's DashScope API provides low-latency, OpenAI-compatible endpoints from the ap-southeast-1 region. |

DeepSeek is used as the independent second provider for the dual-model overlay.
Both models receive the **same evidence pack** and produce the **same structured
fields** (business_quality, moat, pricing_power, capital_allocation, red_flags,
confidence, missing_evidence), enabling apples-to-apples agreement/divergence
scoring.

## US English Prompt Skeleton (Sanitized)

The production prompt template sends the evidence pack as system context and
asks the model to produce a structured JSON assessment. The skeleton below is
sanitized — it shows the *shape* without disclosing the proprietary prompt
library.

```
System:
You are a qualitative equity research analyst. Given the structured evidence
pack below, produce a JSON assessment with these fields:
- business_quality (string): assessment of business quality
- moat (string): assessment of competitive moat
- pricing_power (string): assessment of pricing power
- capital_allocation (string): assessment of management & capital allocation
- red_flags (string): identified red flags & risks
- confidence (float 0-1): your confidence in this assessment
- missing_evidence (list[string]): evidence gaps you identified

Rules:
- Base your assessment ONLY on the evidence provided.
- If evidence is insufficient for a field, say so explicitly.
- Do not fabricate data or make investment recommendations.
- Return valid JSON only.

User:
Evidence pack for {TICKER}:
{evidence_json}
```

## CN/HK Bilingual Evidence Note Skeleton (Sanitized)

For Chinese-listed equities (A-shares, HK stocks), evidence packs may include
bilingual annotations. The skeleton below shows the shape:

```json
{
  "ticker": "0700.HK",
  "company_name": "Tencent Holdings / 腾讯控股",
  "exchange": "HKEX",
  "evidence_notes": [
    {
      "field": "regulatory_risk",
      "en": "Post-2021 regulatory overhang; gaming license renewals stable",
      "cn": "2021年后监管压力持续；游戏版照续期稳定",
      "source": "public_filings",
      "as_of": "2026-06-30"
    },
    {
      "field": "wechat_ecosystem",
      "en": "WeChat mini-program GMV growth (illustrative)",
      "cn": "微信小程序GMV增长 (示例)",
      "source": "earnings_call",
      "as_of": "2026-03-31"
    }
  ]
}
```

The dual-LLM overlay processes these bilingual notes natively. Qwen's
Chinese-language understanding is particularly strong for:

- **A-share filings** (年报/半年报): financial statement notes, risk factors
- **HKEX announcements** (公告): regulatory disclosures in traditional Chinese
- **Management commentary**: earnings call transcripts with code-switching
- **CSRC / SAFE regulatory language**: policy impact assessments

## Evidence Pack Structure (Language-Agnostic)

The evidence pack is language-agnostic at the API level — both Qwen and DeepSeek
receive the same JSON structure. Language-specific content (Chinese text,
bilingual annotations) is carried in the `summary` and `evidence_notes` fields.

```
evidence pack
├── ticker, company_name, exchange, sector, industry (EN)
├── quantitative metrics: PE, PB, ROIC, FCF, margins (numeric)
├── summary: business description (EN or bilingual)
└── evidence_notes[]: per-field bilingual annotations (optional)
    ├── field (EN key)
    ├── en: English note
    ├── cn: Chinese note (when applicable)
    └── source, as_of
```

## What Is Not Included

- **No proprietary prompt library.** Production prompt templates, few-shot
  examples, and fine-tuned system instructions are in the private repo.
- **No raw provider pipelines.** The data ingestion, normalization, and
  bilingual annotation pipeline is proprietary.
- **No private datasets.** All evidence in this public repo is bundled sample
  JSON, redacted traces, or publicly available financial data.
- **No production universe.** The 312-ticker Qwen coverage and 1,331 DeepSeek
  baseline are reported as facts; the underlying data stays private.

## Related Documentation

- [Qwen Integration](qwen_integration.md)
- [Qwen Coverage Report](qwen_coverage_report.md)
- [Architecture](architecture.md)
- [Data Safety](data_safety.md)
- [Safe Claims & Non-Claims](safe_claims.md)
