# Assets

Visual and captured-artifact assets for the README and judging docs.

## Approved architecture image

`pantheon_research_high_level_architecture.png` is the **single approved**
architecture diagram for this submission and the only architecture image shown
in the README. It depicts the full Pantheon Research production architecture:
external data sources, the governed data platform, research engines, the
deterministic + five-model LLM layer, the information dashboard, the signal and
delivery layer, the staged trading roadmap, and the three deployment stacks.
[`docs/architecture.md`](../architecture.md) is its textual source of truth.

> **Maintainer note:** this exact PNG is supplied by Jacob and must be committed
> at `docs/assets/pantheon_research_high_level_architecture.png`. The README and
> `docs/architecture.md` already reference it with a live `<img>` embed, so it
> renders automatically once the file is present. **No substitute or
> Claude-generated architecture image is used** — a previous pass generated a
> stand-in diagram and local-demo screenshots; those were rejected and removed.

## Historical reference (not shown in the README)

- **[`architecture_high_level.png`](architecture_high_level.png)** — prior Qwen
  Cloud hackathon architecture diagram. Superseded by the approved diagram above;
  kept only for historical reference and not shown in the main README.
- **[`alibaba_live_proof.json`](alibaba_live_proof.json)** — a real, unmodified
  capture of the live Alibaba Cloud proof endpoint
  (`GET http://8.222.191.152/api/proof/alibaba-cloud`). Booleans only, no
  secrets. Reproduce:
  ```bash
  curl -s http://8.222.191.152/api/proof/alibaba-cloud | jq
  ```

**Image rules:** PNG or JPG, ideally < 500 KB each; no secrets, admin tokens, DB
URLs, API keys, or browser auth headers; cropped to product UI / proof JSON only.

## Prior technical evidence (not the current BUIDL_QUESTS presentation)

A demo video and deck were recorded for an earlier Qwen Cloud hackathon
milestone. They are **not** the official BUIDL_QUESTS 2026 submission media —
listed here only as supporting technical history:

- Prior Qwen Cloud technical demo (video) — https://www.youtube.com/watch?v=68lceOACLKo
- Prior Qwen Cloud technical deck — [Google Slides](https://docs.google.com/presentation/d/1E72ORBmaiL2QPbmL1CPBqrbSLLOsAVEnDxdo76IPJqs/edit?usp=sharing)

A BUIDL_QUESTS-specific demo video/deck can be recorded using
[`docs/demo_script.md`](../demo_script.md) and linked from the README once
available.
