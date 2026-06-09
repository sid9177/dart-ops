import { describe, expect, it } from "vitest";
import {
  applyArtifactEvent,
  applyStatusEvent,
  createInitialArtifactState,
  selectPrimaryTab,
} from "./artifacts";

describe("artifact state helpers", () => {
  it("starts with a summary tab and no generated artifacts", () => {
    const state = createInitialArtifactState();

    expect(state.activeTab).toBe("summary");
    expect(state.summary).toBe("");
    expect(state.rows).toEqual([]);
    expect(state.chartSeries).toEqual([]);
    expect(state.files).toEqual([]);
    expect(state.statusItems).toEqual([]);
  });

  it("stores markdown summaries and selects the summary tab", () => {
    const state = applyArtifactEvent(createInitialArtifactState(), {
      type: "markdown",
      title: "Executive Summary",
      content: "High residual risk remains concentrated in payment operations.",
    });

    expect(state.summaryTitle).toBe("Executive Summary");
    expect(state.summary).toContain("High residual risk");
    expect(state.activeTab).toBe("summary");
  });

  it("stores table artifacts and selects the data tab", () => {
    const state = applyArtifactEvent(createInitialArtifactState(), {
      type: "data-table",
      rows: [
        { riskId: "RSK-001", severity: "High", status: "Open" },
        { riskId: "RSK-002", severity: "Medium", status: "Review" },
      ],
    });

    expect(state.rows).toHaveLength(2);
    expect(state.rows[0].riskId).toBe("RSK-001");
    expect(state.activeTab).toBe("data");
  });

  it("stores chart-ready artifacts and selects the charts tab", () => {
    const state = applyArtifactEvent(createInitialArtifactState(), {
      type: "chart",
      series: [
        { label: "Payments", value: 18 },
        { label: "Markets", value: 11 },
      ],
    });

    expect(state.chartSeries).toEqual([
      { label: "Payments", value: 18 },
      { label: "Markets", value: 11 },
    ]);
    expect(state.activeTab).toBe("charts");
  });

  it("stores report metadata and file links", () => {
    const state = applyArtifactEvent(createInitialArtifactState(), {
      type: "report",
      reportTitle: "Operational Risk Brief",
      sections: [
        { heading: "Top Findings", body: "Payment operations need review." },
      ],
      files: [{ label: "Download PPTX", href: "/files/report.pptx" }],
    });

    expect(state.reportTitle).toBe("Operational Risk Brief");
    expect(state.reportSections).toHaveLength(1);
    expect(state.files[0].href).toBe("/files/report.pptx");
    expect(state.activeTab).toBe("report");
  });

  it("records status events without changing the selected artifact tab", () => {
    const initial = applyArtifactEvent(createInitialArtifactState(), {
      type: "data-table",
      rows: [{ riskId: "RSK-001", severity: "High" }],
    });

    const state = applyStatusEvent(initial, {
      label: "Querying sample risk data",
      state: "running",
    });

    expect(state.activeTab).toBe("data");
    expect(state.statusItems).toEqual([
      {
        id: "status-1",
        label: "Querying sample risk data",
        state: "running",
      },
    ]);
  });

  it("selects the best available tab for an artifact state", () => {
    expect(selectPrimaryTab(createInitialArtifactState())).toBe("summary");
    expect(
      selectPrimaryTab(
        applyArtifactEvent(createInitialArtifactState(), {
          type: "data-table",
          rows: [{ riskId: "RSK-001" }],
        }),
      ),
    ).toBe("data");
  });
});
