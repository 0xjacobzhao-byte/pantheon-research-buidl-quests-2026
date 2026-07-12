import type { ResearchOpsValidation } from "../../api";

/**
 * ValidationPolicyPanel — the controlled vocabularies and per-module policy
 * governing how records may be validated and whether performance is publishable.
 */

export default function ValidationPolicyPanel({
  data,
}: {
  data: ResearchOpsValidation;
}) {
  return (
    <div className="validation-policy" data-testid="validation-policy-panel">
      <div className="vp-vocab-grid">
        <div className="vp-vocab">
          <h4>Readiness vocabulary</h4>
          <div className="vp-chips">
            {data.readiness_vocabulary.map((v) => (
              <span key={v} className="badge" style={{ background: "var(--surface2)" }}>
                {v}
              </span>
            ))}
          </div>
        </div>
        <div className="vp-vocab">
          <h4>Record kinds</h4>
          <div className="vp-chips">
            {data.record_kind_vocabulary.map((v) => (
              <span key={v} className="badge" style={{ background: "var(--surface2)" }}>
                {v}
              </span>
            ))}
          </div>
        </div>
        <div className="vp-vocab">
          <h4>PIT policies</h4>
          <div className="vp-chips">
            {data.pit_policy_vocabulary.map((v) => (
              <span key={v} className="badge" style={{ background: "var(--surface2)" }}>
                {v}
              </span>
            ))}
          </div>
        </div>
      </div>

      <div className="readiness-scroll">
        <table className="readiness-table">
          <thead>
            <tr>
              <th>Module</th>
              <th>Validation method</th>
              <th>Record kind</th>
              <th>PIT policy</th>
              <th>Public perf. eligible</th>
              <th>Record-kind policy</th>
            </tr>
          </thead>
          <tbody>
            {data.modules.map((m) => (
              <tr key={m.module}>
                <td>
                  <strong>{m.module}</strong>
                </td>
                <td>{m.validation_method}</td>
                <td>{m.record_kind}</td>
                <td>{m.pit_policy}</td>
                <td>
                  {m.public_performance_eligible === null
                    ? "n/a"
                    : m.public_performance_eligible
                    ? "yes"
                    : "no"}
                </td>
                <td>{m.record_kind_policy}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
