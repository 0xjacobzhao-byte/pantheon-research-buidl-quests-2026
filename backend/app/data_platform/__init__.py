"""Canonical Data Platform + Vintage Provenance (public-safe, SQLite-backed).

A sanitized reimplementation of the production data platform's provenance layer:
idempotent ingest, content hashing, append-only vintage history, and end-to-end
lineage traversal from a provider record to the LLM overlays that consume it.
"""
