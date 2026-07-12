import type {
  ComparisonResult,
  QualitativeOverlay,
} from "../../api";

/**
 * OverlayComparisonPanel — a sanitized, production-shaped view of Pantheon
 * Research's dual-LLM equity overlay comparison (Qwen Cloud vs DeepSeek).
 *
 * It is intentionally driven entirely by a ComparisonResult prop so it renders
 * identically from bundled offline samples or a live API response, and it is
 * fail-closed by construction: BLOCKED / PARTIAL / API_ERROR / PARSE_ERROR /
 * QWEN_NOT_GENERATED states are surfaced explicitly and never smoothed into a
 * fabricated agreement score.
 */

const PROVIDER_STATUS_COLORS: Record<string, string> = {
  SUCCESS: "#16a34a",
  OFFLINE_SAMPLE: "#2563eb",
  BLOCKED_BY_MISSING_CREDENTIAL: "#dc2626",
  API_ERROR: "#dc2626",
  PARSE_ERROR: "#dc2626",
  QWEN_NOT_GENERATED: "#b45309",
};

const DATA_STATE_META: Record<string, { color: string; label: string }> = {
  LIVE_DUAL: { color: "#16a34a", label: "Live · Dual-Model" },
  OFFLINE_SAMPLE: { color: "#2563eb", label: "Offline Sample · Dual-Model" },
  MIXED: { color: "#7c3aed", label: "Mixed (Live + Sample)" },
  PARTIAL: { color: "#b45309", label: "Partial · One Provider Only" },
  BLOCKED: { color: "#dc2626", label: "Blocked · Fail-Closed" },
};

const TONE_COLORS: Record<string, string> = {
  positive: "#16a34a",
  conservative_positive: "#2563eb",
  cautious: "#f59e0b",
  neutral: "#6b7280",
  negative: "#dc2626",
};

const SEVERITY_COLORS: Record<string, string> = {
  major: "#dc2626",
  moderate: "#f59e0b",
  minor: "#6b7280",
};

const AGREEMENT_COLORS: Record<string, string> = {
  HIGH: "#16a34a",
  MEDIUM: "#f59e0b",
  LOW: "#dc2626",
  NOT_COMPARABLE: "#6b7280",
};

const ASSESSMENT_FIELDS: { key: keyof AssessmentLike; label: string }[] = [
  { key: "business_quality", label: "Business Quality" },
  { key: "moat", label: "Moat & Competitive Advantage" },
  { key: "pricing_power", label: "Pricing Power" },
  { key: "capital_allocation", label: "Capital Allocation" },
  { key: "red_flags", label: "Red Flags & Risks" },
];

type AssessmentLike = {
  business_quality: string;
  moat: string;
  pricing_power: string;
  capital_allocation: string;
  red_flags: string;
};

export function dataStateMeta(state: string): { color: string; label: string } {
  return DATA_STATE_META[state] ?? { color: "#6b7280", label: state };
}

function Badge({ text, color }: { text: string; color: string }) {
  return (
    <span className="badge" style={{ backgroundColor: color }}>
      {text}
    </span>
  );
}

function ProviderCard({
  title,
  accent,
  overlay,
  tone,
}: {
  title: string;
  accent: string;
  overlay: QualitativeOverlay;
  tone: string;
}) {
  const a = overlay.assessment;
  const statusColor = PROVIDER_STATUS_COLORS[overlay.status] ?? "#6b7280";
  const failClosed = a == null;

  return (
    <div className="provider-card" data-testid={`provider-card-${overlay.provider}`}>
      <div className="provider-card-header" style={{ borderTopColor: accent }}>
        <div className="provider-title-row">
          <h3>{title}</h3>
          <Badge text={overlay.status} color={statusColor} />
        </div>
        <div className="provider-meta">
          <span className="model-name">{overlay.model}</span>
          {overlay.latency_ms != null && (
            <span className="latency">{overlay.latency_ms} ms</span>
          )}
          {overlay.attempts > 1 && (
            <span className="attempts">· {overlay.attempts} attempts</span>
          )}
          <Badge text={tone} color={TONE_COLORS[tone] ?? "#6b7280"} />
        </div>
        {overlay.prompt_version && (
          <div className="provider-versions">
            prompt {overlay.prompt_version} · schema {overlay.output_schema_version}
          </div>
        )}
      </div>

      {failClosed && (
        <div className="error-box fail-closed" role="alert">
          <strong>Fail-closed:</strong>{" "}
          {overlay.error_message ?? "No usable assessment was produced."}
        </div>
      )}

      {overlay.takeaway && (
        <p className="takeaway">
          <strong>Takeaway:</strong> {overlay.takeaway}
        </p>
      )}

      {a && (
        <div className="assessment-grid">
          {ASSESSMENT_FIELDS.map((f) => (
            <div key={f.key} className="assessment-field">
              <h4>{f.label}</h4>
              <p>{(a as AssessmentLike)[f.key] || "—"}</p>
            </div>
          ))}
          <div className="assessment-field confidence-field">
            <h4>Confidence</h4>
            <div className="confidence-bar">
              <div
                className="confidence-fill"
                style={{ width: `${a.confidence * 100}%`, backgroundColor: accent }}
              />
              <span>{Math.round(a.confidence * 100)}%</span>
            </div>
          </div>
          {overlay.usage?.total_tokens != null && (
            <div className="assessment-field">
              <h4>Tokens</h4>
              <p>{overlay.usage.total_tokens.toLocaleString()}</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default function OverlayComparisonPanel({
  comparison,
}: {
  comparison: ComparisonResult;
}) {
  const state = dataStateMeta(comparison.data_state);
  const agreementColor =
    AGREEMENT_COLORS[comparison.agreement_level] ?? "#6b7280";
  const comparable = comparison.agreement_score != null;

  return (
    <div className="overlay-comparison" data-testid="overlay-comparison">
      {/* Headline: data state + agreement + review gate */}
      <div className="oc-headline">
        <div className="oc-headline-item">
          <span className="label">Data State</span>
          <Badge text={state.label} color={state.color} />
        </div>
        <div className="oc-headline-item">
          <span className="label">Agreement</span>
          {comparable ? (
            <span className="oc-agreement" style={{ color: agreementColor }}>
              {comparison.agreement_score} · {comparison.agreement_level}
            </span>
          ) : (
            <Badge text="NOT COMPARABLE" color={agreementColor} />
          )}
        </div>
        <div className="oc-headline-item">
          <span className="label">Human Review</span>
          <span
            className="oc-review"
            style={{
              color: comparison.human_review_required ? "#dc2626" : "#16a34a",
            }}
          >
            {comparison.human_review_required ? "REQUIRED" : "Not Required"}
          </span>
        </div>
        {comparison.evidence_hash && (
          <div className="oc-headline-item">
            <span className="label">Evidence Hash</span>
            <code className="oc-hash" title={comparison.evidence_hash}>
              {comparison.evidence_hash.slice(0, 18)}…
            </code>
          </div>
        )}
      </div>

      {/* Human-review gate banner */}
      {comparison.human_review_required && (
        <div className="oc-review-banner" role="alert">
          Human review gate engaged
          {comparison.human_review_reason
            ? ` — ${comparison.human_review_reason}`
            : "."}{" "}
          LLM output does not execute trades; a human portfolio manager decides.
        </div>
      )}

      {/* Provider cards */}
      <div className="provider-cards">
        <ProviderCard
          title="Qwen Cloud"
          accent="#7c3aed"
          overlay={comparison.qwen_overlay}
          tone={comparison.qwen_tone}
        />
        <ProviderCard
          title="DeepSeek"
          accent="#2563eb"
          overlay={comparison.deepseek_overlay}
          tone={comparison.deepseek_tone}
        />
      </div>

      {/* Divergences */}
      <div className="oc-section">
        <h3>Divergences ({comparison.divergences.length})</h3>
        {!comparable ? (
          <p className="oc-muted">
            Divergence analysis is skipped when the comparison is not fully
            usable — a fail-closed provider is never averaged into a score.
          </p>
        ) : comparison.divergences.length === 0 ? (
          <p className="oc-muted">No material divergences — providers agree.</p>
        ) : (
          comparison.divergences.map((d, i) => (
            <div key={i} className="divergence-item">
              <Badge
                text={d.severity}
                color={SEVERITY_COLORS[d.severity] ?? "#6b7280"}
              />
              <span className="div-field">{d.field}</span>
              <div className="div-views">
                <span>
                  <strong>Qwen:</strong> {d.qwen_view}
                </span>
                <span>
                  <strong>DeepSeek:</strong> {d.deepseek_view}
                </span>
              </div>
            </div>
          ))
        )}
      </div>

      {/* Evidence gaps */}
      <div className="oc-section">
        <h3>Evidence Gaps ({comparison.evidence_gaps.length})</h3>
        {comparison.evidence_gaps.length === 0 ? (
          <p className="oc-muted">No evidence gaps flagged by either model.</p>
        ) : (
          <ul className="gap-list">
            {comparison.evidence_gaps.map((g, i) => (
              <li key={i}>{g}</li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}
