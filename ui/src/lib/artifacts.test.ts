import { describe, expect, it } from "vitest";
import {
  applyArtifactEvent,
  applyStatusEvent,
  type ArtifactState,
  createInitialArtifactState,
  selectPrimaryTab,
} from "./artifacts";

describe("artifact state helpers", () => {
  it("starts with a summary tab and no generated artifacts", () => {
    const state = createInitialArtifactState();

    expect(state.activeTab).toBe("summary");
    expect(state.summaryTitle).toBe("Reporting Workspace");
    expect(state.summary).toBe("");
    expect(state.rows).toEqual([]);
    expect(state.chartSeries).toEqual([]);
    expect(state.reportTitle).toBe("");
    expect(state.reportSections).toEqual([]);
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

  it("preserves existing file links when report artifacts omit files", () => {
    const withFiles = applyArtifactEvent(createInitialArtifactState(), {
      type: "file-link",
      files: [{ label: "Prior CSV", href: "/files/prior.csv" }],
    });

    const state = applyArtifactEvent(withFiles, {
      type: "report",
      reportTitle: "Operational Risk Brief",
      sections: [
        { heading: "Top Findings", body: "Payment operations need review." },
      ],
    });

    expect(state.files).toEqual([
      { label: "Prior CSV", href: "/files/prior.csv" },
    ]);
    expect(state.activeTab).toBe("report");
  });

  it("stores file-link artifacts and selects the files tab", () => {
    const state = applyArtifactEvent(createInitialArtifactState(), {
      type: "file-link",
      files: [{ label: "Export CSV", href: "/files/export.csv" }],
    });

    expect(state.files).toEqual([
      { label: "Export CSV", href: "/files/export.csv" },
    ]);
    expect(state.activeTab).toBe("files");
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

  it("uses deterministic incrementing status ids", () => {
    const first = applyStatusEvent(createInitialArtifactState(), {
      label: "Querying sample risk data",
      state: "running",
    });

    const second = applyStatusEvent(first, {
      label: "Rendering report",
      state: "complete",
    });

    expect(second.statusItems.map((item) => item.id)).toEqual([
      "status-1",
      "status-2",
    ]);
  });

  it("selects the best available tab for an artifact state by priority", () => {
    expect(selectPrimaryTab(createInitialArtifactState())).toBe("summary");

    const withFiles: ArtifactState = {
      ...createInitialArtifactState(),
      files: [{ label: "Export CSV", href: "/files/export.csv" }],
    };

    const withCharts: ArtifactState = {
      ...withFiles,
      chartSeries: [{ label: "Payments", value: 18 }],
    };

    const withData: ArtifactState = {
      ...withCharts,
      rows: [{ riskId: "RSK-001" }],
    };

    const withReport: ArtifactState = {
      ...withData,
      reportSections: [
        { heading: "Top Findings", body: "Payment operations need review." },
      ],
    };

    expect(selectPrimaryTab(withFiles)).toBe("files");
    expect(selectPrimaryTab(withCharts)).toBe("charts");
    expect(selectPrimaryTab(withData)).toBe("data");
    expect(selectPrimaryTab(withReport)).toBe("report");
  });
});
