import type { OutcomeModule } from "../../api";

/**
 * OutcomeMaturityTimeline — per-module outcome maturity with the sample
 * pipeline stages. Performance fields are always null / "n/a — <reason>";
 * never a fabricated number.
 */

export default function OutcomeMaturityTimeline({
  modules,
}: {
  modules: OutcomeModule[];
}) {
  return (
    <div className="outcome-timeline" data-testid="outcome-maturity-timeline">
      {modules.map((m) => (
        <div key={m.module} className="ot-module" data-testid={`outcome-${m.module}`}>
          <div className="ot-head">
            <h4>{m.module}</h4>
            <span
              className="badge"
              style={{
                background: m.warming_up ? "var(--warning)" : "var(--surface2)",
              }}
            >
              {m.outcome_maturity}
            </span>
          </div>
          <div className="ot-stages">
            {m.sample_timeline.map((s, i) => (
              <div key={i} className="ot-stage">
                <span className="ot-stage-count">{s.count}</span>
                <span className="ot-stage-name">{s.stage}</span>
              </div>
            ))}
          </div>
          <div className="ot-perf">
            <span className="ot-perf-label">Performance</span>
            <div className="ot-perf-fields">
              <span>hit_rate: null</span>
              <span>avg_return_pct: null</span>
              <span>sharpe: null</span>
              <span>max_drawdown_pct: null</span>
            </div>
            <p className="ot-perf-reason">n/a — {m.performance.reason}</p>
          </div>
        </div>
      ))}
    </div>
  );
}
