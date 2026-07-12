"""Paper / Shadow Trading Gateway (public-safe, offline, PAPER-ONLY).

This package is a sanitized vertical slice of the production trading gateway's
governance layer. It ports ONLY public-safe logic:

- immutable, provenance-stamped intents
- an actor split that structurally prevents an LLM actor from executing
- a fail-closed risk gate with a full rejection taxonomy
- a human operator approval card
- a paper-only fill simulator (never touches a broker)
- an append-only, hash-chained audit log

It deliberately contains NO broker adapter, NO exchange adapter, NO credential
code, NO TOTP, NO real-order path, and NO live-enablement write path. LIVE is
disabled by construction and cannot be turned on from this public repo.
"""
