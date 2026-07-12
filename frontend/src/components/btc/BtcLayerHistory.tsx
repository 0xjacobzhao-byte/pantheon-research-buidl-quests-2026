import type { BtcHistoryRow } from "../../api";

/**
 * BtcLayerHistory — inline-SVG BTC price sparkline over the window, with a
 * table of per-day layer states below.
 */

export default function BtcLayerHistory({
  rows,
}: {
  rows: BtcHistoryRow[];
}) {
  if (rows.length === 0) {
    return <p className="empty">No history available.</p>;
  }
  const prices = rows.map((r) => r.btc_price);
  const min = Math.min(...prices);
  const max = Math.max(...prices);
  const span = max - min || 1;
  const points = rows
    .map((r, i) => {
      const x = (i / (rows.length - 1 || 1)) * 100;
      const y = 40 - ((r.btc_price - min) / span) * 38 - 1;
      return `${x.toFixed(2)},${y.toFixed(2)}`;
    })
    .join(" ");

  return (
    <div className="btc-history" data-testid="btc-layer-history">
      <svg
        className="bh-svg"
        viewBox="0 0 100 40"
        preserveAspectRatio="none"
        role="img"
        aria-label="BTC price history"
      >
        <polyline
          points={points}
          fill="none"
          stroke="var(--accent)"
          strokeWidth="0.8"
        />
      </svg>
      <div className="bh-range">
        <span>low ${min.toLocaleString()}</span>
        <span>high ${max.toLocaleString()}</span>
      </div>
      <div className="bh-scroll">
        <table className="bh-table">
          <thead>
            <tr>
              <th>Date</th>
              <th>Price</th>
              <th>Signal</th>
              <th>Guardian</th>
              <th>Regime</th>
              <th>Bottom model</th>
              <th>Risk radar</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((r, i) => (
              <tr key={i}>
                <td>{r.date}</td>
                <td>${r.btc_price.toLocaleString()}</td>
                <td>{r.final_signal_label}</td>
                <td>{r.guardian_status}</td>
                <td>{r.regime}</td>
                <td>{r.bottom_model_label}</td>
                <td>{r.risk_radar_label}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
