import type { MacroRiskBudget } from "../../api";

/**
 * MacroRegimeHistory — inline-SVG timeline of exposure cap over time with the
 * confirmed regime labelled per observation.
 */

const REGIME_COLORS: Record<string, string> = {
  risk_on: "#16a34a",
  neutral: "#f59e0b",
  risk_off: "#dc2626",
  defensive: "#dc2626",
};

function regimeColor(regime: string): string {
  return REGIME_COLORS[regime?.toLowerCase()] ?? "#3b82f6";
}

export default function MacroRegimeHistory({
  history,
}: {
  history: MacroRiskBudget[];
}) {
  if (history.length === 0) {
    return <p className="empty">No history available.</p>;
  }
  const barW = 100 / history.length;
  return (
    <div className="macro-history" data-testid="macro-regime-history">
      <svg
        className="mrh-svg"
        viewBox="0 0 100 40"
        preserveAspectRatio="none"
        role="img"
        aria-label="Exposure cap history"
      >
        {history.map((h, i) => {
          const cap = Math.max(0, Math.min(100, h.exposure_cap_pct));
          const barH = (cap / 100) * 38;
          return (
            <rect
              key={i}
              x={i * barW + barW * 0.1}
              y={40 - barH}
              width={barW * 0.8}
              height={barH}
              fill={regimeColor(h.confirmed_regime)}
            >
              <title>
                {h.as_of} · {h.confirmed_regime} · cap {h.exposure_cap_pct}%
              </title>
            </rect>
          );
        })}
      </svg>
      <div className="mrh-scroll">
        <table className="mrh-table">
          <thead>
            <tr>
              <th>As of</th>
              <th>Regime</th>
              <th>Score</th>
              <th>Exposure cap</th>
              <th>Hard stops</th>
            </tr>
          </thead>
          <tbody>
            {history.map((h, i) => (
              <tr key={i}>
                <td>{h.as_of}</td>
                <td>
                  <span
                    className="mrh-regime-dot"
                    style={{ background: regimeColor(h.confirmed_regime) }}
                  />
                  {h.confirmed_regime}
                </td>
                <td>{h.score.toFixed(2)}</td>
                <td>{h.exposure_cap_pct}%</td>
                <td>{h.hard_stops_active ? "active" : "clear"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
