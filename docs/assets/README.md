# Assets

Visual and captured-artifact assets for the README and judging docs.

## Approved architecture image (pending)

`docs/assets/pantheon_research_high_level_architecture.png` is the **single
approved** architecture diagram for this submission — supplied by Jacob and
intended to be the only architecture image shown in the README. It has not yet
been added to this repository (the source file was not accessible in the
environment that prepared this documentation pass). See the "Remaining actions
for Jacob" note in the relevant PR for the exact drop-in path; once the file is
added, the commented-out embed at the top of [`README.md`](../../README.md) and
in [`docs/architecture.md`](../architecture.md) can be uncommented.

**No substitute or Claude-generated architecture image is included.** A
previous presentation pass generated a stand-in diagram and several local-demo
screenshots; those were rejected and removed. This document intentionally does
not list replacement visuals.

## Historical reference (not shown in the README)

- **[`architecture_high_level.png`](architecture_high_level.png)** — prior
  Qwen Cloud hackathon architecture diagram. Superseded by the pending approved
  2026 diagram above; kept here only for historical reference and does not
  appear in the main README.
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
only.

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
