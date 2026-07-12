import type { LineageNode } from "../../api";

/**
 * ProviderRecordPanel — renders the raw provider-record layer node(s), the
 * top of the lineage chain where external data first entered the system.
 */

function renderDetail(detail: any): { k: string; v: string }[] {
  if (detail == null) return [];
  if (typeof detail !== "object") return [{ k: "value", v: String(detail) }];
  return Object.entries(detail).map(([k, v]) => ({
    k,
    v: typeof v === "object" ? JSON.stringify(v) : String(v),
  }));
}

export default function ProviderRecordPanel({
  nodes,
}: {
  nodes: LineageNode[];
}) {
  if (nodes.length === 0) {
    return <p className="empty">No provider record in this lineage.</p>;
  }
  return (
    <div className="provider-record" data-testid="provider-record-panel">
      {nodes.map((n, i) => (
        <div key={i} className="pr-node">
          <div className="pr-head">
            <span className="badge" style={{ background: "var(--accent)" }}>
              {n.entity}
            </span>
            <code className="oc-hash">{n.key}</code>
          </div>
          <dl className="pr-detail">
            {renderDetail(n.detail).map(({ k, v }) => (
              <div key={k}>
                <dt>{k}</dt>
                <dd>{v}</dd>
              </div>
            ))}
          </dl>
        </div>
      ))}
    </div>
  );
}
