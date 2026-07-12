import type { MarketPulseMiniPanelData } from "../api";

/**
 * MarketPulseMiniPanel — context-only TA / market pulse panel.
 * Sample / redacted / stale-safe. No investment advice. No false freshness.
 */

export default function MarketPulseMiniPanel({ data }: { data: MarketPulseMiniPanelData }) {
  return (
    <div className="mini-panel market-pulse-mini" data-testid="market-pulse-mini-panel">
      <div className="mini-panel-header">
        <h3>Market Pulse / TA</h3>
        <span className="badge" style={{ backgroundColor: "#6b7280" }}>
          {data.data_state}
        </span>
      </div>
      <p className="mini-headline">{data.headline}</p>
      <div className="mini-regime">
        {Object.entries(data.market).map(([key, val]) => (
          <div key={key} className="mini-regime-item">
            <span className="mini-key">{key}</span>
            <span className="mini-val">{val}</span>
          </div>
        ))}
      </div>
      <table className="mini-indicators">
        <thead>
          <tr><th>Indicator</th><th>Value</th><th>Signal</th></tr>
        </thead>
        <tbody>
          {data.indicators.map((ind, i) => (
            <tr key={i}>
              <td>{ind.name}</td>
              <td>{ind.value}</td>
              <td>{ind.signal}</td>
            </tr>
          ))}
        </tbody>
      </table>
      <p className="mini-caveat"><strong>Don't infer:</strong> {data.what_not_to_infer}</p>
      <p className="mini-disclaimer">{data.disclaimer}</p>
    </div>
  );
}
