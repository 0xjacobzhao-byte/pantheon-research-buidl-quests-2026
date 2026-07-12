import type { ModuleSnapshotGridData, ModuleSnapshot } from "../api";

/**
 * ModuleSnapshotGrid — a public-safe map of the full Pantheon Research system
 * (Macro, Market Pulse/TA, FICC FI/FX/Commodity, Ticker Profile, Qwen-vs-DeepSeek,
 * Data Quality). It shows the system's scope and its honest governance state
 * (data_state, freshness, validation_state, what-not-to-infer) without exposing
 * any proprietary engine, live feed, or secret. Most cards are context-only
 * bundled samples; the LLM and data-quality cards are computed live in-process.
 */

const DATA_STATE_COLORS: Record<string, string> = {
  LIVE_DUAL: "#16a34a",
  LIVE_IN_PROCESS: "#16a34a",
  OFFLINE_SAMPLE: "#2563eb",
  CONTEXT_ONLY: "#6b7280",
  MIXED: "#7c3aed",
  PARTIAL: "#b45309",
  BLOCKED: "#dc2626",
};

const GROUP_ORDER = [
  "Macro",
  "Signal",
  "FICC",
  "Equity",
  "Research-Ops",
];

function stateColor(state: string): string {
  return DATA_STATE_COLORS[state] ?? "#6b7280";
}

function Card({ m }: { m: ModuleSnapshot }) {
  return (
    <div className="module-card" data-testid={`module-card-${m.key}`}>
      <div className="module-card-top">
        <span className="module-group">{m.group}</span>
        <span
          className="badge"
          style={{ backgroundColor: stateColor(m.data_state) }}
        >
          {m.data_state}
        </span>
      </div>
      <h4 className="module-title">{m.title}</h4>
      <p className="module-headline">{m.headline}</p>
      <dl className="module-meta">
        <div>
          <dt>Freshness</dt>
          <dd>{m.freshness}</dd>
        </div>
        <div>
          <dt>Validation</dt>
          <dd>{m.validation_state}</dd>
        </div>
        <div>
          <dt>Role</dt>
          <dd>{m.role}</dd>
        </div>
      </dl>
      <p className="module-caveat">
        <strong>Don't infer:</strong> {m.what_not_to_infer}
      </p>
      <code className="module-endpoint">{m.sample_endpoint}</code>
    </div>
  );
}

export default function ModuleSnapshotGrid({
  grid,
}: {
  grid: ModuleSnapshotGridData;
}) {
  // Stable ordering by group, then original order within group.
  const ordered = [...grid.modules].sort((a, b) => {
    const ga = GROUP_ORDER.indexOf(a.group);
    const gb = GROUP_ORDER.indexOf(b.group);
    return (ga === -1 ? 99 : ga) - (gb === -1 ? 99 : gb);
  });

  return (
    <div className="module-snapshot-grid" data-testid="module-snapshot-grid">
      <p className="module-disclaimer">{grid.disclaimer}</p>
      <div className="module-cards">
        {ordered.map((m) => (
          <Card key={m.key} m={m} />
        ))}
      </div>
      <p className="module-asof">
        Grid schema {grid.schema_version} · as-of {grid.as_of}
      </p>
    </div>
  );
}
