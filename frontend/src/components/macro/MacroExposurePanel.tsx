/**
 * MacroExposurePanel — renders the risk score and the resulting exposure cap
 * as a simple gauge bar.
 */

function fmtExposure(fe: any): string {
  if (fe == null) return "n/a";
  if (typeof fe === "number") return `${fe}`;
  if (typeof fe === "string") return fe;
  if (typeof fe === "object") {
    if (typeof fe.pct === "number") return `${fe.pct}%`;
    if (typeof fe.label === "string") return fe.label;
  }
  return String(fe);
}

export default function MacroExposurePanel({
  score,
  exposureCapPct,
  finalExposure,
}: {
  score: number;
  exposureCapPct: number;
  finalExposure: any;
}) {
  const capClamped = Math.max(0, Math.min(100, exposureCapPct));
  return (
    <div className="macro-exposure" data-testid="macro-exposure-panel">
      <div className="me-metric">
        <span className="label">Risk score</span>
        <span className="value big">{score.toFixed(2)}</span>
      </div>
      <div className="me-gauge-wrap">
        <div className="me-gauge-head">
          <span className="label">Exposure cap</span>
          <span className="value">{exposureCapPct}%</span>
        </div>
        <div className="me-gauge">
          <div
            className="me-gauge-fill"
            style={{ width: `${capClamped}%` }}
          />
        </div>
      </div>
      <div className="me-metric">
        <span className="label">Final exposure</span>
        <span className="value">{fmtExposure(finalExposure)}</span>
      </div>
    </div>
  );
}
