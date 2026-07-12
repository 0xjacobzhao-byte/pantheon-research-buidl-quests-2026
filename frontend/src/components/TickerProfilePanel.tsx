import type { TickerProfile } from "../api";

/**
 * TickerProfilePanel — production-feel ticker profile with KPI cards,
 * evidence pack summary, and human-review status. Sample-backed NVDA and MA
 * only. No live data, no private DB queries.
 */

const SIGNAL_COLORS: Record<string, string> = {
  premium: "#b45309",
  exceptional: "#16a34a",
  strong: "#2563eb",
  solid: "#2563eb",
  conservative: "#16a34a",
  minimal: "#6b7280",
  moderate: "#b45309",
  low: "#6b7280",
  bullish: "#16a34a",
  "neutral-to-strong": "#2563eb",
  neutral: "#6b7280",
};

function KpiCardView({ card }: { card: { label: string; metrics: { name: string; value: string | number; signal: string }[]; summary: string } }) {
  return (
    <div className="kpi-card">
      <h4 className="kpi-label">{card.label}</h4>
      <div className="kpi-metrics">
        {card.metrics.map((m, i) => (
          <div key={i} className="kpi-metric">
            <span className="kpi-name">{m.name}</span>
            <span className="kpi-value">{m.value}</span>
            <span
              className="kpi-signal"
              style={{ color: SIGNAL_COLORS[m.signal] ?? "#6b7280" }}
            >
              {m.signal}
            </span>
          </div>
        ))}
      </div>
      <p className="kpi-summary">{card.summary}</p>
    </div>
  );
}

export default function TickerProfilePanel({
  profile,
}: {
  profile: TickerProfile;
}) {
  const cards = profile.kpi_cards;
  return (
    <div className="ticker-profile-panel" data-testid="ticker-profile-panel">
      {/* Company header */}
      <div className="tp-header">
        <h3 className="tp-company">{profile.company_name}</h3>
        <div className="tp-meta">
          <span>{profile.exchange}</span>
          <span>{profile.sector}</span>
          <span>{profile.industry}</span>
          <span>Mkt Cap: ${(profile.market_cap_usd / 1e9).toFixed(0)}B</span>
        </div>
      </div>

      {/* KPI cards */}
      <div className="kpi-grid">
        <KpiCardView card={cards.valuation} />
        <KpiCardView card={cards.quality} />
        <KpiCardView card={cards.growth} />
        <KpiCardView card={cards.anchors} />
        <KpiCardView card={cards.technical} />
      </div>

      {/* Evidence pack summary */}
      <div className="tp-evidence-summary">
        <h4>Evidence Pack</h4>
        <div className="tp-ev-row">
          <span>Sources: {profile.evidence_pack_summary.sources}</span>
          <span>Hash: <code>{profile.evidence_pack_summary.hash_prefix}</code></span>
          <span>As of: {profile.evidence_pack_summary.as_of}</span>
        </div>
        <div className="tp-ev-fields">
          {profile.evidence_pack_summary.fields_covered.map((f) => (
            <span key={f} className="badge">{f}</span>
          ))}
        </div>
      </div>

      {/* Human review status */}
      <div className={`tp-human-review ${profile.human_review.status === "GATED" ? "gated" : "cleared"}`}>
        <h4>Human Review</h4>
        <span
          className="badge"
          style={{
            backgroundColor: profile.human_review.status === "GATED" ? "#dc2626" : "#16a34a",
          }}
        >
          {profile.human_review.status}
        </span>
        {profile.human_review.reason && (
          <p className="tp-review-reason">{profile.human_review.reason}</p>
        )}
      </div>
    </div>
  );
}
