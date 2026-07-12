"""SQLite-backed canonical data store (offline, public-safe).

Implements the production-shaped provenance primitives:

- idempotent ingest keyed on a stable ``content_hash`` (wall-clock excluded)
- an append-only ``canonical_observation_versions`` vintage history with a
  monotonic ``revision_sequence``
- content/version hashing over sorted-key canonical JSON
- a mutable CURRENT ``canonical_observations`` row all readers use

The database is an in-memory SQLite instance seeded from bundled JSON, so the
demo is deterministic and self-contained.
"""

from __future__ import annotations

import hashlib
import json
import sqlite3
from typing import Any, Optional

from .models import CANONICAL_QUALITY_STATES


def _canonical_json(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, ensure_ascii=False, default=str)


def _sha256(text: str) -> str:
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


# Fields hashed for an external provider record (wall-clock excluded).
_PROVIDER_HASH_FIELDS = (
    "provider", "provider_family", "market", "ticker", "instrument_id",
    "source_url", "as_of", "currency", "normalized_payload", "dq_state",
    "coverage_state",
)

# Fields hashed for a canonical observation version (capture time excluded).
_VERSION_HASH_FIELDS = (
    "value", "unit", "source", "quality_state", "verified_by", "verified_at",
    "source_vintage",
)


class DataPlatformStore:
    def __init__(self) -> None:
        self.conn = sqlite3.connect(":memory:")
        self.conn.row_factory = sqlite3.Row
        self._init_schema()

    # ------------------------------------------------------------------
    # Schema
    # ------------------------------------------------------------------

    def _init_schema(self) -> None:
        cur = self.conn.cursor()
        cur.executescript(
            """
            CREATE TABLE ingest_runs (
                id INTEGER PRIMARY KEY,
                job_name TEXT, started_at TEXT, finished_at TEXT, status TEXT,
                metrics_ingested INTEGER, series_fetched INTEGER, duration_ms INTEGER,
                errors_json TEXT
            );
            CREATE TABLE provider_health (
                provider TEXT PRIMARY KEY,
                last_success_at TEXT, last_failure_at TEXT, last_error_msg TEXT,
                consecutive_failures INTEGER, daily_calls_used INTEGER,
                daily_calls_limit INTEGER, avg_latency_ms INTEGER, status TEXT
            );
            CREATE TABLE external_provider_records (
                id INTEGER PRIMARY KEY,
                provider TEXT, provider_family TEXT, market TEXT, ticker TEXT,
                instrument_id TEXT, source_url TEXT, retrieved_at TEXT, as_of TEXT,
                currency TEXT, normalized_payload_json TEXT, dq_state TEXT,
                coverage_state TEXT, content_hash TEXT
            );
            CREATE UNIQUE INDEX uq_epr_content_hash
                ON external_provider_records(content_hash)
                WHERE content_hash IS NOT NULL;
            CREATE TABLE canonical_observations (
                id INTEGER PRIMARY KEY,
                domain TEXT, metric_id TEXT, instrument_id TEXT, as_of_date TEXT,
                value REAL, unit TEXT, source TEXT, ingested_at TEXT,
                quality_state TEXT, verified_by TEXT, verified_at TEXT,
                revision_sequence INTEGER, content_hash TEXT
            );
            CREATE UNIQUE INDEX uq_canonical_obs
                ON canonical_observations(domain, metric_id, instrument_id, as_of_date);
            CREATE TABLE canonical_observation_versions (
                id INTEGER PRIMARY KEY,
                canonical_observation_id INTEGER, domain TEXT, metric_id TEXT,
                instrument_id TEXT, as_of_date TEXT, value REAL, unit TEXT,
                source TEXT, ingested_at TEXT, vintage_at TEXT, revision_sequence INTEGER,
                quality_state TEXT, source_vintage TEXT, version_hash TEXT
            );
            CREATE TABLE derived_snapshots (
                id INTEGER PRIMARY KEY,
                snapshot_type TEXT, as_of_date TEXT, payload_json TEXT,
                created_at TEXT, ingest_run_id INTEGER, evidence_hash TEXT,
                consumed_observation_ids_json TEXT
            );
            CREATE TABLE product_snapshots (
                id INTEGER PRIMARY KEY,
                product TEXT, version TEXT, as_of_date TEXT, payload_json TEXT,
                created_at TEXT, ingest_run_id INTEGER, evidence_hash TEXT,
                derived_snapshot_id INTEGER
            );
            CREATE TABLE llm_consumers (
                id INTEGER PRIMARY KEY,
                evidence_hash TEXT, provider TEXT, model TEXT, ticker TEXT,
                overlay_ref TEXT, prompt_version TEXT
            );
            """
        )
        self.conn.commit()

    # ------------------------------------------------------------------
    # Hashing
    # ------------------------------------------------------------------

    def content_hash_for_provider_record(self, row: dict) -> str:
        material = {f: row.get(f) for f in _PROVIDER_HASH_FIELDS}
        return _sha256(_canonical_json(material))

    def version_hash_for_observation(self, row: dict) -> str:
        material = {f: row.get(f) for f in _VERSION_HASH_FIELDS}
        return _sha256(_canonical_json(material))

    # ------------------------------------------------------------------
    # Ingest (idempotent)
    # ------------------------------------------------------------------

    def upsert_provider_record(self, row: dict) -> tuple[int, bool]:
        """Idempotent insert keyed on content_hash. Returns (id, inserted)."""
        ch = self.content_hash_for_provider_record(row)
        cur = self.conn.cursor()
        existing = cur.execute(
            "SELECT id FROM external_provider_records WHERE content_hash = ?", (ch,)
        ).fetchone()
        if existing:
            # Same datum — refresh volatile fetch fields in place, no new row.
            cur.execute(
                "UPDATE external_provider_records SET retrieved_at = ? WHERE id = ?",
                (row.get("retrieved_at"), existing["id"]),
            )
            self.conn.commit()
            return existing["id"], False
        cur.execute(
            """INSERT INTO external_provider_records
               (provider, provider_family, market, ticker, instrument_id, source_url,
                retrieved_at, as_of, currency, normalized_payload_json, dq_state,
                coverage_state, content_hash)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (
                row.get("provider"), row.get("provider_family"), row.get("market"),
                row.get("ticker"), row.get("instrument_id"), row.get("source_url"),
                row.get("retrieved_at"), row.get("as_of"), row.get("currency"),
                _canonical_json(row.get("normalized_payload", {})), row.get("dq_state", "OK"),
                row.get("coverage_state", "FULL"), ch,
            ),
        )
        self.conn.commit()
        return cur.lastrowid, True

    def upsert_observation(self, row: dict, record_version: bool = True) -> tuple[int, bool]:
        """Upsert the CURRENT canonical row + append a vintage version if changed.

        Fail-closed on an invalid quality_state (raises ValueError), never a
        silent downgrade of a MANUAL_VERIFIED row on a routine re-write.
        """
        qs = row.get("quality_state", "UNKNOWN")
        if qs not in CANONICAL_QUALITY_STATES:
            raise ValueError(f"Invalid quality_state: {qs}")

        cur = self.conn.cursor()
        key = (row["domain"], row["metric_id"], row.get("instrument_id"), row["as_of_date"])
        existing = cur.execute(
            """SELECT * FROM canonical_observations
               WHERE domain=? AND metric_id=? AND ifnull(instrument_id,'')=ifnull(?,'')
                 AND as_of_date=?""",
            key,
        ).fetchone()

        version_material = {
            "value": row["value"], "unit": row["unit"], "source": row["source"],
            "quality_state": qs, "verified_by": row.get("verified_by"),
            "verified_at": row.get("verified_at"), "source_vintage": row.get("source_vintage"),
        }
        vhash = self.version_hash_for_observation(version_material)

        if existing is None:
            cur.execute(
                """INSERT INTO canonical_observations
                   (domain, metric_id, instrument_id, as_of_date, value, unit, source,
                    ingested_at, quality_state, verified_by, verified_at,
                    revision_sequence, content_hash)
                   VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (
                    row["domain"], row["metric_id"], row.get("instrument_id"),
                    row["as_of_date"], row["value"], row["unit"], row["source"],
                    row["ingested_at"], qs, row.get("verified_by"), row.get("verified_at"),
                    1, vhash,
                ),
            )
            obs_id = cur.lastrowid
            inserted = True
            new_seq = 1
        else:
            obs_id = existing["id"]
            if existing["content_hash"] == vhash:
                # Identical datum — idempotent no-op.
                self.conn.commit()
                return obs_id, False
            new_seq = existing["revision_sequence"] + 1
            cur.execute(
                """UPDATE canonical_observations
                   SET value=?, unit=?, source=?, ingested_at=?, quality_state=?,
                       verified_by=?, verified_at=?, revision_sequence=?, content_hash=?
                   WHERE id=?""",
                (
                    row["value"], row["unit"], row["source"], row["ingested_at"], qs,
                    row.get("verified_by"), row.get("verified_at"), new_seq, vhash, obs_id,
                ),
            )
            inserted = False

        if record_version:
            self._append_version(obs_id, row, qs, new_seq, vhash)
        self.conn.commit()
        return obs_id, inserted

    def _append_version(self, obs_id: int, row: dict, qs: str, seq: int, vhash: str) -> Optional[int]:
        cur = self.conn.cursor()
        latest = cur.execute(
            """SELECT version_hash FROM canonical_observation_versions
               WHERE canonical_observation_id=? ORDER BY revision_sequence DESC LIMIT 1""",
            (obs_id,),
        ).fetchone()
        if latest and latest["version_hash"] == vhash:
            return None  # idempotent — no spurious version
        cur.execute(
            """INSERT INTO canonical_observation_versions
               (canonical_observation_id, domain, metric_id, instrument_id, as_of_date,
                value, unit, source, ingested_at, vintage_at, revision_sequence,
                quality_state, source_vintage, version_hash)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (
                obs_id, row["domain"], row["metric_id"], row.get("instrument_id"),
                row["as_of_date"], row["value"], row["unit"], row["source"],
                row["ingested_at"], row.get("vintage_at", row["ingested_at"]), seq,
                qs, row.get("source_vintage"), vhash,
            ),
        )
        return cur.lastrowid

    # ------------------------------------------------------------------
    # Simple inserts for derived / product / runs / health / consumers
    # ------------------------------------------------------------------

    def insert_ingest_run(self, row: dict) -> int:
        cur = self.conn.cursor()
        cur.execute(
            """INSERT INTO ingest_runs
               (id, job_name, started_at, finished_at, status, metrics_ingested,
                series_fetched, duration_ms, errors_json)
               VALUES (?,?,?,?,?,?,?,?,?)""",
            (
                row.get("id"), row["job_name"], row["started_at"], row.get("finished_at"),
                row["status"], row.get("metrics_ingested", 0), row.get("series_fetched", 0),
                row.get("duration_ms"), _canonical_json(row.get("errors", [])),
            ),
        )
        self.conn.commit()
        return cur.lastrowid

    def upsert_provider_health(self, row: dict) -> None:
        cur = self.conn.cursor()
        cur.execute(
            """INSERT OR REPLACE INTO provider_health
               (provider, last_success_at, last_failure_at, last_error_msg,
                consecutive_failures, daily_calls_used, daily_calls_limit,
                avg_latency_ms, status)
               VALUES (?,?,?,?,?,?,?,?,?)""",
            (
                row["provider"], row.get("last_success_at"), row.get("last_failure_at"),
                row.get("last_error_msg"), row.get("consecutive_failures", 0),
                row.get("daily_calls_used", 0), row.get("daily_calls_limit"),
                row.get("avg_latency_ms"), row.get("status", "healthy"),
            ),
        )
        self.conn.commit()

    def insert_derived_snapshot(self, row: dict) -> int:
        cur = self.conn.cursor()
        cur.execute(
            """INSERT INTO derived_snapshots
               (id, snapshot_type, as_of_date, payload_json, created_at, ingest_run_id,
                evidence_hash, consumed_observation_ids_json)
               VALUES (?,?,?,?,?,?,?,?)""",
            (
                row.get("id"), row["snapshot_type"], row["as_of_date"],
                _canonical_json(row.get("payload", {})), row["created_at"],
                row.get("ingest_run_id"), row.get("evidence_hash"),
                _canonical_json(row.get("consumed_observation_ids", [])),
            ),
        )
        self.conn.commit()
        return cur.lastrowid

    def insert_product_snapshot(self, row: dict) -> int:
        cur = self.conn.cursor()
        cur.execute(
            """INSERT INTO product_snapshots
               (id, product, version, as_of_date, payload_json, created_at,
                ingest_run_id, evidence_hash, derived_snapshot_id)
               VALUES (?,?,?,?,?,?,?,?,?)""",
            (
                row.get("id"), row["product"], row.get("version", "1.0"), row["as_of_date"],
                _canonical_json(row.get("payload", {})), row["created_at"],
                row.get("ingest_run_id"), row.get("evidence_hash"),
                row.get("derived_snapshot_id"),
            ),
        )
        self.conn.commit()
        return cur.lastrowid

    def insert_llm_consumer(self, row: dict) -> int:
        cur = self.conn.cursor()
        cur.execute(
            """INSERT INTO llm_consumers
               (evidence_hash, provider, model, ticker, overlay_ref, prompt_version)
               VALUES (?,?,?,?,?,?)""",
            (
                row["evidence_hash"], row["provider"], row.get("model"), row.get("ticker"),
                row.get("overlay_ref"), row.get("prompt_version"),
            ),
        )
        self.conn.commit()
        return cur.lastrowid

    # ------------------------------------------------------------------
    # Reads
    # ------------------------------------------------------------------

    def _rows(self, sql: str, params: tuple = ()) -> list[dict]:
        return [dict(r) for r in self.conn.execute(sql, params).fetchall()]

    def ingest_runs(self) -> list[dict]:
        return self._rows("SELECT * FROM ingest_runs ORDER BY id")

    def provider_health(self) -> list[dict]:
        return self._rows("SELECT * FROM provider_health ORDER BY provider")

    def observations(self, domain: Optional[str] = None) -> list[dict]:
        if domain:
            return self._rows(
                "SELECT * FROM canonical_observations WHERE domain=? ORDER BY id", (domain,)
            )
        return self._rows("SELECT * FROM canonical_observations ORDER BY id")

    def observation(self, obs_id: int) -> Optional[dict]:
        rows = self._rows("SELECT * FROM canonical_observations WHERE id=?", (obs_id,))
        return rows[0] if rows else None

    def observation_versions(self, obs_id: int) -> list[dict]:
        return self._rows(
            "SELECT * FROM canonical_observation_versions WHERE canonical_observation_id=? "
            "ORDER BY revision_sequence",
            (obs_id,),
        )

    def derived_snapshots(self) -> list[dict]:
        return self._rows("SELECT * FROM derived_snapshots ORDER BY id")

    def product_snapshots(self) -> list[dict]:
        return self._rows("SELECT * FROM product_snapshots ORDER BY id")

    def llm_consumers(self, evidence_hash: Optional[str] = None) -> list[dict]:
        if evidence_hash:
            return self._rows(
                "SELECT * FROM llm_consumers WHERE evidence_hash=?", (evidence_hash,)
            )
        return self._rows("SELECT * FROM llm_consumers")
