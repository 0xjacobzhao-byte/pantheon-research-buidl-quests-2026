"""Append-only, hash-chained audit log.

Events are only ever appended. Each event commits the hash of the previous event
into its own hash, forming a tamper-evident chain: mutating any historical event
breaks every subsequent ``event_hash``.
"""

from __future__ import annotations

import hashlib
import json
from typing import Any, Optional

from .models import ActorType, AuditEvent


def _canonical(obj: dict[str, Any]) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), default=str)


class AuditLog:
    """In-memory append-only audit chain (offline demo)."""

    def __init__(self) -> None:
        self._events: list[AuditEvent] = []

    def _last_hash(self) -> Optional[str]:
        return self._events[-1].event_hash if self._events else None

    def append(
        self,
        intent_id: str,
        event_type: str,
        actor_type: ActorType,
        actor_identity: str,
        at: str,
        detail: str = "",
    ) -> AuditEvent:
        seq = len(self._events) + 1
        prev_hash = self._last_hash()
        body = {
            "seq": seq,
            "intent_id": intent_id,
            "event_type": event_type,
            "actor_type": actor_type.value,
            "actor_identity": actor_identity,
            "detail": detail,
            "at": at,
            "prev_hash": prev_hash,
        }
        event_hash = "sha256:" + hashlib.sha256(_canonical(body).encode("utf-8")).hexdigest()
        event = AuditEvent(**body, event_hash=event_hash)
        self._events.append(event)
        return event

    def events(self, intent_id: Optional[str] = None) -> list[AuditEvent]:
        if intent_id is None:
            return list(self._events)
        return [e for e in self._events if e.intent_id == intent_id]

    def verify_chain(self) -> bool:
        """Re-derive every hash and confirm the chain is intact (append-only)."""
        prev: Optional[str] = None
        for i, e in enumerate(self._events):
            body = {
                "seq": e.seq,
                "intent_id": e.intent_id,
                "event_type": e.event_type,
                "actor_type": e.actor_type.value,
                "actor_identity": e.actor_identity,
                "detail": e.detail,
                "at": e.at,
                "prev_hash": prev,
            }
            expected = "sha256:" + hashlib.sha256(_canonical(body).encode("utf-8")).hexdigest()
            if e.seq != i + 1 or e.prev_hash != prev or e.event_hash != expected:
                return False
            prev = e.event_hash
        return True
