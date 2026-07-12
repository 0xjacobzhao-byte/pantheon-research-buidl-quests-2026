import { useEffect, useState } from "react";
import {
  fetchMacroRiskBudget,
  fetchMacroHistory,
  fetchMacroScenarios,
  type MacroRiskBudget,
  type MacroHistoryData,
  type MacroScenariosData,
} from "../../api";
import MacroHardStopsPanel from "./MacroHardStopsPanel";
import MacroExposurePanel from "./MacroExposurePanel";
import MacroRegimeHistory from "./MacroRegimeHistory";

/**
 * MacroRiskContextPanel — page container for the macro risk budget. Shows the
 * current regime, confirmed regime, score, exposure cap, freshness, hard stops
 * and hysteresis, a regime history timeline, and the four fail-closed scenarios
 * (valid / hard-stop / stale / missing).
 */

function fmtFreshness(f: any): string {
  if (f == null) return "n/a";
  if (typeof f === "string") return f;
  if (typeof f === "object") {
    if (typeof f.state === "string") return f.state;
    if (typeof f.label === "string") return f.label;
    return JSON.stringify(f);
  }
  return String(f);
}

export default function MacroRiskContextPanel() {
  const [budget, setBudget] = useState<MacroRiskBudget | null>(null);
  const [history, setHistory] = useState<MacroHistoryData | null>(null);
  const [scenarios, setScenarios] = useState<MacroScenariosData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let active = true;
    Promise.all([
      fetchMacroRiskBudget(),
      fetchMacroHistory(),
      fetchMacroScenarios(),
    ])
      .then(([b, h, s]) => {
        if (!active) return;
        setBudget(b);
        setHistory(h);
        setScenarios(s);
      })
      .catch((e) => active && setError(e instanceof Error ? e.message : "Failed to load"))
      .finally(() => active && setLoading(false));
    return () => {
      active = false;
    };
  }, []);

  if (loading) {
    return (
      <div data-testid="view-macro" className="view">
        <p className="empty">Loading macro risk budget…</p>
      </div>
    );
  }
  if (error || !budget) {
    return (
      <div data-testid="view-macro" className="view">
        <div className="error-box">{error ?? "No macro data."}</div>
      </div>
    );
  }

  return (
    <div data-testid="view-macro" className="view">
      <section className="card">
        <h2>Macro Risk Budget</h2>
        <p className="section-lead">
          A fail-closed risk governor. Regime confirmation uses hysteresis; stale
          or missing inputs collapse exposure rather than guessing.
        </p>
        <div className="comparison-summary">
          <div className="summary-item">
            <span className="label">Raw regime</span>
            <span className="value">{budget.regime}</span>
          </div>
          <div className="summary-item">
            <span className="label">Confirmed regime</span>
            <span className="value">{budget.confirmed_regime}</span>
          </div>
          <div className="summary-item">
            <span className="label">Freshness</span>
            <span className="value">{fmtFreshness(budget.freshness)}</span>
          </div>
          <div className="summary-item">
            <span className="label">As of</span>
            <span className="value">{budget.as_of}</span>
          </div>
        </div>

        <MacroExposurePanel
          score={budget.score}
          exposureCapPct={budget.exposure_cap_pct}
          finalExposure={budget.final_exposure}
        />

        <MacroHardStopsPanel
          active={budget.hard_stops_active}
          triggered={budget.hard_stops_triggered}
          anomalyFlags={budget.anomaly_flags}
        />

        {budget.hysteresis && (
          <div className="macro-hysteresis">
            <h3>Regime Hysteresis</h3>
            <p className="hyst-reason">{budget.hysteresis.reason}</p>
            <div className="hyst-grid">
              <span>Raw: {budget.hysteresis.raw_regime}</span>
              <span>Confirmed: {budget.hysteresis.confirmed_regime}</span>
              <span>Pending: {budget.hysteresis.pending_regime}</span>
              <span>
                Observations: {budget.hysteresis.observations_seen}/
                {budget.hysteresis.observations_required}
              </span>
              <span>
                Transition pending:{" "}
                {budget.hysteresis.transition_pending ? "yes" : "no"}
              </span>
            </div>
          </div>
        )}

        {budget.degraded_reason && (
          <p className="macro-degraded">Degraded: {budget.degraded_reason}</p>
        )}
      </section>

      {history && (
        <section className="card">
          <h2>Regime History</h2>
          <p className="section-lead">Exposure cap and confirmed regime over time.</p>
          <MacroRegimeHistory history={history.history} />
        </section>
      )}

      {scenarios && (
        <section className="card">
          <h2>Fail-Closed Scenarios</h2>
          <p className="section-lead">
            The same governor across four input conditions — proving valid,
            hard-stop, stale and missing inputs each resolve safely.
          </p>
          <div className="scenario-grid">
            {scenarios.scenarios.map((s) => (
              <div key={s.id} className="scenario-card" data-testid={`scenario-${s.id}`}>
                <div className="scenario-head">
                  <h4>{s.label}</h4>
                  <span
                    className="badge"
                    style={{
                      background: s.risk_budget.hard_stops_active
                        ? "var(--error)"
                        : "var(--surface2)",
                    }}
                  >
                    {s.risk_budget.confirmed_regime}
                  </span>
                </div>
                <div className="scenario-meta">
                  <span>Cap: {s.risk_budget.exposure_cap_pct}%</span>
                  <span>Score: {s.risk_budget.score.toFixed(2)}</span>
                  <span>
                    Hard stops:{" "}
                    {s.risk_budget.hard_stops_active ? "active" : "clear"}
                  </span>
                </div>
                {s.risk_budget.degraded_reason && (
                  <p className="scenario-degraded">
                    {s.risk_budget.degraded_reason}
                  </p>
                )}
              </div>
            ))}
          </div>
        </section>
      )}
    </div>
  );
}
