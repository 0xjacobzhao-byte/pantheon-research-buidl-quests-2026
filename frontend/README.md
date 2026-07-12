# Frontend — Pantheon Research Qwen Hackathon

Vite + React + TypeScript frontend that renders dual-LLM equity qualitative overlays side-by-side with agreement scoring, tone classification, and divergence detection.

## Running

```bash
npm install
npm run dev
```

The dev server runs on http://localhost:5173 and proxies API requests to http://localhost:8000.

## Build

```bash
npm run build
```

## Features

- Ticker selector (MA, NVDA) with sample data
- Four-layer architecture display (Strategy → Information → Signal → Trading)
- Tech stack and Alibaba Cloud integration panels
- Qwen + DeepSeek dual-model workflow diagram
- Side-by-side Qwen Cloud vs DeepSeek comparison
- Assessment fields: business_quality, moat, pricing_power, capital_allocation, red_flags, confidence, missing_evidence
- Agreement score, tone badges, divergence detection, evidence gaps
- Status badges (SUCCESS, BLOCKED_BY_MISSING_CREDENTIAL, API_ERROR, OFFLINE_SAMPLE)
- Human review required flag
- Safety statement: LLMs do not execute trades; human remains portfolio manager
