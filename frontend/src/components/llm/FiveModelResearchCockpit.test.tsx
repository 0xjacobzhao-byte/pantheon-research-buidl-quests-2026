import { render, screen } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import FiveModelResearchCockpit from "./FiveModelResearchCockpit";

const CASE = {
  case_id: "nvda",
  ticker: "NVDA",
  market: "US",
  company_name: "NVIDIA",
  evidence_hash: "sha256:abc123abc123abc123abc123abc123",
};

vi.mock("../../api", () => ({
  fetchLlmProviders: () =>
    Promise.resolve({
      providers: [],
      status: {
        registered_providers: 0,
        provider_order: [],
        case_coverage: {},
        cases: [],
        note: "",
      },
    }),
  fetchLlmCases: () => Promise.resolve({ cases: [CASE], count: 1 }),
  fetchLlmCase: () => Promise.resolve({ case: CASE, overlays: [] }),
  fetchLlmComparison: () =>
    Promise.resolve({
      case: CASE,
      comparable_providers: [],
      provider_states: {},
      agreement_matrix: {
        factors: [],
        comparisons: 0,
        agreements: 0,
        agreement_score: null,
      },
      disagreement_matrix: [],
      confidence_spread: null,
      red_flags: {
        per_provider: {},
        shared_red_flag_themes: [],
        unique_red_flags: {},
        material_risk_disagreement: false,
      },
      missing_evidence: {
        per_provider: {},
        shared_missing_evidence: [],
        all_missing_evidence: [],
      },
      evidence_coverage: {
        per_provider: {},
        coverage_rank_spread: null,
        weak_evidence_providers: [],
      },
      human_review_required: false,
      human_review_reasons: [],
      winner: null,
      note: "Models compared; verdicts overlaid.",
    }),
}));

describe("FiveModelResearchCockpit", () => {
  it("renders the view and an explicit no-winner note", async () => {
    render(<FiveModelResearchCockpit />);
    expect(await screen.findByText(/No winner/)).toBeInTheDocument();
    expect(screen.getByTestId("view-llm")).toBeInTheDocument();
  });
});
