import type { DataQualityReport } from "../api";

/**
 * DataQualityPanel — a public-safe slice of Pantheon Research's Research-Ops
 * governance plane. It reports configuration and coverage state (what is
 * configured, what is reachable, which overlays are usable) without exposing
 * any admin action, secret, or private dataset.
 */

function Dot({ ok }: { ok: boolean }) {
  return (
    <span
      className="dq-dot"
      style={{ backgroundColor: ok ? "#16a34a" : "#9ca3af" }}
      aria-label={ok ? "configured" : "not configured"}
    />
  );
}

export default function DataQualityPanel({
  report,
}: {
  report: DataQualityReport;
}) {
  const cov = report.sample_evidence_coverage;
  return (
    <div className="data-quality-panel" data-testid="data-quality-panel">
      <div className="dq-row">
        <div className="dq-metric">
          <span className="label">Mode</span>
          <span className="value">{report.mode}</span>
        </div>
        <div className="dq-metric">
          <span className="label">Qwen</span>
          <span className="value">
            <Dot ok={report.providers.qwen_configured} />
            {report.providers.qwen_configured ? "configured" : "offline"} ·{" "}
            {report.providers.qwen_model}
          </span>
        </div>
        <div className="dq-metric">
          <span className="label">DeepSeek</span>
          <span className="value">
            <Dot ok={report.providers.deepseek_configured} />
            {report.providers.deepseek_configured ? "configured" : "offline"} ·{" "}
            {report.providers.deepseek_model}
          </span>
        </div>
        <div className="dq-metric">
          <span className="label">Alibaba Proof</span>
          <span className="value">
            <Dot ok={report.alibaba_proof_reachable} />
            {report.alibaba_proof_reachable ? "reachable" : "unreachable"}
          </span>
        </div>
        <div className="dq-metric">
          <span className="label">Healthy Comparisons</span>
          <span className="value">
            {cov.healthy_comparisons}/{cov.evidence_packs_present}
          </span>
        </div>
      </div>

      <table className="dq-table">
        <thead>
          <tr>
            <th>Ticker</th>
            <th>Qwen</th>
            <th>DeepSeek</th>
            <th>Data State</th>
            <th>Agreement</th>
            <th>Review</th>
          </tr>
        </thead>
        <tbody>
          {report.overlay_statuses.map((row, i) => (
            <tr key={i}>
              <td>{String(row.ticker ?? "—")}</td>
              <td>{String(row.qwen_status ?? "—")}</td>
              <td>{String(row.deepseek_status ?? "—")}</td>
              <td>{String(row.data_state ?? "—")}</td>
              <td>{String(row.agreement_level ?? "—")}</td>
              <td>{row.human_review_required ? "required" : "—"}</td>
            </tr>
          ))}
        </tbody>
      </table>

      <p className="dq-note">{report.governance_note}</p>
    </div>
  );
}
