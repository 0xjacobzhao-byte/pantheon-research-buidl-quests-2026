import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import OverlayComparisonPanel, { dataStateMeta } from "./OverlayComparisonPanel";
import type {
  ComparisonResult,
  QualitativeOverlay,
} from "../../api";

function overlay(overrides: Partial<QualitativeOverlay>): QualitativeOverlay {
  return {
    provider: "qwen",
    model: "qwen-plus",
    ticker: "MA",
    status: "OFFLINE_SAMPLE",
    takeaway: "Strong, durable network business.",
    assessment: {
      business_quality: "Excellent economics.",
      moat: "Wide two-sided network moat.",
      pricing_power: "Strong pricing power.",
      capital_allocation: "Disciplined buybacks.",
      red_flags: "Regulatory scrutiny.",
      confidence: 0.82,
      missing_evidence: ["No real-time interchange data"],
    },
    error_message: null,
    latency_ms: 1200,
    attempts: 1,
    prompt_version: "qwen-overlay-v1.1",
    output_schema_version: "overlay-assessment-1.0",
    usage: null,
    ...overrides,
  };
}

function comparison(overrides: Partial<ComparisonResult>): ComparisonResult {
  return {
    ticker: "MA",
    data_state: "OFFLINE_SAMPLE",
    qwen_status: "OFFLINE_SAMPLE",
    deepseek_status: "OFFLINE_SAMPLE",
    evidence: {} as ComparisonResult["evidence"],
    evidence_hash: "sha256:abc123def456abc123def456",
    qwen_overlay: overlay({ provider: "qwen" }),
    deepseek_overlay: overlay({ provider: "deepseek", model: "deepseek-chat" }),
    agreement_score: 0.78,
    agreement_level: "HIGH",
    qwen_tone: "conservative_positive",
    deepseek_tone: "positive",
    divergences: [],
    evidence_gaps: ["No real-time interchange data"],
    human_review_required: false,
    human_review_reason: null,
    ...overrides,
  };
}

describe("dataStateMeta", () => {
  it("labels known states and falls back gracefully", () => {
    expect(dataStateMeta("LIVE_DUAL").label).toMatch(/Live/);
    expect(dataStateMeta("BLOCKED").label).toMatch(/Blocked/);
    expect(dataStateMeta("WHATEVER").label).toBe("WHATEVER");
  });
});

describe("OverlayComparisonPanel — offline dual", () => {
  it("renders both provider cards", () => {
    render(<OverlayComparisonPanel comparison={comparison({})} />);
    expect(screen.getByText("Qwen Cloud")).toBeInTheDocument();
    expect(screen.getByText("DeepSeek")).toBeInTheDocument();
    expect(screen.getByTestId("provider-card-qwen")).toBeInTheDocument();
    expect(screen.getByTestId("provider-card-deepseek")).toBeInTheDocument();
  });

  it("shows data state, agreement score and evidence hash", () => {
    render(<OverlayComparisonPanel comparison={comparison({})} />);
    expect(screen.getByText(/Offline Sample/)).toBeInTheDocument();
    expect(screen.getByText(/0\.78 · HIGH/)).toBeInTheDocument();
    expect(screen.getByText(/sha256:abc123/)).toBeInTheDocument();
  });

  it("does not flag human review when agreement is high", () => {
    render(<OverlayComparisonPanel comparison={comparison({})} />);
    expect(screen.getByText("Not Required")).toBeInTheDocument();
    expect(screen.queryByText(/Human review gate engaged/)).toBeNull();
  });
});

describe("OverlayComparisonPanel — major divergence", () => {
  it("engages the human-review gate with a reason", () => {
    const c = comparison({
      agreement_score: 0.3,
      agreement_level: "LOW",
      divergences: [
        {
          field: "moat",
          qwen_view: "wide",
          deepseek_view: "narrow",
          severity: "major",
        },
      ],
      human_review_required: true,
      human_review_reason: "At least one major divergence between providers.",
    });
    render(<OverlayComparisonPanel comparison={c} />);
    expect(screen.getByText(/Human review gate engaged/)).toBeInTheDocument();
    expect(screen.getByText(/major divergence/)).toBeInTheDocument();
    expect(screen.getByText("moat")).toBeInTheDocument();
  });
});

describe("OverlayComparisonPanel — fail-closed PARTIAL", () => {
  it("shows NOT COMPARABLE and surfaces the failed provider", () => {
    const c = comparison({
      data_state: "PARTIAL",
      qwen_status: "OFFLINE_SAMPLE",
      deepseek_status: "API_ERROR",
      deepseek_overlay: overlay({
        provider: "deepseek",
        model: "deepseek-chat",
        status: "API_ERROR",
        assessment: null,
        takeaway: "",
        error_message: "Upstream 500 from provider.",
      }),
      agreement_score: null,
      agreement_level: "NOT_COMPARABLE",
      human_review_required: true,
      human_review_reason:
        "Only Qwen returned a usable assessment; comparison not possible.",
    });
    render(<OverlayComparisonPanel comparison={c} />);
    expect(screen.getByText("NOT COMPARABLE")).toBeInTheDocument();
    expect(screen.getByText(/Fail-closed:/)).toBeInTheDocument();
    expect(screen.getByText(/Upstream 500/)).toBeInTheDocument();
    // A fail-closed provider is never averaged into a divergence score.
    expect(screen.getByText(/Divergence analysis is skipped/)).toBeInTheDocument();
  });
});
