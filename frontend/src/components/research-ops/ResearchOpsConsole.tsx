import { useEffect, useState } from "react";
import {
  fetchResearchOpsReadiness,
  fetchResearchOpsValidation,
  fetchResearchOpsOutcomes,
  fetchResearchOpsSummary,
  type ResearchOpsReadiness,
  type ResearchOpsValidation,
  type ResearchOpsOutcomes,
  type ResearchOpsSummary,
} from "../../api";
import ModuleReadinessTable from "./ModuleReadinessTable";
import ValidationPolicyPanel from "./ValidationPolicyPanel";
import OutcomeMaturityTimeline from "./OutcomeMaturityTimeline";

/**
 * ResearchOpsConsole — page container for the research operations governance
 * layer. Prominently renders the no-alpha banner and never shows a performance
 * number for immature/ineligible outcomes.
 */

export const NO_ALPHA_BANNER =
  "No alpha, return, or performance claim is made for modules without mature, eligible outcomes.";

export default function ResearchOpsConsole() {
  const [readiness, setReadiness] = useState<ResearchOpsReadiness | null>(null);
  const [validation, setValidation] = useState<ResearchOpsValidation | null>(null);
  const [outcomes, setOutcomes] = useState<ResearchOpsOutcomes | null>(null);
  const [summary, setSummary] = useState<ResearchOpsSummary | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let active = true;
    Promise.all([
      fetchResearchOpsReadiness(),
      fetchResearchOpsValidation(),
      fetchResearchOpsOutcomes(),
      fetchResearchOpsSummary(),
    ])
      .then(([r, v, o, s]) => {
        if (!active) return;
        setReadiness(r);
        setValidation(v);
        setOutcomes(o);
        setSummary(s);
      })
      .catch((e) => active && setError(e instanceof Error ? e.message : "Failed to load"))
      .finally(() => active && setLoading(false));
    return () => {
      active = false;
    };
  }, []);

  if (loading) {
    return (
      <div data-testid="view-research-ops" className="view">
        <p className="empty">Loading research-ops console…</p>
      </div>
    );
  }
  if (error) {
    return (
      <div data-testid="view-research-ops" className="view">
        <div className="error-box">{error}</div>
      </div>
    );
  }

  return (
    <div data-testid="view-research-ops" className="view">
      <section className="card">
        <h2>Research-Ops Console</h2>
        <div className="no-alpha-banner" data-testid="no-alpha-banner">
          {NO_ALPHA_BANNER}
        </div>
        {summary && (
          <div className="comparison-summary">
            <div className="summary-item">
              <span className="label">Total modules</span>
              <span className="value big">{summary.total_modules}</span>
            </div>
            <div className="summary-item">
              <span className="label">Public-perf eligible</span>
              <span className="value big">
                {summary.public_performance_eligible_count}
              </span>
            </div>
            <div className="summary-item">
              <span className="label">With public performance</span>
              <span className="value big">
                {summary.modules_with_public_performance}
              </span>
            </div>
          </div>
        )}
      </section>

      {readiness && (
        <section className="card">
          <h2>Module Readiness</h2>
          <p className="section-lead">{readiness.no_alpha_claim}</p>
          <ModuleReadinessTable modules={readiness.modules} />
        </section>
      )}

      {validation && (
        <section className="card">
          <h2>Validation Policy</h2>
          <ValidationPolicyPanel data={validation} />
        </section>
      )}

      {outcomes && (
        <section className="card">
          <h2>Outcome Maturity</h2>
          <p className="section-lead">{outcomes.performance_null_reason}</p>
          <OutcomeMaturityTimeline modules={outcomes.modules} />
        </section>
      )}
    </div>
  );
}
