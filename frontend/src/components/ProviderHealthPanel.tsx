import type { ProviderHealthData } from "../api";

/**
 * ProviderHealthPanel — public-safe provider health status.
 * Shows Qwen/DeepSeek config, sample evidence, Alibaba proof, offline/live
 * mode, secrets exposure, and fail-closed state. No secrets exposed.
 */

function StatusDot({ ok }: { ok: boolean }) {
  return (
    <span
      className="ph-dot"
      style={{ backgroundColor: ok ? "#16a34a" : "#9ca3af" }}
    />
  );
}

export default function ProviderHealthPanel({ data }: { data: ProviderHealthData }) {
  return (
    <div className="provider-health-panel" data-testid="provider-health-panel">
      <h3>Provider Health</h3>
      <p className="ph-schema">{data.schema_version} · {data.demo_mode} mode</p>

      <div className="ph-grid">
        {/* Qwen */}
        <div className="ph-card">
          <div className="ph-card-header">
            <StatusDot ok={data.qwen.configured} />
            <h4>Qwen via Alibaba Cloud</h4>
          </div>
          <div className="ph-detail">
            <span>Provider: {data.qwen.provider}</span>
            <span>Model: {data.qwen.model}</span>
            <span>Status: {data.qwen.status}</span>
            <span>Fail-closed: {data.qwen.fail_closed_active ? "active" : "inactive"}</span>
            <span>Live gated: {data.qwen.live_mode_gated ? "yes" : "no"}</span>
          </div>
        </div>

        {/* DeepSeek */}
        <div className="ph-card">
          <div className="ph-card-header">
            <StatusDot ok={data.deepseek.configured} />
            <h4>DeepSeek</h4>
          </div>
          <div className="ph-detail">
            <span>Provider: {data.deepseek.provider}</span>
            <span>Model: {data.deepseek.model}</span>
            <span>Status: {data.deepseek.status}</span>
            <span>Fail-closed: {data.deepseek.fail_closed_active ? "active" : "inactive"}</span>
            <span>Live gated: {data.deepseek.live_mode_gated ? "yes" : "no"}</span>
          </div>
        </div>

        {/* System status */}
        <div className="ph-card ph-system">
          <h4>System Status</h4>
          <div className="ph-detail">
            <span>
              <StatusDot ok={data.sample_evidence.present} />
              Sample evidence: {data.sample_evidence.count} tickers ({data.sample_evidence.tickers.join(", ")})
            </span>
            <span>
              <StatusDot ok={data.alibaba_proof.documented} />
              Alibaba proof: documented ({data.alibaba_proof.endpoint})
            </span>
            <span>
              <StatusDot ok={data.offline_mode.available} />
              Offline mode: {data.offline_mode.active ? "active" : "available"}
            </span>
            <span>
              <StatusDot ok={!data.live_mode.gated} />
              Live mode: {data.live_mode.gated ? "gated" : "active"}
            </span>
            <span>
              <StatusDot ok={!data.secrets_exposed} />
              Secrets exposed: {data.secrets_exposed ? "YES" : "none"}
            </span>
            <span>
              <StatusDot ok={data.fail_closed_active} />
              Fail-closed: {data.fail_closed_active ? "active" : "inactive"}
            </span>
          </div>
        </div>
      </div>

      <p className="ph-note">{data.note}</p>
    </div>
  );
}
