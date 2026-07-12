/**
 * BtcCurrentPosture — the resolved cross-layer posture with its reasons. This
 * is a context read-out, not a trade instruction.
 */

const OUTCOME_COLORS: Record<string, string> = {
  risk_on: "#16a34a",
  accumulate: "#16a34a",
  neutral: "#f59e0b",
  caution: "#f59e0b",
  risk_off: "#dc2626",
  defensive: "#dc2626",
  de_risk: "#dc2626",
};

function outcomeColor(outcome: string): string {
  return OUTCOME_COLORS[outcome?.toLowerCase()] ?? "#3b82f6";
}

export default function BtcCurrentPosture({
  outcome,
  reasons,
  note,
  asOf,
}: {
  outcome: string;
  reasons: string[];
  note: string;
  asOf?: string;
}) {
  return (
    <div className="btc-posture" data-testid="btc-current-posture">
      <div className="bp-head">
        <span className="bp-label">Resolved posture</span>
        <span
          className="badge"
          style={{ background: outcomeColor(outcome) }}
        >
          {outcome}
        </span>
        {asOf && <span className="bp-asof">{asOf}</span>}
      </div>
      {reasons.length > 0 && (
        <ul className="bp-reasons">
          {reasons.map((r, i) => (
            <li key={i}>{r}</li>
          ))}
        </ul>
      )}
      {note && <p className="bp-note">{note}</p>}
    </div>
  );
}
