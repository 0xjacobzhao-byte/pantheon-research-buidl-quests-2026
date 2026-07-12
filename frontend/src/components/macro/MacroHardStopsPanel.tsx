/**
 * MacroHardStopsPanel — shows whether fail-closed hard stops are active and
 * which specific stops have triggered.
 */

export default function MacroHardStopsPanel({
  active,
  triggered,
  anomalyFlags,
}: {
  active: boolean;
  triggered: string[];
  anomalyFlags: string[];
}) {
  return (
    <div
      className={`macro-hardstops ${active ? "gated" : "cleared"}`}
      data-testid="macro-hardstops-panel"
    >
      <div className="mh-head">
        <span className="mh-label">Hard stops</span>
        <span
          className="badge"
          style={{ background: active ? "var(--error)" : "var(--success)" }}
        >
          {active ? "ACTIVE" : "clear"}
        </span>
      </div>
      {triggered.length > 0 ? (
        <ul className="mh-list">
          {triggered.map((t, i) => (
            <li key={i}>{t}</li>
          ))}
        </ul>
      ) : (
        <p className="model-none">No hard stops triggered</p>
      )}
      {anomalyFlags.length > 0 && (
        <div className="mh-anomalies">
          <span className="mh-label">Anomaly flags</span>
          <div className="mh-flags">
            {anomalyFlags.map((f, i) => (
              <span key={i} className="badge" style={{ background: "var(--warning)" }}>
                {f}
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
