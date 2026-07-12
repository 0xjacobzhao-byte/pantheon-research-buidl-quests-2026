import { render, screen } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import BtcThreeLayerStack from "./BtcThreeLayerStack";

const STACK = {
  as_of: "2026-07-02",
  l1: {
    state: "neutral",
    label: "Range",
    triggered: false,
    available: true,
    coverage_ratio: null,
    confidence: null,
    rating_capped: null,
    score: null,
    primary_signal: "structure",
    layer_bias: "neutral",
    execution_effect: "none",
    source_timestamp: "2026-07-02",
  },
  l2: {
    guardian_state: "green",
    guardian_score: null,
    macro_score: null,
    long_gate: null,
    short_gate: null,
    hunter_state: "idle",
    hunter_score: null,
    architect_state: "idle",
    architect_score: null,
    risk_multiplier: 1,
    vol_scalar: null,
    regime: "neutral",
    final_signal_score: null,
    final_signal_direction: "flat",
    final_signal_conviction: null,
    missing_fields: [],
    source_timestamp: "2026-07-02",
  },
  l3: {
    state: "calm",
    risk_label_raw: "low",
    risk_score: null,
    confidence: null,
    mode: "normal",
    high_alert_mode: false,
    degraded_mode: false,
    primary_signal: "risk",
    posture_72h: "stable",
    triggers_fired_72h: null,
    metric_triggers: {},
    conditions_fired: [],
    source_timestamp: "2026-07-02",
  },
  macro_risk_budget: {
    regime: "neutral",
    confirmed_regime: "neutral",
    hard_stops_active: false,
    exposure_cap_pct: 60,
    final_exposure: 60,
  },
  resolved_posture: {
    outcome: "neutral_hold",
    reasons: ["layers aligned neutral"],
    layer_inputs: {},
    note: "Context only.",
  },
  missing_fields: { l2: [] },
  disclaimer: "Not a trade signal.",
};

vi.mock("../../api", () => ({
  fetchBtcStack: () => Promise.resolve(STACK),
  fetchBtcHistory: () =>
    Promise.resolve({
      cadence: "daily",
      count: 0,
      first: "",
      last: "",
      rows: [],
      l1_quality_distribution: {},
      l3_state_distribution: {},
      disclaimer: "",
    }),
  fetchBtcConflicts: () =>
    Promise.resolve({ examples: [], outcomes_vocabulary: [], note: "" }),
}));

describe("BtcThreeLayerStack", () => {
  it("renders the view and resolved posture", async () => {
    render(<BtcThreeLayerStack />);
    expect(await screen.findByTestId("btc-current-posture")).toBeInTheDocument();
    expect(screen.getByTestId("view-btc")).toBeInTheDocument();
    expect(screen.getByText("neutral_hold")).toBeInTheDocument();
  });
});
