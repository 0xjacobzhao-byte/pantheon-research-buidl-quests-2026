import { useEffect, useState } from "react";
import {
  fetchLineage,
  fetchDpObservations,
  fetchDpVersions,
  DEFAULT_LINEAGE_HASH,
  type LineageData,
  type DpVersion,
  type LineageNode,
} from "../../api";
import ProviderRecordPanel from "./ProviderRecordPanel";
import ObservationVersionTimeline from "./ObservationVersionTimeline";
import EvidenceConsumersPanel from "./EvidenceConsumersPanel";

/**
 * DataLineageExplorer — page container that walks the full evidence lineage
 * for the anchor NVDA evidence hash, top layer to bottom:
 * provider record → canonical observation → observation version →
 * derived snapshot → product snapshot → evidence-pack hash → LLM overlay.
 */

const LAYER_ORDER = [
  "provider_record",
  "canonical_observation",
  "observation_version",
  "derived_snapshot",
  "product_snapshot",
  "evidence_pack_hash",
  "llm_overlay",
];

const LAYER_LABELS: Record<string, string> = {
  provider_record: "Provider Record",
  canonical_observation: "Canonical Observation",
  observation_version: "Observation Version",
  derived_snapshot: "Derived Snapshot",
  product_snapshot: "Product Snapshot",
  evidence_pack_hash: "Evidence Pack Hash",
  llm_overlay: "LLM Overlay",
};

function detailText(detail: any): string {
  if (detail == null) return "";
  if (typeof detail === "string") return detail;
  if (typeof detail === "object") {
    const parts = Object.entries(detail)
      .slice(0, 4)
      .map(([k, v]) => `${k}: ${typeof v === "object" ? JSON.stringify(v) : v}`);
    return parts.join(" · ");
  }
  return String(detail);
}

export default function DataLineageExplorer() {
  const [lineage, setLineage] = useState<LineageData | null>(null);
  const [versions, setVersions] = useState<DpVersion[]>([]);
  const [observationId, setObservationId] = useState<number | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let active = true;
    fetchLineage(DEFAULT_LINEAGE_HASH)
      .then((lin) => {
        if (active) setLineage(lin);
      })
      .catch((e) => active && setError(e instanceof Error ? e.message : "Failed to load"))
      .finally(() => active && setLoading(false));

    fetchDpObservations()
      .then((obs) => {
        const first = obs.observations[0];
        if (!first || !active) return;
        setObservationId(first.id);
        return fetchDpVersions(first.id);
      })
      .then((v) => {
        if (active && v) setVersions(v.versions);
      })
      .catch(() => {});
    return () => {
      active = false;
    };
  }, []);

  if (loading) {
    return (
      <div data-testid="view-data-lineage" className="view">
        <p className="empty">Loading data lineage…</p>
      </div>
    );
  }
  if (error || !lineage) {
    return (
      <div data-testid="view-data-lineage" className="view">
        <div className="error-box">{error ?? "No lineage data."}</div>
      </div>
    );
  }

  const byLayer = (layer: string): LineageNode[] =>
    lineage.nodes.filter((n) => n.layer === layer);

  return (
    <div data-testid="view-data-lineage" className="view">
      <section className="card">
        <h2>Data Lineage Explorer</h2>
        <p className="section-lead">
          End-to-end provenance for a single evidence hash — from the raw
          provider record all the way to the LLM overlays that consumed it.
        </p>
        <p className="meta">
          <code className="oc-hash">{lineage.evidence_hash}</code>{" "}
          {lineage.found ? (
            <span className="badge" style={{ background: "var(--success)" }}>
              found
            </span>
          ) : (
            <span className="badge" style={{ background: "var(--error)" }}>
              not found
            </span>
          )}
        </p>

        <div className="lineage-chain">
          {LAYER_ORDER.map((layer, li) => {
            const nodes = byLayer(layer);
            if (nodes.length === 0) return null;
            return (
              <div key={layer} className="lineage-layer" data-testid={`lineage-layer-${layer}`}>
                <div className="ll-head">
                  <span className="ll-num">{li + 1}</span>
                  <span className="ll-name">{LAYER_LABELS[layer] ?? layer}</span>
                </div>
                {nodes.map((n, ni) => (
                  <div key={ni} className="ll-node">
                    <span className="ll-entity">{n.entity}</span>
                    <code className="oc-hash">{n.key}</code>
                    <span className="ll-detail">{detailText(n.detail)}</span>
                  </div>
                ))}
              </div>
            );
          })}
        </div>
      </section>

      <section className="card">
        <h2>Provider Record</h2>
        <ProviderRecordPanel nodes={byLayer("provider_record")} />
      </section>

      <section className="card">
        <h2>Observation Version History</h2>
        <ObservationVersionTimeline observationId={observationId} versions={versions} />
      </section>

      <section className="card">
        <h2>Evidence Consumers</h2>
        <p className="section-lead">{lineage.note}</p>
        <EvidenceConsumersPanel consumers={lineage.llm_consumers} />
      </section>
    </div>
  );
}
