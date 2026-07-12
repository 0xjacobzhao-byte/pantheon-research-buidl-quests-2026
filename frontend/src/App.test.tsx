import { render, screen, fireEvent } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import App from "./App";

// App's own overview fetches: reject so the overview stays inert (each call is
// wrapped in .catch in App). We only care about nav + tab switching here.
vi.mock("./api", () => {
  const reject = () => Promise.reject(new Error("mock"));
  return {
    fetchProject: reject,
    fetchDemoFlow: reject,
    fetchComparison: reject,
    fetchAlibabaProof: reject,
    fetchQwenConfig: reject,
    fetchDataQuality: reject,
    fetchModules: reject,
    fetchTickerProfile: reject,
    fetchProviderHealth: reject,
    fetchValidationTimeline: reject,
    fetchMacroMini: reject,
    fetchMarketPulseMini: reject,
    fetchFiccMini: reject,
  };
});

// Stub the page containers so switching tabs is isolated + fast.
vi.mock("./components/llm/FiveModelResearchCockpit", () => ({
  default: () => <div data-testid="view-llm">llm</div>,
}));
vi.mock("./components/macro/MacroRiskContextPanel", () => ({
  default: () => <div data-testid="view-macro">macro</div>,
}));
vi.mock("./components/research-ops/ResearchOpsConsole", () => ({
  default: () => <div data-testid="view-research-ops">research-ops</div>,
}));
vi.mock("./components/data-lineage/DataLineageExplorer", () => ({
  default: () => <div data-testid="view-data-lineage">data-lineage</div>,
}));
vi.mock("./components/paper-gateway/PaperGatewayDemo", () => ({
  default: () => <div data-testid="view-paper-gateway">paper-gateway</div>,
}));
vi.mock("./components/btc/BtcThreeLayerStack", () => ({
  default: () => <div data-testid="view-btc">btc</div>,
}));

const TAB_LABELS = [
  "Overview",
  "Five-Model LLM",
  "Macro Risk",
  "Research Ops",
  "Data Lineage",
  "Paper Gateway",
  "BTC Stack",
];

describe("App tab navigation", () => {
  it("renders the nav with all seven tabs and the overview by default", () => {
    render(<App />);
    const nav = screen.getByTestId("main-nav");
    expect(nav).toBeInTheDocument();
    for (const label of TAB_LABELS) {
      expect(screen.getByText(label)).toBeInTheDocument();
    }
    expect(screen.getByTestId("view-overview")).toBeInTheDocument();
  });

  it("switches to the Macro Risk view when its tab is clicked", () => {
    render(<App />);
    expect(screen.queryByTestId("view-macro")).toBeNull();
    fireEvent.click(screen.getByText("Macro Risk"));
    expect(screen.getByTestId("view-macro")).toBeInTheDocument();
    expect(screen.queryByTestId("view-overview")).toBeNull();
  });

  it("switches to the BTC and Paper Gateway views", () => {
    render(<App />);
    fireEvent.click(screen.getByText("BTC Stack"));
    expect(screen.getByTestId("view-btc")).toBeInTheDocument();
    fireEvent.click(screen.getByText("Paper Gateway"));
    expect(screen.getByTestId("view-paper-gateway")).toBeInTheDocument();
  });
});
