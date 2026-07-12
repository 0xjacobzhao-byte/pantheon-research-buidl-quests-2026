import type { ApprovalCardData } from "../../api";

/**
 * RiskGatePanel — shows whether the pre-trade risk gate passed and enumerates
 * any rejection reasons from the taxonomy.
 */

export default function RiskGatePanel({
  card,
}: {
  card: ApprovalCardData;
}) {
  const passed = card.risk_gate_passed;
  return (
    <div
      className={`risk-gate ${passed ? "cleared" : "gated"}`}
      data-testid="risk-gate-panel"
    >
      <div className="rg-head">
        <span className="rg-label">Risk gate</span>
        <span
          className="badge"
          style={{ background: passed ? "var(--success)" : "var(--error)" }}
        >
          {passed ? "PASSED" : "BLOCKED"}
        </span>
      </div>
      <div className="rg-checks">
        <span>
          Provenance complete: {card.provenance_complete ? "yes" : "no"}
        </span>
        <span>Data freshness: {card.data_freshness_state}</span>
        <span>Kill switch: {card.kill_switch_snapshot}</span>
        <span>Validation maturity: {card.validation_maturity}</span>
      </div>
      <div className="rg-reasons">
        <span className="rg-label">Rejection reasons</span>
        {card.rejection_reasons.length === 0 ? (
          <p className="model-none">None — no policy violations</p>
        ) : (
          <ul>
            {card.rejection_reasons.map((r, i) => (
              <li key={i}>{r}</li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}
