# Assets

Visual and captured-artifact assets for the README and judging docs.

## Captured (committed)

- **[`pantheon_research_high_level_architecture_2026.png`](pantheon_research_high_level_architecture_2026.png)**
  — the current, verified high-level architecture diagram: external data
  sources, data platform, research engines, the deterministic + five-model LLM
  layer, the deployment footprint (Vercel + Railway core production, Google
  Cloud, Alibaba Cloud), the information/signal layer, and the trading roadmap.
  This is the diagram shown at the top of the [README](../../README.md#architecture);
  [`docs/architecture.md`](../architecture.md) is its textual source of truth.
- **[`product_overview.png`](product_overview.png)** — a real capture of the
  local demo (`http://localhost:5173`): the four-layer architecture strip and
  the system-scope module snapshot grid.
- **[`equity_llm_comparison.png`](equity_llm_comparison.png)** — a real capture
  of the Qwen vs DeepSeek overlay comparison panel for NVDA: agreement score,
  human-review gate, and side-by-side qualitative assessments.
- **[`research_ops_data_quality.png`](research_ops_data_quality.png)** — a real
  capture of the Research-Ops / data-quality panel: provider configuration and
  per-ticker comparison health.
- **[`architecture_high_level.png`](architecture_high_level.png)** — prior
  Qwen Cloud hackathon architecture diagram, kept for historical reference; the
  2026 diagram above supersedes it as the current source of truth.
- **[`alibaba_live_proof.json`](alibaba_live_proof.json)** — a real, unmodified
  capture of the live Alibaba Cloud proof endpoint
  (`GET http://8.222.191.152/api/proof/alibaba-cloud`). Booleans only, no
  secrets. Confirms Alibaba ECS host + live Qwen (`qwen3.7-plus`) + a configured
  database. Reproduce:
  ```bash
  curl -s http://8.222.191.152/api/proof/alibaba-cloud | jq
  ```

**Image rules:** PNG or JPG, ideally < 500 KB each; no secrets, admin tokens, DB
URLs, API keys, or browser auth headers; cropped to product UI / proof JSON
only. All three product screenshots above were captured from the local offline
demo (`docker compose up --build` → `http://localhost:5173`) with zero
credentials configured.

## Prior technical evidence (not the current BUIDL_QUESTS presentation)

A demo video and deck were recorded for an earlier Qwen Cloud hackathon
milestone. They are **not** the official BUIDL_QUESTS 2026 submission media —
listed here only as supporting technical history, not as the canonical
walkthrough for this submission:

- Prior Qwen Cloud technical demo (video) — https://www.youtube.com/watch?v=68lceOACLKo
- Prior Qwen Cloud technical deck — [Google Slides](https://docs.google.com/presentation/d/1E72ORBmaiL2QPbmL1CPBqrbSLLOsAVEnDxdo76IPJqs/edit?usp=sharing)

A BUIDL_QUESTS-specific demo video/deck can be recorded using
[`docs/demo_script.md`](../demo_script.md) and linked from the README once
available.
