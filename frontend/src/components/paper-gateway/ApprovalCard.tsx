import type { ApprovalCardData } from "../../api";

/**
 * ApprovalCard — the human approval surface for a paper intent. An LLM can
 * never approve; only a human operator can, and only when live is disabled.
 */

function fmtNotional(n: any): string {
  if (n == null) return "n/a";
  if (typeof n === "number") return `$${n.toLocaleString()}`;
  return String(n);
}

export default function ApprovalCard({
  card,
  onApprove,
  onReject,
  busy,
}: {
  card: ApprovalCardData;
  onApprove: () => void;
  onReject: () => void;
  busy: boolean;
}) {
  const canApprove = card.risk_gate_passed && card.provenance_complete && !busy;
  return (
    <div className="approval-card" data-testid="approval-card">
      <div className="ac-head">
        <h3>
          {card.side.toUpperCase()} {card.ticker} · {card.quantity}
        </h3>
        <span className="ac-notional">{fmtNotional(card.notional_usd)}</span>
      </div>

      <dl className="ac-fields">
        <div>
          <dt>Validation maturity</dt>
          <dd>{card.validation_maturity}</dd>
        </div>
        <div>
          <dt>Macro risk budget</dt>
          <dd>{card.macro_risk_budget_ref}</dd>
        </div>
        <div>
          <dt>Data freshness</dt>
          <dd>{card.data_freshness_state}</dd>
        </div>
        <div>
          <dt>Kill switch</dt>
          <dd>{card.kill_switch_snapshot}</dd>
        </div>
      </dl>

      <div className="ac-gates">
        <span className="badge" style={{ background: "var(--error)" }}>
          LLM can approve: {card.llm_can_approve ? "yes" : "no"}
        </span>
        <span className="badge" style={{ background: "var(--error)" }}>
          Live enabled: {card.live_enabled ? "yes" : "no"}
        </span>
        <span className="badge" style={{ background: "var(--surface2)" }}>
          Requires human: {card.requires_human_approval ? "yes" : "no"}
        </span>
      </div>

      {card.operator_note && <p className="ac-note">{card.operator_note}</p>}

      <div className="ac-actions">
        <button
          className="run-btn"
          onClick={onApprove}
          disabled={!canApprove}
          title={
            canApprove
              ? "Approve and simulate paper fill"
              : "Blocked by risk gate / provenance"
          }
        >
          {busy ? "Working…" : "Approve + Simulate"}
        </button>
        <button className="reject-btn" onClick={onReject} disabled={busy}>
          Reject
        </button>
      </div>
    </div>
  );
}
