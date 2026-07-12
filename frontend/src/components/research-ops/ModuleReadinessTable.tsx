import type { ReadinessModule } from "../../api";

/**
 * ModuleReadinessTable — honest readiness scorecard for every module.
 */

const READINESS_COLORS: Record<string, string> = {
  production: "#16a34a",
  validated: "#16a34a",
  in_process: "#f59e0b",
  warming_up: "#f59e0b",
  context_only: "#6b7280",
  scaffold: "#6b7280",
  research: "#3b82f6",
};

function readinessColor(r: string): string {
  return READINESS_COLORS[r?.toLowerCase()] ?? "#3b82f6";
}

function eligibleLabel(v: boolean | null): string {
  if (v === null) return "n/a";
  return v ? "yes" : "no";
}

export default function ModuleReadinessTable({
  modules,
}: {
  modules: ReadinessModule[];
}) {
  return (
    <div className="readiness-scroll" data-testid="module-readiness-table">
      <table className="readiness-table">
        <thead>
          <tr>
            <th>Module</th>
            <th>Readiness</th>
            <th>Validation</th>
            <th>Samples</th>
            <th>Outcome maturity</th>
            <th>Record kind</th>
            <th>PIT policy</th>
            <th>Public perf. eligible</th>
          </tr>
        </thead>
        <tbody>
          {modules.map((m) => (
            <tr key={m.module} data-testid={`readiness-row-${m.module}`}>
              <td>
                <strong>{m.display_name}</strong>
              </td>
              <td>
                <span
                  className="badge"
                  style={{ background: readinessColor(m.readiness) }}
                >
                  {m.readiness}
                </span>
              </td>
              <td>{m.validation_method}</td>
              <td>{m.sample_count}</td>
              <td>{m.outcome_maturity}</td>
              <td>{m.record_kind}</td>
              <td>{m.pit_policy}</td>
              <td>{eligibleLabel(m.public_performance_eligible)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
