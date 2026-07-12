import type { LineageConsumer } from "../../api";

/**
 * EvidenceConsumersPanel — the downstream LLM overlays that consumed this
 * evidence hash. Proves every model read the same governed evidence pack.
 */

export default function EvidenceConsumersPanel({
  consumers,
}: {
  consumers: LineageConsumer[];
}) {
  return (
    <div className="evidence-consumers" data-testid="evidence-consumers-panel">
      {consumers.length === 0 ? (
        <p className="empty">No LLM consumers recorded.</p>
      ) : (
        <div className="ec-grid">
          {consumers.map((c, i) => (
            <div key={i} className="ec-card">
              <div className="ec-head">
                <strong>{c.provider}</strong>
                <span className="badge" style={{ background: "var(--surface2)" }}>
                  {c.ticker}
                </span>
              </div>
              <div className="ec-model">{c.model}</div>
              <div className="ec-meta">
                <span>prompt {c.prompt_version}</span>
                <code className="oc-hash">{c.overlay_ref}</code>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
