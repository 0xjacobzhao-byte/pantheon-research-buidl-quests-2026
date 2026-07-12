import { useEffect, useState } from "react";
import {
  fetchLlmProviders,
  fetchLlmCases,
  fetchLlmCase,
  fetchLlmComparison,
  type LlmProvidersData,
  type LlmCase,
  type LlmCaseDetail,
  type LlmComparison,
} from "../../api";
import ModelProviderStatusStrip from "./ModelProviderStatusStrip";
import FiveModelAgreementMatrix from "./FiveModelAgreementMatrix";
import ModelRiskComparison from "./ModelRiskComparison";
import MissingEvidencePanel from "./MissingEvidencePanel";

/**
 * FiveModelResearchCockpit — page container for the five-model LLM overlay.
 * Lets the operator pick a case (NVDA / MA / BTC), then shows every model's
 * verdicts, the agreement matrix, risk comparison, missing evidence, the
 * human-review summary and an explicit "no winner declared" note.
 */

export default function FiveModelResearchCockpit() {
  const [providers, setProviders] = useState<LlmProvidersData | null>(null);
  const [cases, setCases] = useState<LlmCase[]>([]);
  const [selected, setSelected] = useState<string>("");
  const [detail, setDetail] = useState<LlmCaseDetail | null>(null);
  const [comparison, setComparison] = useState<LlmComparison | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let active = true;
    setLoading(true);
    Promise.all([fetchLlmProviders(), fetchLlmCases()])
      .then(([prov, cs]) => {
        if (!active) return;
        setProviders(prov);
        setCases(cs.cases);
        setSelected(cs.cases[0]?.case_id ?? "");
      })
      .catch((e) => active && setError(e instanceof Error ? e.message : "Failed to load"))
      .finally(() => active && setLoading(false));
    return () => {
      active = false;
    };
  }, []);

  useEffect(() => {
    if (!selected) return;
    let active = true;
    setError(null);
    Promise.all([fetchLlmCase(selected), fetchLlmComparison(selected)])
      .then(([d, c]) => {
        if (!active) return;
        setDetail(d);
        setComparison(c);
      })
      .catch((e) => active && setError(e instanceof Error ? e.message : "Failed to load case"));
    return () => {
      active = false;
    };
  }, [selected]);

  if (loading) {
    return (
      <div data-testid="view-llm" className="view">
        <p className="empty">Loading five-model cockpit…</p>
      </div>
    );
  }

  return (
    <div data-testid="view-llm" className="view">
      <section className="card">
        <h2>Five-Model LLM Research Cockpit</h2>
        <p className="section-lead">
          Five independent models analyze the same hashed evidence pack. Verdicts
          are compared factor-by-factor — no model is treated as ground truth.
        </p>
        <div className="ticker-panel">
          {cases.map((c) => (
            <button
              key={c.case_id}
              className={`ticker-btn ${selected === c.case_id ? "selected" : ""}`}
              onClick={() => setSelected(c.case_id)}
            >
              {c.ticker}
            </button>
          ))}
        </div>
        {error && <div className="error-box">{error}</div>}
        {providers && (
          <div className="mp-strip-wrap">
            <ModelProviderStatusStrip
              providers={providers.providers}
              providerStates={comparison?.provider_states}
            />
          </div>
        )}
      </section>

      {detail && (
        <section className="card">
          <h2>
            Model Verdicts — {detail.case.company_name} ({detail.case.ticker})
          </h2>
          <p className="meta">
            <code className="oc-hash">{detail.case.evidence_hash.slice(0, 26)}…</code>
          </p>
          <ModelRiskComparison overlays={detail.overlays} />
        </section>
      )}

      {comparison && (
        <>
          <section className="card">
            <h2>Agreement Matrix</h2>
            <FiveModelAgreementMatrix
              matrix={comparison.agreement_matrix}
              providers={comparison.comparable_providers}
            />
          </section>

          <section className="card">
            <h2>Missing Evidence</h2>
            <MissingEvidencePanel missing={comparison.missing_evidence} />
          </section>

          <section className="card">
            <h2>Human-Review Summary</h2>
            <div
              className={`hr-summary ${
                comparison.human_review_required ? "gated" : "cleared"
              }`}
            >
              <p className="hr-status">
                Human review:{" "}
                <strong>
                  {comparison.human_review_required ? "REQUIRED" : "Not required"}
                </strong>
              </p>
              {comparison.human_review_reasons.length > 0 && (
                <ul>
                  {comparison.human_review_reasons.map((r, i) => (
                    <li key={i}>{r}</li>
                  ))}
                </ul>
              )}
              {comparison.confidence_spread != null && (
                <p className="hr-spread">
                  Confidence spread: {comparison.confidence_spread.toFixed(2)}
                </p>
              )}
            </div>
            <p className="no-winner">
              No winner declared. {comparison.note}
            </p>
          </section>
        </>
      )}
    </div>
  );
}
