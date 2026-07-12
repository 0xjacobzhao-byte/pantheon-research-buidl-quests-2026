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

This exact PNG is supplied by Jacob and is committed at
`pantheon_research_high_level_architecture.png` (1672×941, ~1.6 MB). The README
and `docs/architecture.md` reference it with a live `<img>` embed. **No
substitute or Claude-generated architecture image is used** — a previous pass
generated a stand-in diagram and local-demo screenshots; those were rejected and
removed.

## GitHub Social Preview asset

`pantheon_research_social_preview.png` is the GitHub **Social Preview** image
for this repository (the card shown when the repo is linked on social media,
Slack, etc.). It is a **separate asset from the approved architecture
diagram** above — the architecture PNG is never resized, edited, or reused as
the social card.

- **Dimensions:** exactly 1280×640 (GitHub's required social-preview size).
- **Size:** ~420 KB, under the 1 MB limit.
- **Format:** PNG.
- **Content:** title, subtitle, the Strategy → Information → Signal →
  Controlled Execution flow, the "Five-Model AI · Governed Data · Multi-Cloud"
  capability line, and a `BUIDL_QUESTS 2026` footer badge — dark navy/charcoal
  background with restrained blue/green accents, consistent with the approved
  architecture image's visual language. No screenshots, no QR code, no
  sponsor/provider logos, no metrics, and no investor-return, alpha, or
  autonomous-trading claims.
- **Derived from:** the Pantheon visual identity (same color palette and
  typographic tone as the approved architecture diagram), authored as a
  standalone composition rather than a crop or edit of that file.
- This image is **not embedded in the README**; it is only used as GitHub's
  repository Social Preview via *Settings → General → Social preview*.

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
