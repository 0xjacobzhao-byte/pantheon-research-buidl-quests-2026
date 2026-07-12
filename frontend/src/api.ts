const API_BASE = "/api";

export interface ProjectInfo {
  name: string;
  description: string;
  author: string;
  github: string;
  license: string;
  version: string;
  demo_mode: string;
  architecture_layers: string[];
  safety_statement: string;
}

export interface EquityEvidence {
  ticker: string;
  company_name: string;
  exchange: string;
  sector: string;
  industry: string;
  market_cap_usd: number;
  pe_ratio: number | null;
  pb_ratio: number | null;
  roic_pct: number | null;
  fcf_ttm_usd: number | null;
  revenue_growth_yoy_pct: number | null;
  gross_margin_pct: number | null;
  net_margin_pct: number | null;
  dividend_yield_pct: number | null;
  debt_to_equity: number | null;
  summary: string;
}

export interface EvidenceSource {
  group: string;
  label: string;
  origin: string;
  as_of: string;
}

export interface EvidenceProvenance {
  evidence_schema_version: string;
  evidence_hash: string;
  generated_at_utc: string;
  sources: EvidenceSource[];
  redaction_note: string;
}

export interface EvidencePack {
  evidence: EquityEvidence;
  provenance: EvidenceProvenance;
}

export interface OverlayAssessment {
  business_quality: string;
  moat: string;
  pricing_power: string;
  capital_allocation: string;
  red_flags: string;
  confidence: number;
  missing_evidence: string[];
}

export interface TokenUsage {
  prompt_tokens: number | null;
  completion_tokens: number | null;
  total_tokens: number | null;
  estimated_cost_usd: number | null;
}

export interface QualitativeOverlay {
  provider: string;
  model: string;
  ticker: string;
  status: string;
  takeaway: string;
  assessment: OverlayAssessment | null;
  error_message: string | null;
  latency_ms: number | null;
  attempts: number;
  prompt_version: string | null;
  output_schema_version: string | null;
  usage: TokenUsage | null;
}

export interface Divergence {
  field: string;
  qwen_view: string;
  deepseek_view: string;
  severity: string;
}

export interface ComparisonResult {
  ticker: string;
  data_state: string;
  qwen_status: string;
  deepseek_status: string;
  evidence: EquityEvidence;
  evidence_hash: string | null;
  qwen_overlay: QualitativeOverlay;
  deepseek_overlay: QualitativeOverlay;
  agreement_score: number | null;
  agreement_level: string;
  qwen_tone: string;
  deepseek_tone: string;
  divergences: Divergence[];
  evidence_gaps: string[];
  human_review_required: boolean;
  human_review_reason: string | null;
}

export interface DatabaseProof {
  provider: string;
  configured: boolean;
  connected: boolean | null;
  role: string;
  production_data_migrated: boolean;
  note: string;
}

export interface AlibabaCloudProof {
  schema_version: string;
  project: string;
  cloud_provider: string;
  host_runtime: string;
  alibaba_hosted: boolean;
  backend_runtime: string;
  reverse_proxy: string;
  frontend_source: string;
  qwen_provider: string;
  qwen_base_url: string;
  qwen_model: string;
  qwen_configured: boolean;
  dashscope_api_key_configured: boolean;
  demo_mode: string;
  region: string;
  git_sha: string;
  timestamp_utc: string;
  proof_endpoints: Record<string, string>;
  database: DatabaseProof;
  safe_claims: string[];
  non_claims: string[];
}

export interface QwenConfig {
  provider: string;
  base_url: string;
  model: string;
  integration_type: string;
  prompt_version: string;
  output_schema_version: string;
  credential_configured: boolean;
  demo_mode: string;
}

export interface DataQualityReport {
  generated_at_utc: string;
  demo_mode: string;
  mode: string;
  providers: {
    qwen_configured: boolean;
    qwen_model: string;
    deepseek_configured: boolean;
    deepseek_model: string;
  };
  alibaba_proof_reachable: boolean;
  sample_evidence_coverage: {
    tickers: string[];
    evidence_packs_present: number;
    healthy_comparisons: number;
  };
  overlay_statuses: Array<Record<string, unknown>>;
  fail_closed_states: string[];
  governance_note: string;
}

export interface ModuleSnapshot {
  key: string;
  title: string;
  group: string;
  data_state: string;
  freshness: string;
  validation_state: string;
  role: string;
  what_not_to_infer: string;
  sample_endpoint: string;
  headline: string;
}

export interface ModuleSnapshotGridData {
  schema_version: string;
  as_of: string;
  generated_at_utc: string;
  disclaimer: string;
  modules: ModuleSnapshot[];
}

export interface DemoFlowStep {
  step: number;
  title: string;
  description: string;
}

export interface DemoFlow {
  title: string;
  steps: DemoFlowStep[];
  architecture_layers: string[];
  safety_statement: string;
}

async function getJson<T>(path: string): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`);
  if (!res.ok) throw new Error(`Failed: ${res.status} ${res.statusText}`);
  return res.json() as Promise<T>;
}

export const fetchProject = () => getJson<ProjectInfo>("/project");
export const fetchDemoFlow = () => getJson<DemoFlow>("/demo-flow");
export const fetchComparison = (ticker: string) =>
  getJson<ComparisonResult>(`/comparison/${ticker}`);
export const fetchAlibabaProof = () =>
  getJson<AlibabaCloudProof>("/proof/alibaba-cloud");
export const fetchQwenConfig = () => getJson<QwenConfig>("/alibaba/qwen-config");
export const fetchDataQuality = () => getJson<DataQualityReport>("/data-quality");
export const fetchModules = () => getJson<ModuleSnapshotGridData>("/modules");

// ---------------------------------------------------------------------------
// Ticker Profile
// ---------------------------------------------------------------------------

export interface KpiMetric {
  name: string;
  value: string | number;
  signal: string;
}

export interface KpiCard {
  label: string;
  metrics: KpiMetric[];
  summary: string;
}

export interface EvidencePackSummary {
  sources: number;
  hash_prefix: string;
  as_of: string;
  fields_covered: string[];
}

export interface HumanReviewStatus {
  status: string;
  reason: string | null;
  queue_position: string | null;
}

export interface TickerProfile {
  ticker: string;
  company_name: string;
  exchange: string;
  sector: string;
  industry: string;
  market_cap_usd: number;
  kpi_cards: {
    valuation: KpiCard;
    quality: KpiCard;
    growth: KpiCard;
    anchors: KpiCard;
    technical: KpiCard;
  };
  evidence_pack_summary: EvidencePackSummary;
  human_review: HumanReviewStatus;
}

// ---------------------------------------------------------------------------
// Provider Health
// ---------------------------------------------------------------------------

export interface ProviderHealthData {
  schema_version: string;
  generated_at_utc: string;
  demo_mode: string;
  qwen: {
    provider: string;
    configured: boolean;
    model: string;
    status: string;
    fail_closed_active: boolean;
    live_mode_gated: boolean;
  };
  deepseek: {
    provider: string;
    configured: boolean;
    model: string;
    status: string;
    fail_closed_active: boolean;
    live_mode_gated: boolean;
  };
  sample_evidence: {
    present: boolean;
    tickers: string[];
    count: number;
  };
  alibaba_proof: {
    documented: boolean;
    endpoint: string;
  };
  offline_mode: {
    available: boolean;
    active: boolean;
  };
  live_mode: {
    gated: boolean;
    requires: string[];
  };
  secrets_exposed: boolean;
  fail_closed_active: boolean;
  note: string;
}

// ---------------------------------------------------------------------------
// Validation Timeline
// ---------------------------------------------------------------------------

export interface TimelineStage {
  stage: number;
  name: string;
  status: string;
  description: string;
  evidence: string;
}

export interface ValidationTimelineData {
  schema_version: string;
  generated_at_utc: string;
  stance: string;
  stages: TimelineStage[];
  non_claims: string[];
  illustrative_demo_summary: {
    note: string;
    cohort: string;
    signals_captured: number;
    evidence_hashed: number;
    models_recorded: number;
    awaiting_forward_window: number;
    matured_and_scored: number;
    performance_claim: string;
  };
}

// ---------------------------------------------------------------------------
// Mini Panels (Macro / Market Pulse / FICC)
// ---------------------------------------------------------------------------

export interface MiniIndicator {
  name: string;
  value: string;
  signal: string;
  note: string;
}

export interface MacroMiniPanelData {
  schema_version: string;
  generated_at_utc: string;
  data_state: string;
  disclaimer: string;
  regime: Record<string, string>;
  indicators: MiniIndicator[];
  headline: string;
  what_not_to_infer: string;
}

export interface MarketPulseMiniPanelData {
  schema_version: string;
  generated_at_utc: string;
  data_state: string;
  disclaimer: string;
  market: Record<string, string>;
  indicators: MiniIndicator[];
  headline: string;
  what_not_to_infer: string;
}

export interface FiccMiniPanelData {
  schema_version: string;
  generated_at_utc: string;
  data_state: string;
  disclaimer: string;
  fixed_income: Record<string, string>;
  fx: Record<string, string>;
  commodity: Record<string, string>;
  headline: string;
  what_not_to_infer: string;
}

// ---------------------------------------------------------------------------
// New fetch functions
// ---------------------------------------------------------------------------

export const fetchTickerProfile = (ticker: string) =>
  getJson<TickerProfile>(`/ticker-profile/${ticker}`);
export const fetchTickerProfiles = () =>
  getJson<{ tickers: string[] }>("/ticker-profiles");
export const fetchProviderHealth = () =>
  getJson<ProviderHealthData>("/provider-health");
export const fetchValidationTimeline = () =>
  getJson<ValidationTimelineData>("/validation-timeline");
export const fetchMacroMini = () =>
  getJson<MacroMiniPanelData>("/mini/macro");
export const fetchMarketPulseMini = () =>
  getJson<MarketPulseMiniPanelData>("/mini/market-pulse");
export const fetchFiccMini = () =>
  getJson<FiccMiniPanelData>("/mini/ficc");

// ===========================================================================
// Shared POST helper
// ===========================================================================

async function postJson<T>(path: string, body?: unknown): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: body != null ? JSON.stringify(body) : undefined,
  });
  if (!res.ok) throw new Error(`Failed: ${res.status} ${res.statusText}`);
  return res.json() as Promise<T>;
}

// ===========================================================================
// FIVE-MODEL LLM
// ===========================================================================

export interface LlmProvider {
  provider: string;
  display_name: string;
  model: string;
  family: string;
  credential_configured: boolean;
  default_runs_live: boolean;
  mode: string;
}

export interface LlmProvidersData {
  providers: LlmProvider[];
  status: {
    registered_providers: number;
    provider_order: string[];
    case_coverage: Record<string, Record<string, string>>;
    cases: string[];
    note: string;
  };
}

export interface LlmCase {
  case_id: string;
  ticker: string;
  market: string;
  company_name: string;
  evidence_hash: string;
}

export interface LlmCasesData {
  cases: LlmCase[];
  count: number;
}

export interface VerdictNote {
  verdict: string;
  note: string;
}

export interface ModelOverlay {
  provider: string;
  model: string;
  ticker: string;
  market: string;
  generated_at: string;
  data_state: string;
  evidence_hash: string;
  evidence_coverage: any;
  confidence: number | null;
  business_quality: VerdictNote | null;
  moat: VerdictNote | null;
  pricing_power: VerdictNote | null;
  management_capital_allocation: VerdictNote | null;
  valuation_view: VerdictNote | null;
  red_flags: string[];
  missing_evidence: string[];
  risk_summary: any;
  tone: any;
  human_review_required: boolean;
  source_refs: string[];
  error_message: string | null;
}

export interface LlmCaseDetail {
  case: LlmCase;
  overlays: ModelOverlay[];
}

export interface AgreementFactor {
  factor: string;
  verdicts: Record<string, string>;
  distinct_verdicts: string[];
  comparable: boolean;
  agreement: boolean;
}

export interface AgreementMatrix {
  factors: AgreementFactor[];
  comparisons: number;
  agreements: number;
  agreement_score: number | null;
}

export interface DisagreementFactor {
  factor: string;
  verdicts: Record<string, string>;
  distinct_verdicts: string[];
}

export interface LlmComparison {
  case: LlmCase;
  comparable_providers: string[];
  provider_states: Record<string, string>;
  agreement_matrix: AgreementMatrix;
  disagreement_matrix: DisagreementFactor[];
  confidence_spread: number | null;
  red_flags: {
    per_provider: Record<string, string[]>;
    shared_red_flag_themes: string[];
    unique_red_flags: Record<string, string[]>;
    material_risk_disagreement: boolean;
  };
  missing_evidence: {
    per_provider: Record<string, string[]>;
    shared_missing_evidence: string[];
    all_missing_evidence: string[];
  };
  evidence_coverage: {
    per_provider: Record<string, string | null>;
    coverage_rank_spread: number | null;
    weak_evidence_providers: string[];
  };
  human_review_required: boolean;
  human_review_reasons: string[];
  winner: null;
  note: string;
}

export interface LlmAgreementData {
  case: LlmCase;
  agreement_matrix: AgreementMatrix;
}

export const fetchLlmProviders = () => getJson<LlmProvidersData>("/llm/providers");
export const fetchLlmCases = () => getJson<LlmCasesData>("/llm/cases");
export const fetchLlmCase = (id: string) => getJson<LlmCaseDetail>(`/llm/case/${id}`);
export const fetchLlmComparison = (id: string) =>
  getJson<LlmComparison>(`/llm/comparison/${id}`);
export const fetchLlmAgreement = (id: string) =>
  getJson<LlmAgreementData>(`/llm/agreement/${id}`);

// ===========================================================================
// MACRO
// ===========================================================================

export interface MacroRiskBudget {
  version: string;
  score: number;
  regime: string;
  confirmed_regime: string;
  regime_confidence: any;
  coverage: any;
  hard_stops_active: boolean;
  hard_stops_triggered: string[];
  final_exposure: any;
  exposure_cap_pct: number;
  anomaly_flags: string[];
  as_of: string;
  freshness: any;
  hysteresis: {
    raw_regime: string;
    confirmed_regime: string;
    pending_regime: string;
    observations_required: number;
    observations_seen: number;
    transition_pending: boolean;
    reason: string;
  } | null;
  degraded_reason: string | null;
}

export interface MacroHistoryData {
  count: number;
  history: MacroRiskBudget[];
}

export interface MacroScenario {
  id: string;
  label: string;
  risk_budget: MacroRiskBudget;
}

export interface MacroScenariosData {
  scenarios: MacroScenario[];
}

export const fetchMacroRiskBudget = () =>
  getJson<MacroRiskBudget>("/macro/risk-budget");
export const fetchMacroHistory = () => getJson<MacroHistoryData>("/macro/history");
export const fetchMacroScenarios = () =>
  getJson<MacroScenariosData>("/macro/scenarios");

// ===========================================================================
// RESEARCH OPS
// ===========================================================================

export interface ReadinessModule {
  module: string;
  display_name: string;
  readiness: string;
  validation_method: string;
  sample_count: number;
  outcome_maturity: string;
  record_kind: string;
  pit_policy: string;
  public_performance_eligible: boolean | null;
  limitations: string[];
  next_action: string;
}

export interface ResearchOpsReadiness {
  schema_version: string;
  as_of: string;
  no_alpha_claim: string;
  modules: ReadinessModule[];
}

export interface ResearchOpsValidation {
  pit_policy_vocabulary: string[];
  record_kind_vocabulary: string[];
  readiness_vocabulary: string[];
  modules: {
    module: string;
    validation_method: string;
    record_kind: string;
    pit_policy: string;
    public_performance_eligible: boolean | null;
    record_kind_policy: string;
  }[];
}

export interface OutcomeModule {
  module: string;
  sample_count: number;
  outcome_maturity: string;
  realized_outcomes: number;
  open_outcomes: number;
  warming_up: boolean;
  public_performance_eligible: boolean | null;
  performance: {
    hit_rate: null;
    avg_return_pct: null;
    sharpe: null;
    max_drawdown_pct: null;
    reason: string;
  };
  sample_timeline: { stage: string; count: number }[];
}

export interface ResearchOpsOutcomes {
  outcome_status_vocabulary: string[];
  performance_null_reason: string;
  modules: OutcomeModule[];
}

export interface ResearchOpsSummary {
  total_modules: number;
  readiness_distribution: Record<string, number>;
  public_performance_eligible_count: number;
  modules_with_public_performance: number;
  no_alpha_claim: string;
  scorecards: {
    module: string;
    display_name: string;
    readiness: string;
    record_kind: string;
    pit_policy: string;
    public_performance_eligible: boolean | null;
    sample_count: number;
    outcome_maturity: string;
  }[];
}

export const fetchResearchOpsReadiness = () =>
  getJson<ResearchOpsReadiness>("/research-ops/readiness");
export const fetchResearchOpsValidation = () =>
  getJson<ResearchOpsValidation>("/research-ops/validation");
export const fetchResearchOpsOutcomes = () =>
  getJson<ResearchOpsOutcomes>("/research-ops/outcomes");
export const fetchResearchOpsSummary = () =>
  getJson<ResearchOpsSummary>("/research-ops/summary");

// ===========================================================================
// DATA LINEAGE
// ===========================================================================

export interface IngestRun {
  id: number;
  job_name: string;
  started_at: string;
  finished_at: string;
  status: string;
  metrics_ingested: number;
  series_fetched: number;
  duration_ms: number;
  errors_json: any;
}

export interface IngestRunsData {
  ingest_runs: IngestRun[];
}

export interface DpProviderHealth {
  provider: string;
  last_success_at: string;
  last_failure_at: string | null;
  consecutive_failures: number;
  daily_calls_used: number;
  daily_calls_limit: number;
  avg_latency_ms: number;
  status: string;
}

export interface DpProviderHealthData {
  provider_health: DpProviderHealth[];
}

export interface DpObservation {
  id: number;
  domain: string;
  metric_id: string;
  instrument_id: string;
  as_of_date: string;
  value: number;
  unit: string;
  source: string;
  ingested_at: string;
  quality_state: string;
  revision_sequence: number;
  content_hash: string;
}

export interface DpObservationsData {
  observations: DpObservation[];
}

export interface DpVersion {
  id: number;
  revision_sequence: number;
  value: number;
  unit: string;
  source: string;
  quality_state: string;
  source_vintage: string;
  vintage_at: string;
  version_hash: string;
}

export interface DpVersionsData {
  observation_id: number;
  versions: DpVersion[];
}

export interface LineageNode {
  layer: string;
  entity: string;
  id: any;
  key: string;
  detail: any;
}

export interface LineageConsumer {
  provider: string;
  model: string;
  ticker: string;
  overlay_ref: string;
  prompt_version: string;
}

export interface LineageData {
  evidence_hash: string;
  found: boolean;
  nodes: LineageNode[];
  llm_consumers: LineageConsumer[];
  note: string;
}

export const DEFAULT_LINEAGE_HASH =
  "sha256:b1b1a99dc8d5e218d93487c23166a804c3b69684e3781c6fa10f5117efdce4c9";

export const fetchIngestRuns = () =>
  getJson<IngestRunsData>("/data-platform/ingest-runs");
export const fetchDpProviderHealth = () =>
  getJson<DpProviderHealthData>("/data-platform/provider-health");
export const fetchDpObservations = () =>
  getJson<DpObservationsData>("/data-platform/observations");
export const fetchDpVersions = (id: number | string) =>
  getJson<DpVersionsData>(`/data-platform/versions/${id}`);
export const fetchLineage = (evidenceHash: string) =>
  getJson<LineageData>(`/data-platform/lineage/${evidenceHash}`);

// ===========================================================================
// PAPER GATEWAY
// ===========================================================================

export interface PaperGatewayStatus {
  live_enabled: boolean;
  broker_connected: boolean;
  real_order_path: boolean;
  paper_only: boolean;
  broker_adapter_present: boolean;
  llm_can_execute: boolean;
  llm_can_approve: boolean;
  human_approval_required: boolean;
  audit_append_only: boolean;
  note: string;
}

export interface PaperProvenance {
  source_module: string;
  source_verdict_ref: string;
  validation_maturity: string;
  macro_risk_budget_ref: string;
  data_freshness_state: string;
  kill_switch_snapshot: string;
  risk_policy_snapshot: string;
  actor_identity: string;
  actor_type: string;
  created_by_surface: string;
  audit_hash: string;
}

export interface PaperFill {
  fill_id: string;
  filled_quantity: number;
  fill_price: number;
  slippage_bps: number;
  venue: string;
  is_paper: boolean;
  filled_at: string;
}

export interface PaperIntent {
  intent_id: string;
  ticker: string;
  asset_class: string;
  sector: string;
  side: string;
  quantity: number;
  limit_price: any;
  notional_usd: any;
  state: string;
  provenance: PaperProvenance;
  created_at: string;
  rejection_reasons: string[];
  approved_by: string | null;
  paper_fill: PaperFill | null;
}

export interface PaperIntentsData {
  intents: PaperIntent[];
}

export interface ApprovalCardData {
  intent_id: string;
  ticker: string;
  side: string;
  quantity: number;
  notional_usd: any;
  validation_maturity: string;
  macro_risk_budget_ref: string;
  data_freshness_state: string;
  kill_switch_snapshot: string;
  provenance_complete: boolean;
  risk_gate_passed: boolean;
  rejection_reasons: string[];
  requires_human_approval: boolean;
  llm_can_approve: boolean;
  live_enabled: boolean;
  operator_note: string;
}

export interface PaperIntentDetail {
  intent: PaperIntent;
  approval_card: ApprovalCardData | null;
}

export interface AuditEvent {
  seq: number;
  intent_id: string;
  event_type: string;
  actor_type: string;
  actor_identity: string;
  detail: any;
  at: string;
  prev_hash: string | null;
  event_hash: string;
}

export interface AuditData {
  events: AuditEvent[];
}

export interface ProvenanceCompleteness {
  total_intents: number;
  fully_provenanced: number;
  completeness_pct: number;
  audit_chain_intact: boolean;
  intents: {
    intent_id: string;
    provenance_complete: boolean;
    audit_hash_valid: boolean;
    missing_fields: string[];
  }[];
}

export interface LiveDisabledProof {
  live_enabled: boolean;
  broker_connected: boolean;
  real_order_path: boolean;
  paper_only: boolean;
  broker_adapter_present: boolean;
  llm_actor_intents: number;
  llm_actor_paper_filled: number;
  llm_actor_auto_executed_without_approval: number;
  live_disabled: boolean;
  attestation: string;
}

export const fetchPaperGatewayStatus = () =>
  getJson<PaperGatewayStatus>("/paper-gateway/status");
export const fetchPaperIntents = () =>
  getJson<PaperIntentsData>("/paper-gateway/intents");
export const fetchPaperIntent = (id: string) =>
  getJson<PaperIntentDetail>(`/paper-gateway/intent/${id}`);
export const fetchPaperAudit = (intentId?: string) =>
  getJson<AuditData>(
    `/paper-gateway/audit${intentId ? `?intent_id=${intentId}` : ""}`
  );
export const fetchProvenanceCompleteness = () =>
  getJson<ProvenanceCompleteness>("/paper-gateway/provenance-completeness");
export const fetchLiveDisabledProof = () =>
  getJson<LiveDisabledProof>("/paper-gateway/live-disabled-proof");
export const approvePaperIntent = (id: string, operator: string) =>
  postJson<PaperIntent>(`/paper-gateway/intent/${id}/approve`, { operator });
export const simulatePaperIntent = (id: string) =>
  postJson<PaperIntent>(`/paper-gateway/intent/${id}/simulate`);
export const rejectPaperIntent = (id: string, operator: string, note: string) =>
  postJson<PaperIntent>(`/paper-gateway/intent/${id}/reject`, { operator, note });

// ===========================================================================
// BTC
// ===========================================================================

export interface BtcL1 {
  state: string;
  label: string;
  triggered: boolean;
  available: boolean;
  coverage_ratio: any;
  confidence: any;
  rating_capped: any;
  score: any;
  primary_signal: string;
  layer_bias: string;
  execution_effect: string;
  source_timestamp: string;
}

export interface BtcL2 {
  guardian_state: string;
  guardian_score: any;
  macro_score: any;
  long_gate: any;
  short_gate: any;
  hunter_state: string;
  hunter_score: any;
  architect_state: string;
  architect_score: any;
  risk_multiplier: any;
  vol_scalar: any;
  regime: string;
  final_signal_score: any;
  final_signal_direction: string;
  final_signal_conviction: any;
  missing_fields: string[];
  source_timestamp: string;
}

export interface BtcL3 {
  state: string;
  risk_label_raw: string;
  risk_score: any;
  confidence: any;
  mode: string;
  high_alert_mode: boolean;
  degraded_mode: boolean;
  primary_signal: string;
  posture_72h: string;
  triggers_fired_72h: any;
  metric_triggers: Record<string, boolean>;
  conditions_fired: string[];
  source_timestamp: string;
}

export interface BtcStack {
  as_of: string;
  l1: BtcL1;
  l2: BtcL2;
  l3: BtcL3;
  macro_risk_budget: {
    regime: string;
    confirmed_regime: string;
    hard_stops_active: boolean;
    exposure_cap_pct: number;
    final_exposure: any;
  };
  resolved_posture: {
    outcome: string;
    reasons: string[];
    layer_inputs: Record<string, any>;
    note: string;
  };
  missing_fields: { l2: string[] };
  disclaimer: string;
}

export interface BtcHistoryRow {
  date: string;
  btc_price: number;
  final_signal_label: string;
  final_signal_value: number;
  guardian_status: string;
  regime: string;
  risk_multiplier: any;
  bottom_model_state: string;
  bottom_model_label: string;
  bottom_score: any;
  risk_radar_state: string;
  risk_radar_label: string;
  risk_score: any;
  fear_greed: any;
  fear_greed_bucket: string;
  mvrv: any;
  l1_quality: string;
  l2_quality: string;
  l3_quality: string;
  is_reconstructed: boolean;
}

export interface BtcHistoryData {
  cadence: string;
  count: number;
  first: string;
  last: string;
  rows: BtcHistoryRow[];
  l1_quality_distribution: Record<string, number>;
  l3_state_distribution: Record<string, number>;
  disclaimer: string;
}

export interface BtcConflict {
  id: string;
  title: string;
  inputs: { l1: any; l2: any; l3: any; macro: any };
  resolved_outcome: string;
  expected_outcome: string;
  matches_expected: boolean;
  reasons: string[];
}

export interface BtcConflictsData {
  examples: BtcConflict[];
  outcomes_vocabulary: string[];
  note: string;
}

export interface BtcPosture {
  as_of: string;
  outcome: string;
  reasons: string[];
  layer_inputs: Record<string, any>;
  note: string;
}

export const fetchBtcStack = () => getJson<BtcStack>("/btc/stack");
export const fetchBtcHistory = (limit = 60) =>
  getJson<BtcHistoryData>(`/btc/history?limit=${limit}`);
export const fetchBtcConflicts = () => getJson<BtcConflictsData>("/btc/conflicts");
export const fetchBtcCurrentPosture = () =>
  getJson<BtcPosture>("/btc/current-posture");

// ===========================================================================
// JUDGE
// ===========================================================================

export interface JudgeFlowStep {
  step: number;
  title: string;
  endpoint: string;
  status: string;
  detail: string;
}

export interface JudgeFullDemo {
  title: string;
  anchor_case: string;
  evidence_hash: string;
  equity_flow: JudgeFlowStep[];
  btc_flow: JudgeFlowStep[];
  modules: string[];
  safety: {
    live_enabled: boolean;
    llm_can_execute: boolean;
    broker_connected: boolean;
    offline_first: boolean;
  };
  note: string;
}

export const fetchJudgeFullDemo = () => getJson<JudgeFullDemo>("/judge/full-demo");
