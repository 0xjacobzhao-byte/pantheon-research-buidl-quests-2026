import type { ValidationTimelineData } from "../api";

/**
 * ValidationTimeline — signal lifecycle tracker showing the path from
 * signal capture through forward validation. No alpha claim before maturation.
 */

const STATUS_COLORS: Record<string, string> = {
  COMPLETE: "#16a34a",
  AWAITING: "#f59e0b",
  PENDING: "#6b7280",
};

export default function ValidationTimeline({ data }: { data: ValidationTimelineData }) {
  return (
    <div className="validation-timeline" data-testid="validation-timeline">
      <h3>Validation Timeline</h3>
      <p className="vt-stance">{data.stance}</p>

      <div className="vt-stages">
        {data.stages.map((s) => (
          <div key={s.stage} className="vt-stage">
            <div className="vt-stage-marker">
              <span
                className="vt-dot"
                style={{ backgroundColor: STATUS_COLORS[s.status] ?? "#6b7280" }}
              />
              {s.stage < data.stages.length && <div className="vt-line" />}
            </div>
            <div className="vt-stage-content">
              <div className="vt-stage-header">
                <span className="vt-stage-num">Stage {s.stage}</span>
                <span
                  className="badge"
                  style={{ backgroundColor: STATUS_COLORS[s.status] ?? "#6b7280" }}
                >
                  {s.status}
                </span>
              </div>
              <h4 className="vt-stage-name">{s.name}</h4>
              <p className="vt-stage-desc">{s.description}</p>
              <code className="vt-stage-evidence">{s.evidence}</code>
            </div>
          </div>
        ))}
      </div>

      {/* Non-claims */}
      <div className="vt-non-claims">
        <h4>Non-claims</h4>
        <ul>
          {data.non_claims.map((nc, i) => (
            <li key={i}>{nc}</li>
          ))}
        </ul>
      </div>

      {/* Illustrative summary */}
      <div className="vt-summary">
        <h4>Illustrative Demo Summary</h4>
        <p className="vt-summary-note">{data.illustrative_demo_summary.note}</p>
        <div className="vt-summary-grid">
          <span>Signals captured: {data.illustrative_demo_summary.signals_captured}</span>
          <span>Evidence hashed: {data.illustrative_demo_summary.evidence_hashed}</span>
          <span>Models recorded: {data.illustrative_demo_summary.models_recorded}</span>
          <span>Awaiting forward window: {data.illustrative_demo_summary.awaiting_forward_window}</span>
          <span>Matured & scored: {data.illustrative_demo_summary.matured_and_scored}</span>
          <span className="vt-perf-claim">
            Performance claim: {data.illustrative_demo_summary.performance_claim}
          </span>
        </div>
      </div>
    </div>
  );
}
