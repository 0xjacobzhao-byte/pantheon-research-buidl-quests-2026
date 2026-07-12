import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import ModuleSnapshotGrid from "./ModuleSnapshotGrid";
import type { ModuleSnapshotGridData, ModuleSnapshot } from "../api";

function mod(overrides: Partial<ModuleSnapshot>): ModuleSnapshot {
  return {
    key: "macro",
    title: "Macro Regime",
    group: "Macro",
    data_state: "CONTEXT_ONLY",
    freshness: "bundled sample as-of 2026-07-02",
    validation_state: "CONTEXT_ONLY",
    role: "Cross-asset regime dashboard",
    what_not_to_infer: "Not a live macro nowcast.",
    sample_endpoint: "/api/modules#macro",
    headline: "Regime: late-cycle (illustrative)",
    ...overrides,
  };
}

function grid(mods: ModuleSnapshot[]): ModuleSnapshotGridData {
  return {
    schema_version: "module-snapshots-1.0",
    as_of: "2026-07-02",
    generated_at_utc: "2026-07-02T12:00:00Z",
    disclaimer: "Context-only snapshots demonstrating system scope.",
    modules: mods,
  };
}

describe("ModuleSnapshotGrid", () => {
  it("renders a card per module with title and data_state", () => {
    const g = grid([
      mod({ key: "macro", title: "Macro Regime", group: "Macro" }),
      mod({
        key: "fx",
        title: "FX",
        group: "FICC",
        data_state: "CONTEXT_ONLY",
        validation_state: "SIGNAL_ONLY",
      }),
      mod({
        key: "data_quality",
        title: "Data Quality",
        group: "Research-Ops",
        data_state: "LIVE_IN_PROCESS",
        validation_state: "GOVERNANCE",
      }),
    ]);
    render(<ModuleSnapshotGrid grid={g} />);

    expect(screen.getByTestId("module-snapshot-grid")).toBeInTheDocument();
    expect(screen.getByText("Macro Regime")).toBeInTheDocument();
    expect(screen.getByText("FX")).toBeInTheDocument();
    expect(screen.getByText("Data Quality")).toBeInTheDocument();
    expect(screen.getByTestId("module-card-fx")).toBeInTheDocument();
    // data_state badge is shown
    expect(screen.getByText("LIVE_IN_PROCESS")).toBeInTheDocument();
  });

  it("shows the honest 'what not to infer' caveat and endpoint on each card", () => {
    const g = grid([
      mod({
        key: "commodity",
        title: "Commodity",
        group: "FICC",
        what_not_to_infer: "No fair-value band is published here.",
        sample_endpoint: "/api/modules#commodity",
      }),
    ]);
    render(<ModuleSnapshotGrid grid={g} />);
    expect(screen.getByText(/No fair-value band is published/)).toBeInTheDocument();
    expect(screen.getByText("/api/modules#commodity")).toBeInTheDocument();
    expect(screen.getByText(/Don't infer:/)).toBeInTheDocument();
  });

  it("renders the scope disclaimer and as-of footer", () => {
    render(<ModuleSnapshotGrid grid={grid([mod({})])} />);
    expect(screen.getByText(/Context-only snapshots/)).toBeInTheDocument();
    // Footer is uniquely identified by the grid schema version.
    expect(screen.getByText(/Grid schema module-snapshots-1.0/)).toBeInTheDocument();
  });
});
