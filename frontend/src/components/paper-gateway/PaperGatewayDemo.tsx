import { useEffect, useState, useCallback } from "react";
import {
  fetchPaperGatewayStatus,
  fetchPaperIntents,
  fetchPaperIntent,
  fetchPaperAudit,
  fetchLiveDisabledProof,
  approvePaperIntent,
  simulatePaperIntent,
  rejectPaperIntent,
  type PaperGatewayStatus,
  type PaperIntent,
  type PaperIntentDetail,
  type AuditEvent,
  type LiveDisabledProof as LiveDisabledProofData,
} from "../../api";
import LiveDisabledProof from "./LiveDisabledProof";
import ApprovalCard from "./ApprovalCard";
import RiskGatePanel from "./RiskGatePanel";
import IntentAuditTimeline from "./IntentAuditTimeline";

/**
 * PaperGatewayDemo — page container for the human-in-the-loop paper trading
 * gateway. Lists intents, shows the approval card + risk gate + audit trail for
 * the selected intent, and wires the approve / simulate / reject actions.
 */

const OPERATOR = "demo-operator";

export default function PaperGatewayDemo() {
  const [status, setStatus] = useState<PaperGatewayStatus | null>(null);
  const [proof, setProof] = useState<LiveDisabledProofData | null>(null);
  const [intents, setIntents] = useState<PaperIntent[]>([]);
  const [selected, setSelected] = useState<string>("");
  const [detail, setDetail] = useState<PaperIntentDetail | null>(null);
  const [audit, setAudit] = useState<AuditEvent[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    let active = true;
    Promise.all([
      fetchPaperGatewayStatus(),
      fetchPaperIntents(),
      fetchLiveDisabledProof(),
    ])
      .then(([st, ins, pf]) => {
        if (!active) return;
        setStatus(st);
        setIntents(ins.intents);
        setProof(pf);
        setSelected(ins.intents[0]?.intent_id ?? "");
      })
      .catch((e) => active && setError(e instanceof Error ? e.message : "Failed to load"))
      .finally(() => active && setLoading(false));
    return () => {
      active = false;
    };
  }, []);

  const loadSelected = useCallback((id: string) => {
    if (!id) return;
    Promise.all([fetchPaperIntent(id), fetchPaperAudit(id)])
      .then(([d, a]) => {
        setDetail(d);
        setAudit(a.events);
      })
      .catch((e) => setError(e instanceof Error ? e.message : "Failed to load intent"));
  }, []);

  useEffect(() => {
    loadSelected(selected);
  }, [selected, loadSelected]);

  const refreshIntents = useCallback(() => {
    fetchPaperIntents().then((ins) => setIntents(ins.intents)).catch(() => {});
  }, []);

  const handleApprove = useCallback(async () => {
    if (!selected) return;
    setBusy(true);
    setError(null);
    try {
      await approvePaperIntent(selected, OPERATOR);
      await simulatePaperIntent(selected);
      loadSelected(selected);
      refreshIntents();
    } catch (e) {
      setError(e instanceof Error ? e.message : "Approve failed");
    } finally {
      setBusy(false);
    }
  }, [selected, loadSelected, refreshIntents]);

  const handleReject = useCallback(async () => {
    if (!selected) return;
    setBusy(true);
    setError(null);
    try {
      await rejectPaperIntent(selected, OPERATOR, "Rejected by operator in demo.");
      loadSelected(selected);
      refreshIntents();
    } catch (e) {
      setError(e instanceof Error ? e.message : "Reject failed");
    } finally {
      setBusy(false);
    }
  }, [selected, loadSelected, refreshIntents]);

  if (loading) {
    return (
      <div data-testid="view-paper-gateway" className="view">
        <p className="empty">Loading paper gateway…</p>
      </div>
    );
  }

  return (
    <div data-testid="view-paper-gateway" className="view">
      {proof && (
        <section className="card safety-card">
          <h2>Live-Disabled Proof</h2>
          <LiveDisabledProof data={proof} />
        </section>
      )}

      <section className="card">
        <h2>Paper Trading Gateway</h2>
        {status && (
          <p className="section-lead">{status.note}</p>
        )}
        {error && <div className="error-box">{error}</div>}
        <div className="pg-layout">
          <div className="pg-intent-list">
            {intents.map((it) => (
              <button
                key={it.intent_id}
                className={`pg-intent-btn ${selected === it.intent_id ? "selected" : ""}`}
                onClick={() => setSelected(it.intent_id)}
              >
                <span className="pg-intent-ticker">
                  {it.side.toUpperCase()} {it.ticker}
                </span>
                <span className="pg-intent-state">{it.state}</span>
              </button>
            ))}
          </div>

          <div className="pg-detail">
            {detail?.approval_card ? (
              <>
                <ApprovalCard
                  card={detail.approval_card}
                  onApprove={handleApprove}
                  onReject={handleReject}
                  busy={busy}
                />
                <RiskGatePanel card={detail.approval_card} />
              </>
            ) : (
              <p className="empty">
                {detail
                  ? `Intent ${detail.intent.state} — no approval card.`
                  : "Select an intent."}
              </p>
            )}
          </div>
        </div>
      </section>

      <section className="card">
        <h2>Intent Audit Trail</h2>
        <IntentAuditTimeline events={audit} />
      </section>
    </div>
  );
}
