import { render, screen } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import ResearchOpsConsole, { NO_ALPHA_BANNER } from "./ResearchOpsConsole";

vi.mock("../../api", () => ({
  fetchResearchOpsReadiness: () =>
    Promise.resolve({
      schema_version: "1.0",
      as_of: "2026-07-02",
      no_alpha_claim: "no alpha claim",
      modules: [],
    }),
  fetchResearchOpsValidation: () =>
    Promise.resolve({
      pit_policy_vocabulary: [],
      record_kind_vocabulary: [],
      readiness_vocabulary: [],
      modules: [],
    }),
  fetchResearchOpsOutcomes: () =>
    Promise.resolve({
      outcome_status_vocabulary: [],
      performance_null_reason: "warming up",
      modules: [],
    }),
  fetchResearchOpsSummary: () =>
    Promise.resolve({
      total_modules: 14,
      readiness_distribution: {},
      public_performance_eligible_count: 0,
      modules_with_public_performance: 0,
      no_alpha_claim: "no alpha claim",
      scorecards: [],
    }),
}));

describe("ResearchOpsConsole", () => {
  it("renders the view and the exact no-alpha banner", async () => {
    render(<ResearchOpsConsole />);
    expect(await screen.findByTestId("no-alpha-banner")).toHaveTextContent(
      NO_ALPHA_BANNER
    );
    expect(screen.getByTestId("view-research-ops")).toBeInTheDocument();
  });
});
