import type { BtcConflict } from "../../api";

/**
 * BtcConflictResolutionPanel — worked examples where the three layers disagree,
 * showing the resolved outcome vs. the expected outcome and whether they match.
 */

export default function BtcConflictResolutionPanel({
  examples,
}: {
  examples: BtcConflict[];
}) {
  return (
    <div className="btc-conflicts" data-testid="btc-conflict-panel">
      {examples.map((ex) => (
        <div key={ex.id} className="bc-example" data-testid={`btc-conflict-${ex.id}`}>
          <div className="bc-head">
            <h4>{ex.title}</h4>
            <span
              className="badge"
              style={{
                background: ex.matches_expected ? "var(--success)" : "var(--error)",
              }}
            >
              {ex.matches_expected ? "matches expected" : "mismatch"}
            </span>
          </div>
          <div className="bc-outcomes">
            <span>
              Resolved: <strong>{ex.resolved_outcome}</strong>
            </span>
            <span>
              Expected: <strong>{ex.expected_outcome}</strong>
            </span>
          </div>
          <div className="bc-inputs">
            <span>L1: {String(ex.inputs.l1)}</span>
            <span>L2: {String(ex.inputs.l2)}</span>
            <span>L3: {String(ex.inputs.l3)}</span>
            <span>Macro: {String(ex.inputs.macro)}</span>
          </div>
          {ex.reasons.length > 0 && (
            <ul className="bc-reasons">
              {ex.reasons.map((r, i) => (
                <li key={i}>{r}</li>
              ))}
            </ul>
          )}
        </div>
      ))}
    </div>
  );
}
