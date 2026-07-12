import type { LlmComparison } from "../../api";

/**
 * MissingEvidencePanel — surfaces the evidence gaps each model reported,
 * plus the shared gaps common to every comparable model.
 */

export default function MissingEvidencePanel({
  missing,
}: {
  missing: LlmComparison["missing_evidence"];
}) {
  const perProvider = Object.entries(missing.per_provider);
  return (
    <div className="missing-evidence" data-testid="missing-evidence-panel">
      {missing.shared_missing_evidence.length > 0 && (
        <div className="me-shared">
          <h4>Shared missing evidence</h4>
          <ul>
            {missing.shared_missing_evidence.map((m, i) => (
              <li key={i}>{m}</li>
            ))}
          </ul>
        </div>
      )}
      <div className="me-per-provider">
        {perProvider.map(([provider, gaps]) => (
          <div key={provider} className="me-provider">
            <span className="me-provider-name">{provider}</span>
            {gaps.length === 0 ? (
              <span className="model-none">No gaps reported</span>
            ) : (
              <ul>
                {gaps.map((g, i) => (
                  <li key={i}>{g}</li>
                ))}
              </ul>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
