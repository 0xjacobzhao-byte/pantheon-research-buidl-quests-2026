import type { LiveDisabledProof as LiveDisabledProofData } from "../../api";

/**
 * LiveDisabledProof — prominent attestation that live trading is disabled and
 * no LLM actor ever auto-executed without human approval.
 */

function Flag({ label, value, safeWhenFalse }: { label: string; value: boolean; safeWhenFalse?: boolean }) {
  const safe = safeWhenFalse ? !value : value;
  return (
    <div className="ldp-flag">
      <span className="ldp-flag-label">{label}</span>
      <span
        className="badge"
        style={{ background: safe ? "var(--success)" : "var(--error)" }}
      >
        {value ? "true" : "false"}
      </span>
    </div>
  );
}

export default function LiveDisabledProof({
  data,
}: {
  data: LiveDisabledProofData;
}) {
  return (
    <div className="live-disabled-proof" data-testid="live-disabled-proof">
      <div className="ldp-banner">LIVE TRADING DISABLED</div>
      <div className="ldp-flags">
        <Flag label="live_enabled" value={data.live_enabled} safeWhenFalse />
        <Flag label="broker_connected" value={data.broker_connected} safeWhenFalse />
        <Flag label="real_order_path" value={data.real_order_path} safeWhenFalse />
        <Flag label="broker_adapter_present" value={data.broker_adapter_present} safeWhenFalse />
        <Flag label="paper_only" value={data.paper_only} />
        <Flag label="live_disabled" value={data.live_disabled} />
      </div>
      <div className="ldp-counts">
        <div className="ldp-count">
          <span className="value big">{data.llm_actor_intents}</span>
          <span className="label">LLM-actor intents</span>
        </div>
        <div className="ldp-count">
          <span className="value big">{data.llm_actor_paper_filled}</span>
          <span className="label">LLM-actor paper-filled</span>
        </div>
        <div className="ldp-count">
          <span
            className="value big"
            style={{
              color:
                data.llm_actor_auto_executed_without_approval === 0
                  ? "var(--success)"
                  : "var(--error)",
            }}
          >
            {data.llm_actor_auto_executed_without_approval}
          </span>
          <span className="label">Auto-executed without approval</span>
        </div>
      </div>
      <p className="ldp-attestation">{data.attestation}</p>
    </div>
  );
}
