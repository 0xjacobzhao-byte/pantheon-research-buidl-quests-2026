# Data Safety Policy

## Safety Statement

**LLMs do not execute trades; human remains portfolio manager.**

Pantheon Research is not an autonomous trading bot. It is a framework-first, data-governed, human-in-the-loop AI research operating system.

## What Is Excluded

This repository is a **public-safe standalone demo** for BUIDL_QUESTS 2026 (originally derived from the public Qwen Cloud Hackathon slice). The following are explicitly **NOT included**:

### Secrets & Credentials
- `.env` files (only `.env.example` with empty values)
- API keys, tokens, or secrets of any kind
- Database URLs or connection strings
- Alibaba Cloud credentials (AccessKey, SecretKey, STS tokens)
- DeepSeek API keys
- Broker credentials
- Payment secrets

### Private Data
- Real portfolio data or positions
- Trade logs or transaction history
- User data or PII
- Proprietary production workflows
- Production database dumps

### Private Infrastructure
- Production deployment scripts
- Private git history
- Internal infrastructure configuration
- Private repo contents (the production Pantheon Research repo remains private)

## What Is Included

- **Synthetic sample data** based on publicly available information about public companies (MA, NVDA)
- **Template `.env.example`** with empty placeholder values
- **Demo-mode sample LLM outputs** that simulate what the APIs would return
- **Standard open-source scaffolding** (README, LICENSE, Dockerfile, etc.)
- **Comparison fields**: `business_quality`, `moat`, `pricing_power`, `capital_allocation`, `red_flags`, `confidence`, `missing_evidence`

## Credential Loading

All credentials are loaded from environment variables — never hardcoded:

| Variable              | Purpose                          | Required for offline? |
|-----------------------|----------------------------------|------------------------|
| `DASHSCOPE_API_KEY`   | Qwen Cloud (DashScope) auth      | No                     |
| `DEEPSEEK_API_KEY`    | DeepSeek API auth               | No                     |
| `DEMO_MODE`           | `offline` (default) or `live`   | No                     |
| `QWEN_MODEL`          | Qwen model override             | No                     |
| `DEEPSEEK_MODEL`      | DeepSeek model override          | No                     |

In offline mode (default), no API keys are needed. The app uses bundled sample data in `data/`.

## Git History

This repository has a **fresh git history** — no private commit history from the production repo is carried over.

## Verification

To verify no secrets are present:

```bash
# Check for .env files
find . -name ".env" -not -path "*/node_modules/*"

# Check for common secret patterns
grep -r "sk-" . --include="*.py" --include="*.ts" --include="*.json"
grep -r "AKIA" . --include="*.py" --include="*.ts" --include="*.json"
grep -r "password" . --include="*.py" --include="*.ts" --include="*.json" -i
```

All searches should return no results (excluding `.env.example` which has empty values).

## Public Demo Repository Disclaimer

This repository contains a sanitized public hackathon demo version of Pantheon Research.

The production Pantheon Research system uses private infrastructure, private databases, provider credentials, operational runbooks, and proprietary research workflows that are not included in this repository.

No API keys, private user data, live trading credentials, production secrets, or private financial records are included.

## License

All content in this repository is licensed under Apache-2.0.
