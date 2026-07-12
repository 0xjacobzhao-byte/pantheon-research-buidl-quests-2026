# Assets

Visual and captured-artifact assets for the README and judging docs.

## Captured (committed)

- **[`architecture_high_level.png`](architecture_high_level.png)** — Pantheon Research
  high-level architecture diagram showing all 7 layers: external data sources,
  data platform, strategy engines, deterministic + LLM layer, information layer,
  signal layer, and trading layer. Includes Alibaba Cloud stack integration and
  Qwen via DashScope dual-model overlay workflow.
- **[`alibaba_live_proof.json`](alibaba_live_proof.json)** — a real, unmodified
  capture of the live Alibaba Cloud proof endpoint
  (`GET http://8.222.191.152/api/proof/alibaba-cloud`). Booleans only, no
  secrets. Confirms Alibaba ECS host + live Qwen (`qwen3.7-plus`) + a configured
  database. Reproduce:
  ```bash
  curl -s http://8.222.191.152/api/proof/alibaba-cloud | jq
  ```

## Screenshots (TODO — capture from the live/local demo)

Screenshots were not auto-captured in the build environment (headless browser
unavailable). To add them, run the demo locally (`docker compose up --build`)
or open the live product, capture the frames below, and drop the PNGs here —
the README will reference them once present.

| File | What to capture | Source |
|------|----------------|--------|
| `demo_overlay_comparison.png` | OverlayComparisonPanel on NVDA: Qwen vs DeepSeek cards, agreement score, divergences, human-review gate | `http://localhost:5173` → select NVDA → Run Comparison, or `https://pantheon-research.com` Ticker Profile → Qwen vs DeepSeek |
| `module_snapshot_grid.png` | ModuleSnapshotGrid (System Scope): Macro / TA / FICC / Equity / Qwen-vs-DeepSeek / Data Quality cards with per-module `data_state` | `/api/modules` rendered at the top of the demo cockpit |
| `data_quality_panel.png` | DataQualityPanel (Research-Ops): provider config, coverage, per-ticker data_state table | Data Quality tab in frontend |
| `alibaba_live_proof.png` | Browser view of the live proof JSON | `http://8.222.191.152/api/proof/alibaba-cloud` in browser |
| `judge_quickstart.png` | Terminal running `./scripts/judge_smoke.sh` all green | Local terminal after `docker compose up --build` |

**Image rules:**
- PNG or JPG, ideally < 500 KB each
- No secrets, admin tokens, DB URLs, API keys, or browser auth headers
- Crop to product UI / proof JSON only

Until PNGs are added, the **demo video** is the canonical visual walkthrough:
https://www.youtube.com/watch?v=68lceOACLKo
