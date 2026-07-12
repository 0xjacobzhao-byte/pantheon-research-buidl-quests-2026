import type { FiccMiniPanelData } from "../api";

/**
 * FiccMiniPanel — context-only FICC (FI / FX / Commodity) panel.
 * Sample / redacted / stale-safe. No investment advice. No false freshness.
 */

function AssetBlock({ title, data }: { title: string; data: Record<string, string> }) {
  return (
    <div className="ficc-block">
      <h4>{title}</h4>
      {Object.entries(data).map(([key, val]) => (
        <div key={key} className="ficc-row">
          <span className="ficc-key">{key.replace(/_/g, " ")}</span>
          <span className="ficc-val">{val}</span>
        </div>
      ))}
    </div>
  );
}

export default function FiccMiniPanel({ data }: { data: FiccMiniPanelData }) {
  return (
    <div className="mini-panel ficc-mini" data-testid="ficc-mini-panel">
      <div className="mini-panel-header">
        <h3>FICC (FI / FX / Commodity)</h3>
        <span className="badge" style={{ backgroundColor: "#6b7280" }}>
          {data.data_state}
        </span>
      </div>
      <p className="mini-headline">{data.headline}</p>
      <div className="ficc-grid">
        <AssetBlock title="Fixed Income" data={data.fixed_income} />
        <AssetBlock title="FX" data={data.fx} />
        <AssetBlock title="Commodity" data={data.commodity} />
      </div>
      <p className="mini-caveat"><strong>Don't infer:</strong> {data.what_not_to_infer}</p>
      <p className="mini-disclaimer">{data.disclaimer}</p>
    </div>
  );
}
