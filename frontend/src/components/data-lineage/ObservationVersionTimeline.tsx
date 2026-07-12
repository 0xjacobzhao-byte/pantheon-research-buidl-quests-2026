import type { DpVersion } from "../../api";

/**
 * ObservationVersionTimeline — bitemporal revision history for a single
 * canonical observation. Each version is content-hashed and vintage-stamped
 * so revisions never silently overwrite prior truth.
 */

export default function ObservationVersionTimeline({
  observationId,
  versions,
}: {
  observationId: number | null;
  versions: DpVersion[];
}) {
  if (versions.length === 0) {
    return <p className="empty">No version history available.</p>;
  }
  return (
    <div className="version-timeline" data-testid="observation-version-timeline">
      {observationId != null && (
        <p className="meta">Observation #{observationId}</p>
      )}
      {versions.map((v) => (
        <div key={v.id} className="vt-version">
          <div className="vt-version-marker">
            <span className="vt-dot" style={{ background: "var(--accent)" }} />
          </div>
          <div className="vt-version-body">
            <div className="vt-version-head">
              <span className="vt-rev">rev {v.revision_sequence}</span>
              <span className="badge" style={{ background: "var(--surface2)" }}>
                {v.quality_state}
              </span>
            </div>
            <div className="vt-version-row">
              <span>
                {v.value} {v.unit}
              </span>
              <span className="vt-source">{v.source}</span>
            </div>
            <div className="vt-version-meta">
              <span>vintage {v.source_vintage}</span>
              <code className="oc-hash">{v.version_hash.slice(0, 18)}…</code>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}
