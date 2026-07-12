import { useState, useEffect, useCallback } from "react";
import {
  fetchProject,
  fetchDemoFlow,
  fetchComparison,
  fetchAlibabaProof,
  fetchQwenConfig,
  fetchDataQuality,
  fetchModules,
  fetchTickerProfile,
  fetchProviderHealth,
  fetchValidationTimeline,
  fetchMacroMini,
  fetchMarketPulseMini,
  fetchFiccMini,
  type ProjectInfo,
  type DemoFlow,
  type ComparisonResult,
  type AlibabaCloudProof,
  type QwenConfig,
  type DataQualityReport,
  type ModuleSnapshotGridData,
  type TickerProfile,
  type ProviderHealthData,
  type ValidationTimelineData,
  type MacroMiniPanelData,
  type MarketPulseMiniPanelData,
  type FiccMiniPanelData,
} from "./api";
import OverlayComparisonPanel from "./components/equity/OverlayComparisonPanel";
import DataQualityPanel from "./components/DataQualityPanel";
import ModuleSnapshotGrid from "./components/ModuleSnapshotGrid";
import TickerProfilePanel from "./components/TickerProfilePanel";
import ProviderHealthPanel from "./components/ProviderHealthPanel";
import ValidationTimeline from "./components/ValidationTimeline";
import MacroMiniPanel from "./components/MacroMiniPanel";
import MarketPulseMiniPanel from "./components/MarketPulseMiniPanel";
import FiccMiniPanel from "./components/FiccMiniPanel";

const TICKERS = ["MA", "NVDA"];

function App() {
  const [project, setProject] = useState<ProjectInfo | null>(null);
  const [demoFlow, setDemoFlow] = useState<DemoFlow | null>(null);
  const [proof, setProof] = useState<AlibabaCloudProof | null>(null);
  const [qwenCfg, setQwenCfg] = useState<QwenConfig | null>(null);
  const [dataQuality, setDataQuality] = useState<DataQualityReport | null>(null);
  const [modules, setModules] = useState<ModuleSnapshotGridData | null>(null);
  const [providerHealth, setProviderHealth] = useState<ProviderHealthData | null>(null);
  const [timeline, setTimeline] = useState<ValidationTimelineData | null>(null);
  const [macro, setMacro] = useState<MacroMiniPanelData | null>(null);
  const [marketPulse, setMarketPulse] = useState<MarketPulseMiniPanelData | null>(null);
  const [ficc, setFicc] = useState<FiccMiniPanelData | null>(null);
  const [selected, setSelected] = useState<string>("");
  const [comparison, setComparison] = useState<ComparisonResult | null>(null);
  const [tickerProfile, setTickerProfile] = useState<TickerProfile | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchProject().then(setProject).catch(() => {});
    fetchDemoFlow().then(setDemoFlow).catch(() => {});
    fetchAlibabaProof().then(setProof).catch(() => {});
    fetchQwenConfig().then(setQwenCfg).catch(() => {});
    fetchDataQuality().then(setDataQuality).catch(() => {});
    fetchModules().then(setModules).catch(() => {});
    fetchProviderHealth().then(setProviderHealth).catch(() => {});
    fetchValidationTimeline().then(setTimeline).catch(() => {});
    fetchMacroMini().then(setMacro).catch(() => {});
    fetchMarketPulseMini().then(setMarketPulse).catch(() => {});
    fetchFiccMini().then(setFicc).catch(() => {});
  }, []);

  const handleCompare = useCallback(async () => {
    if (!selected) return;
    setLoading(true);
    setError(null);
    setTickerProfile(null);
    try {
      const [comp, profile] = await Promise.all([
        fetchComparison(selected),
        fetchTickerProfile(selected).catch(() => null),
      ]);
      setComparison(comp);
      setTickerProfile(profile);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Unknown error");
    } finally {
      setLoading(false);
    }
  }, [selected]);

  const ev = comparison?.evidence;

  return (
    <div className="app">
      <header className="hero">
        <h1>Pantheon Research — BUIDL_QUESTS 2026</h1>
        <p className="subtitle">
          AI-native investment research operating system for public markets. This slice
          showcases the multi-model qualitative overlay: independent LLMs (Qwen, DeepSeek)
          analyze the same structured evidence, with agreement scoring, fail-closed handling,
          and a human-review gate.
        </p>
        {project && (
          <p className="demo-mode">
            Mode: {project.demo_mode} · v{project.version}
          </p>
        )}
      </header>

      {/* Four-layer architecture */}
      <section className="card">
        <h2>Four-Layer Architecture</h2>
        <div className="arch-layers">
          {(project?.architecture_layers ||
            demoFlow?.architecture_layers || [
              "Strategy",
              "Information",
              "Signal",
              "Trading",
            ]).map((layer, i, arr) => (
            <div key={layer} className="arch-layer">
              <span className="layer-num">{i + 1}</span>
              <span className="layer-name">{layer}</span>
              {i < arr.length - 1 && <span className="arch-arrow">→</span>}
            </div>
          ))}
        </div>
        <p className="arch-desc">
          Strategy → Information (evidence pack) → Signal (dual-LLM overlay) →
          Trading — every signal gated by human review.
        </p>
      </section>

      {/* System scope — module snapshot grid */}
      {modules && (
        <section className="card">
          <h2>System Scope — Module Snapshots</h2>
          <p className="section-lead">
            Pantheon Research is a multi-asset research operating system. This grid
            maps its full scope (Macro · TA · FICC · Equity · Research-Ops) with
            each module's honest governance state — not just the Qwen overlay.
          </p>
          <ModuleSnapshotGrid grid={modules} />
        </section>
      )}

      {/* Multi-asset context mini panels */}
      {(macro || marketPulse || ficc) && (
        <section className="card">
          <h2>Multi-Asset Context (Context-Only)</h2>
          <p className="section-lead">
            Illustrative panels showing the shape of Pantheon Research's Macro, TA, and FICC modules.
            Not investment advice. Values are bundled samples, not live feeds.
          </p>
          <div className="mini-panels-grid">
            {macro && <MacroMiniPanel data={macro} />}
            {marketPulse && <MarketPulseMiniPanel data={marketPulse} />}
            {ficc && <FiccMiniPanel data={ficc} />}
          </div>
        </section>
      )}

      {/* Provider Health */}
      {providerHealth && (
        <section className="card">
          <ProviderHealthPanel data={providerHealth} />
        </section>
      )}

      {/* Alibaba Cloud proof v2 */}
      {proof && (
        <section className="card">
          <h2>Alibaba Cloud Deployment Proof</h2>
          <p className="proof-schema">
            schema <code>{proof.schema_version}</code> · git{" "}
            <code>{proof.git_sha}</code> · {proof.demo_mode} mode
          </p>
          <div className="alibaba-grid">
            <div className="alibaba-item">
              <span className="label">Qwen AI Provider</span>
              <span className="value">{proof.qwen_provider}</span>
            </div>
            <div className="alibaba-item">
              <span className="label">Compute Host (honest)</span>
              <span className="value">
                {proof.host_runtime}{" "}
                <span
                  className="host-flag"
                  style={{ color: proof.alibaba_hosted ? "#16a34a" : "#b45309" }}
                >
                  {proof.alibaba_hosted
                    ? "Alibaba-hosted"
                    : "not Alibaba compute"}
                </span>
              </span>
            </div>
            <div className="alibaba-item">
              <span className="label">Backend</span>
              <span className="value">{proof.backend_runtime}</span>
            </div>
            <div className="alibaba-item">
              <span className="label">Reverse Proxy</span>
              <span className="value">{proof.reverse_proxy}</span>
            </div>
            <div className="alibaba-item">
              <span className="label">DashScope Key</span>
              <span className="value">
                {proof.dashscope_api_key_configured
                  ? "configured"
                  : "not set (offline)"}
              </span>
            </div>
            <div className="alibaba-item">
              <span className="label">Database</span>
              <span className="value">{proof.database.provider}</span>
            </div>
          </div>
          <p className="proof-db-note">
            <strong>Database claim (precise):</strong> {proof.database.note}
          </p>
          <details className="proof-claims">
            <summary>Safe claims &amp; non-claims</summary>
            <div className="claims-grid">
              <div>
                <h4>Safe claims</h4>
                <ul>
                  {proof.safe_claims.map((c, i) => (
                    <li key={i}>{c}</li>
                  ))}
                </ul>
              </div>
              <div>
                <h4>Non-claims</h4>
                <ul>
                  {proof.non_claims.map((c, i) => (
                    <li key={i}>{c}</li>
                  ))}
                </ul>
              </div>
            </div>
          </details>
        </section>
      )}

      {/* Qwen config */}
      {qwenCfg && (
        <section className="card">
          <h2>Qwen Integration</h2>
          <div className="alibaba-grid">
            <div className="alibaba-item">
              <span className="label">Model</span>
              <span className="value">{qwenCfg.model}</span>
            </div>
            <div className="alibaba-item">
              <span className="label">Base URL</span>
              <span className="value cfg-url">{qwenCfg.base_url}</span>
            </div>
            <div className="alibaba-item">
              <span className="label">Prompt / Schema</span>
              <span className="value">
                {qwenCfg.prompt_version} · {qwenCfg.output_schema_version}
              </span>
            </div>
            <div className="alibaba-item">
              <span className="label">Integration</span>
              <span className="value">{qwenCfg.integration_type}</span>
            </div>
          </div>
        </section>
      )}

      {/* Research-Ops mini: data quality */}
      {dataQuality && (
        <section className="card">
          <h2>Research-Ops · Data Quality</h2>
          <DataQualityPanel report={dataQuality} />
        </section>
      )}

      {/* Validation Timeline */}
      {timeline && (
        <section className="card">
          <ValidationTimeline data={timeline} />
        </section>
      )}

      {/* Ticker panel */}
      <section className="card">
        <h2>Run a Dual-Model Comparison</h2>
        <div className="ticker-panel">
          {TICKERS.map((t) => (
            <button
              key={t}
              className={`ticker-btn ${selected === t ? "selected" : ""}`}
              onClick={() => setSelected(t)}
            >
              {t}
            </button>
          ))}
          <button
            className="run-btn"
            onClick={handleCompare}
            disabled={!selected || loading}
          >
            {loading ? "Analyzing…" : "Run Comparison"}
          </button>
        </div>
        {error && <div className="error-box">{error}</div>}
      </section>

      {/* Ticker Profile (production-feel) */}
      {tickerProfile && (
        <section className="card">
          <h2>Ticker Profile</h2>
          <TickerProfilePanel profile={tickerProfile} />
        </section>
      )}

      {/* Evidence pack */}
      {ev && (
        <section className="card">
          <h2>
            Evidence Pack — {ev.company_name} ({ev.ticker})
          </h2>
          <p className="meta">
            {ev.exchange} · {ev.sector} · {ev.industry}
            {comparison?.evidence_hash && (
              <>
                {" "}
                · <code className="oc-hash">{comparison.evidence_hash.slice(0, 22)}…</code>
              </>
            )}
          </p>
          <p>{ev.summary}</p>
          <div className="metrics-grid">
            {ev.pe_ratio != null && <span>P/E: {ev.pe_ratio}</span>}
            {ev.pb_ratio != null && <span>P/B: {ev.pb_ratio}</span>}
            {ev.roic_pct != null && <span>ROIC: {ev.roic_pct}%</span>}
            {ev.fcf_ttm_usd != null && (
              <span>FCF: ${ev.fcf_ttm_usd.toLocaleString()}</span>
            )}
            {ev.revenue_growth_yoy_pct != null && (
              <span>Rev Growth: {ev.revenue_growth_yoy_pct}%</span>
            )}
            {ev.gross_margin_pct != null && (
              <span>Gross Margin: {ev.gross_margin_pct}%</span>
            )}
            {ev.net_margin_pct != null && (
              <span>Net Margin: {ev.net_margin_pct}%</span>
            )}
            {ev.debt_to_equity != null && <span>D/E: {ev.debt_to_equity}</span>}
          </div>
        </section>
      )}

      {/* Dual-model comparison */}
      {comparison && (
        <section className="card">
          <h2>Qwen vs DeepSeek — Overlay Comparison</h2>
          <OverlayComparisonPanel comparison={comparison} />
        </section>
      )}

      {/* Safety statement */}
      <section className="card safety-card">
        <h2>Safety Statement</h2>
        <p className="safety-text">
          LLMs do not execute trades; a human remains the portfolio manager.
        </p>
        <p className="safety-text">
          Pantheon Research is not an autonomous trading bot. It is a
          framework-first, data-governed, human-in-the-loop AI research
          operating system. This public repository is a sanitized vertical
          slice; the production system stays private.
        </p>
      </section>

      <footer>
        <p>
          Apache-2.0 · BUIDL_QUESTS 2026 (OPC / Super Individuals) ·{" "}
          <a
            href="https://github.com/0xjacobzhao-byte/pantheon-research-buidl-quests-2026"
            target="_blank"
            rel="noopener noreferrer"
          >
            GitHub
          </a>
        </p>
      </footer>
    </div>
  );
}

export default App;
