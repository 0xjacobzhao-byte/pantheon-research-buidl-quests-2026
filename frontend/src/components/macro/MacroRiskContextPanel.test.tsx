import { render, screen } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import MacroRiskContextPanel from "./MacroRiskContextPanel";

const BUDGET = {
  version: "1.0",
  score: 0.42,
  regime: "neutral",
  confirmed_regime: "risk_off",
  regime_confidence: null,
  coverage: null,
  hard_stops_active: true,
  hard_stops_triggered: ["vol_spike"],
  final_exposure: 25,
  exposure_cap_pct: 25,
  anomaly_flags: [],
  as_of: "2026-07-02",
  freshness: "fresh",
  hysteresis: null,
  degraded_reason: null,
};

vi.mock("../../api", () => ({
  fetchMacroRiskBudget: () => Promise.resolve(BUDGET),
  fetchMacroHistory: () => Promise.resolve({ count: 1, history: [BUDGET] }),
  fetchMacroScenarios: () =>
    Promise.resolve({
      scenarios: [
        { id: "valid", label: "Valid inputs", risk_budget: BUDGET },
      ],
    }),
}));

describe("MacroRiskContextPanel", () => {
  it("renders the view and the confirmed regime", async () => {
    render(<MacroRiskContextPanel />);
    expect(await screen.findByText("Macro Risk Budget")).toBeInTheDocument();
    expect(screen.getByTestId("view-macro")).toBeInTheDocument();
    expect(screen.getAllByText(/risk_off/).length).toBeGreaterThan(0);
  });
});
