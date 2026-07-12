import type { AuditEvent } from "../../api";

/**
 * IntentAuditTimeline — append-only, hash-chained audit trail for an intent.
 * Each event references the prior event's hash, so tampering is detectable.
 */

function detailText(detail: any): string {
  if (detail == null) return "";
  if (typeof detail === "string") return detail;
  return JSON.stringify(detail);
}

export default function IntentAuditTimeline({
  events,
}: {
  events: AuditEvent[];
}) {
  if (events.length === 0) {
    return <p className="empty">No audit events yet.</p>;
  }
  return (
    <div className="audit-timeline" data-testid="intent-audit-timeline">
      {events.map((e) => (
        <div key={e.seq} className="audit-event">
          <div className="ae-marker">
            <span className="ae-seq">{e.seq}</span>
          </div>
          <div className="ae-body">
            <div className="ae-head">
              <span className="ae-type">{e.event_type}</span>
              <span className="badge" style={{ background: "var(--surface2)" }}>
                {e.actor_type}
              </span>
              <span className="ae-actor">{e.actor_identity}</span>
            </div>
            {detailText(e.detail) && (
              <p className="ae-detail">{detailText(e.detail)}</p>
            )}
            <div className="ae-hashes">
              <span>at {e.at}</span>
              <code className="oc-hash">prev {e.prev_hash.slice(0, 14)}…</code>
              <code className="oc-hash">hash {e.event_hash.slice(0, 14)}…</code>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}
