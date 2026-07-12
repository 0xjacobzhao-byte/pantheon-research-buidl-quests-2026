import { render, screen } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import DataLineageExplorer from "./DataLineageExplorer";

vi.mock("../../api", () => ({
  DEFAULT_LINEAGE_HASH: "sha256:default",
  fetchLineage: () =>
    Promise.resolve({
      evidence_hash: "sha256:default",
      found: true,
      nodes: [
        {
          layer: "provider_record",
          entity: "fmp",
          id: 1,
          key: "prov-1",
          detail: { metric: "pe_ratio" },
        },
      ],
      llm_consumers: [
        {
          provider: "qwen",
          model: "qwen-plus",
          ticker: "NVDA",
          overlay_ref: "ov-1",
          prompt_version: "v1",
        },
      ],
      note: "consumers listed",
    }),
  fetchDpObservations: () => Promise.resolve({ observations: [] }),
  fetchDpVersions: () =>
    Promise.resolve({ observation_id: 1, versions: [] }),
}));

describe("DataLineageExplorer", () => {
  it("renders the view and lineage chain", async () => {
    render(<DataLineageExplorer />);
    expect(await screen.findByText("Data Lineage Explorer")).toBeInTheDocument();
    expect(screen.getByTestId("view-data-lineage")).toBeInTheDocument();
    expect(screen.getByTestId("lineage-layer-provider_record")).toBeInTheDocument();
  });
});
