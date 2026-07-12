import type { ModelOverlay } from "../../api";

/**
 * ModelRiskComparison — one column per model showing confidence, evidence
 * coverage, factor verdicts and red flags. Fail-closed overlays surface the
 * error message instead of a fabricated verdict.
 */

function coverageLabel(cov: any): string {
  if (cov == null) return "n/a";
  if (typeof cov === "number") return `${(cov * 100).toFixed(0)}%`;
  if (typeof cov === "string") return cov;
  if (typeof cov === "object") {
    if (typeof cov.ratio === "number") return `${(cov.ratio * 100).toFixed(0)}%`;
    if (typeof cov.pct === "number") return `${cov.pct}%`;
    if (typeof cov.label === "string") return cov.label;
  }
  return String(cov);
}

const FACTORS: { key: keyof ModelOverlay; label: string }[] = [
  { key: "business_quality", label: "Business Quality" },
  { key: "moat", label: "Moat" },
  { key: "pricing_power", label: "Pricing Power" },
  { key: "management_capital_allocation", label: "Capital Allocation" },
  { key: "valuation_view", label: "Valuation" },
];

export default function ModelRiskComparison({
  overlays,
}: {
  overlays: ModelOverlay[];
}) {
  return (
    <div className="model-risk-grid" data-testid="model-risk-comparison">
      {overlays.map((o) => {
        const failed = !!o.error_message;
        return (
          <div
            key={o.provider}
            className="model-card"
            data-testid={`model-card-${o.provider}`}
          >
            <div className="model-card-head">
              <h4>{o.provider}</h4>
              <span className="badge" style={{ background: "var(--surface2)" }}>
                {o.data_state}
              </span>
            </div>
            <div className="model-card-model">{o.model}</div>

            {failed ? (
              <p className="model-failclosed">Fail-closed: {o.error_message}</p>
            ) : (
              <>
                <div className="model-metric-row">
                  <span>
                    Confidence:{" "}
                    <strong>
                      {o.confidence != null ? o.confidence.toFixed(2) : "n/a"}
                    </strong>
                  </span>
                  <span>Coverage: {coverageLabel(o.evidence_coverage)}</span>
                </div>

                <dl className="model-factors">
                  {FACTORS.map(({ key, label }) => {
                    const val = o[key] as { verdict: string } | null;
                    return (
                      <div key={String(key)}>
                        <dt>{label}</dt>
                        <dd>{val?.verdict ?? "—"}</dd>
                      </div>
                    );
                  })}
                </dl>

                <div className="model-redflags">
                  <span className="model-redflags-label">Red flags</span>
                  {o.red_flags.length === 0 ? (
                    <p className="model-none">None recorded</p>
                  ) : (
                    <ul>
                      {o.red_flags.map((rf, i) => (
                        <li key={i}>{rf}</li>
                      ))}
                    </ul>
                  )}
                </div>

                {o.human_review_required && (
                  <p className="model-review-flag">Human review flagged</p>
                )}
              </>
            )}
          </div>
        );
      })}
    </div>
  );
}
