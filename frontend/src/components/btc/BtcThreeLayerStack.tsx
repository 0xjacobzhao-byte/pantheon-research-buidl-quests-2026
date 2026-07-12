import { useEffect, useState } from "react";
import {
  fetchBtcStack,
  fetchBtcHistory,
  fetchBtcConflicts,
  type BtcStack,
  type BtcHistoryData,
  type BtcConflictsData,
} from "../../api";
import BtcCurrentPosture from "./BtcCurrentPosture";
import BtcLayerHistory from "./BtcLayerHistory";
import BtcConflictResolutionPanel from "./BtcConflictResolutionPanel";

/**
 * BtcThreeLayerStack — page container for the BTC L1/L2/L3 decision stack.
 * Renders each layer's state, the macro risk-budget input, the resolved
 * posture, the layer history and the conflict-resolution examples.
 */

function fmt(v: any): string {
  if (v == null) return "—";
  if (typeof v === "number") return String(v);
  if (typeof v === "boolean") return v ? "yes" : "no";
  if (typeof v === "object") return JSON.stringify(v);
  return String(v);
}

function LayerRow({ label, value }: { label: string; value: any }) {
  return (
    <div className="bl-row">
      <span className="bl-key">{label}</span>
      <span className="bl-val">{fmt(value)}</span>
    </div>
  );
}

export default function BtcThreeLayerStack() {
  const [stack, setStack] = useState<BtcStack | null>(null);
  const [history, setHistory] = useState<BtcHistoryData | null>(null);
  const [conflicts, setConflicts] = useState<BtcConflictsData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let active = true;
    Promise.all([
      fetchBtcStack(),
      fetchBtcHistory(60),
      fetchBtcConflicts(),
    ])
      .then(([s, h, c]) => {
        if (!active) return;
        setStack(s);
        setHistory(h);
        setConflicts(c);
      })
      .catch((e) => active && setError(e instanceof Error ? e.message : "Failed to load"))
      .finally(() => active && setLoading(false));
    return () => {
      active = false;
    };
  }, []);

  if (loading) {
    return (
      <div data-testid="view-btc" className="view">
        <p className="empty">Loading BTC stack…</p>
      </div>
    );
  }
  if (error || !stack) {
    return (
      <div data-testid="view-btc" className="view">
        <div className="error-box">{error ?? "No BTC data."}</div>
      </div>
    );
  }

  return (
    <div data-testid="view-btc" className="view">
      <section className="card">
        <h2>BTC Three-Layer Stack</h2>
        <p className="section-lead">
          Three independent layers (structure, momentum, risk) resolve to a
          single posture, gated by the macro risk budget. Context only — not a
          trade signal.
        </p>

        <div className="btc-layers">
          <div className="btc-layer-card" data-testid="btc-l1">
            <div className="blc-head">
              <h3>L1 · Structure</h3>
              <span className="badge" style={{ background: "var(--surface2)" }}>
                {stack.l1.state}
              </span>
            </div>
            <LayerRow label="Label" value={stack.l1.label} />
            <LayerRow label="Primary signal" value={stack.l1.primary_signal} />
            <LayerRow label="Layer bias" value={stack.l1.layer_bias} />
            <LayerRow label="Execution effect" value={stack.l1.execution_effect} />
            <LayerRow label="Triggered" value={stack.l1.triggered} />
          </div>

          <div className="btc-layer-card" data-testid="btc-l2">
            <div className="blc-head">
              <h3>L2 · Momentum</h3>
              <span className="badge" style={{ background: "var(--surface2)" }}>
                {stack.l2.regime}
              </span>
            </div>
            <LayerRow label="Guardian" value={stack.l2.guardian_state} />
            <LayerRow label="Hunter" value={stack.l2.hunter_state} />
            <LayerRow label="Architect" value={stack.l2.architect_state} />
            <LayerRow label="Final signal" value={stack.l2.final_signal_direction} />
            <LayerRow label="Risk multiplier" value={stack.l2.risk_multiplier} />
            {stack.l2.missing_fields.length > 0 && (
              <p className="blc-missing">
                Missing: {stack.l2.missing_fields.join(", ")}
              </p>
            )}
          </div>

          <div className="btc-layer-card" data-testid="btc-l3">
            <div className="blc-head">
              <h3>L3 · Risk</h3>
              <span className="badge" style={{ background: "var(--surface2)" }}>
                {stack.l3.state}
              </span>
            </div>
            <LayerRow label="Risk label" value={stack.l3.risk_label_raw} />
            <LayerRow label="Mode" value={stack.l3.mode} />
            <LayerRow label="High alert" value={stack.l3.high_alert_mode} />
            <LayerRow label="Primary signal" value={stack.l3.primary_signal} />
            <LayerRow label="Posture 72h" value={stack.l3.posture_72h} />
          </div>

          <div className="btc-layer-card" data-testid="btc-macro">
            <div className="blc-head">
              <h3>Macro Input</h3>
              <span className="badge" style={{ background: "var(--surface2)" }}>
                {stack.macro_risk_budget.confirmed_regime}
              </span>
            </div>
            <LayerRow label="Regime" value={stack.macro_risk_budget.regime} />
            <LayerRow
              label="Hard stops"
              value={stack.macro_risk_budget.hard_stops_active}
            />
            <LayerRow
              label="Exposure cap"
              value={`${stack.macro_risk_budget.exposure_cap_pct}%`}
            />
            <LayerRow
              label="Final exposure"
              value={stack.macro_risk_budget.final_exposure}
            />
          </div>
        </div>

        <BtcCurrentPosture
          outcome={stack.resolved_posture.outcome}
          reasons={stack.resolved_posture.reasons}
          note={stack.resolved_posture.note}
          asOf={stack.as_of}
        />
        <p className="btc-disclaimer">{stack.disclaimer}</p>
      </section>

      {history && (
        <section className="card">
          <h2>Layer History</h2>
          <p className="section-lead">{history.disclaimer}</p>
          <BtcLayerHistory rows={history.rows} />
        </section>
      )}

      {conflicts && (
        <section className="card">
          <h2>Conflict Resolution</h2>
          <p className="section-lead">{conflicts.note}</p>
          <BtcConflictResolutionPanel examples={conflicts.examples} />
        </section>
      )}
    </div>
  );
}
