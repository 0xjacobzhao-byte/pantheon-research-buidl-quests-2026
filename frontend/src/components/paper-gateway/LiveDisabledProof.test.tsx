import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import LiveDisabledProof from "./LiveDisabledProof";
import type { LiveDisabledProof as LiveDisabledProofData } from "../../api";

const data: LiveDisabledProofData = {
  live_enabled: false,
  broker_connected: false,
  real_order_path: false,
  paper_only: true,
  broker_adapter_present: false,
  llm_actor_intents: 3,
  llm_actor_paper_filled: 1,
  llm_actor_auto_executed_without_approval: 0,
  live_disabled: true,
  attestation: "No live order path exists in this build.",
};

describe("LiveDisabledProof", () => {
  it("renders the LIVE disabled banner and attestation", () => {
    render(<LiveDisabledProof data={data} />);
    expect(screen.getByTestId("live-disabled-proof")).toBeInTheDocument();
    expect(screen.getByText(/LIVE TRADING DISABLED/)).toBeInTheDocument();
    expect(screen.getByText(/No live order path exists/)).toBeInTheDocument();
    expect(screen.getByText("live_enabled")).toBeInTheDocument();
  });
});
