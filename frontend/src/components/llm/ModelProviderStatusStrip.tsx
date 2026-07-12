import type { LlmProvider } from "../../api";

/**
 * ModelProviderStatusStrip — horizontal strip of the registered LLM providers
 * with credential + mode state. Optionally overlays per-case comparability.
 */

export default function ModelProviderStatusStrip({
  providers,
  providerStates,
}: {
  providers: LlmProvider[];
  providerStates?: Record<string, string>;
}) {
  return (
    <div className="mp-strip" data-testid="model-provider-strip">
      {providers.map((p) => {
        const caseState = providerStates?.[p.provider];
        return (
          <div key={p.provider} className="mp-strip-item">
            <div className="mp-strip-top">
              <span className="mp-strip-name">{p.display_name}</span>
              <span
                className="mp-dot"
                style={{
                  backgroundColor: p.credential_configured
                    ? "var(--success)"
                    : "var(--warning)",
                }}
                title={p.credential_configured ? "credential configured" : "offline"}
              />
            </div>
            <div className="mp-strip-model">{p.model}</div>
            <div className="mp-strip-meta">
              <span className="badge" style={{ background: "var(--surface2)" }}>
                {p.mode}
              </span>
              {caseState && (
                <span className="badge" style={{ background: "var(--accent)" }}>
                  {caseState}
                </span>
              )}
            </div>
          </div>
        );
      })}
    </div>
  );
}
