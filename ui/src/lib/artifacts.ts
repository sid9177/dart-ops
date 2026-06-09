export type ArtifactTab = "summary" | "data" | "charts" | "report" | "files";

export type ArtifactRow = Record<string, string | number | boolean | null>;

export interface ChartPoint {
  label: string;
  value: number;
}

export interface ReportSection {
  heading: string;
  body: string;
}

export interface FileLink {
  label: string;
  href: string;
}

export interface StatusItem {
  id: string;
  label: string;
  state: "queued" | "running" | "complete" | "error";
}

export interface ArtifactState {
  activeTab: ArtifactTab;
  summaryTitle: string;
  summary: string;
  rows: ArtifactRow[];
  chartSeries: ChartPoint[];
  reportTitle: string;
  reportSections: ReportSection[];
  files: FileLink[];
  statusItems: StatusItem[];
}

export type ArtifactEvent =
  | { type: "markdown"; title: string; content: string }
  | { type: "data-table"; rows: ArtifactRow[] }
  | { type: "chart"; series: ChartPoint[] }
  | {
      type: "report";
      reportTitle: string;
      sections: ReportSection[];
      files?: FileLink[];
    }
  | { type: "file-link"; files: FileLink[] };

export interface StatusEvent {
  label: string;
  state: StatusItem["state"];
}

export function createInitialArtifactState(): ArtifactState {
  return {
    activeTab: "summary",
    summaryTitle: "Reporting Workspace",
    summary: "",
    rows: [],
    chartSeries: [],
    reportTitle: "",
    reportSections: [],
    files: [],
    statusItems: [],
  };
}

export function applyArtifactEvent(
  state: ArtifactState,
  event: ArtifactEvent,
): ArtifactState {
  if (event.type === "markdown") {
    return {
      ...state,
      activeTab: "summary",
      summaryTitle: event.title,
      summary: event.content,
    };
  }

  if (event.type === "data-table") {
    return {
      ...state,
      activeTab: "data",
      rows: event.rows,
    };
  }

  if (event.type === "chart") {
    return {
      ...state,
      activeTab: "charts",
      chartSeries: event.series,
    };
  }

  if (event.type === "report") {
    return {
      ...state,
      activeTab: "report",
      reportTitle: event.reportTitle,
      reportSections: event.sections,
      files: event.files ?? state.files,
    };
  }

  return {
    ...state,
    activeTab: "files",
    files: event.files,
  };
}

export function applyStatusEvent(
  state: ArtifactState,
  event: StatusEvent,
): ArtifactState {
  const nextIndex = state.statusItems.length + 1;

  return {
    ...state,
    statusItems: [
      ...state.statusItems,
      {
        id: `status-${nextIndex}`,
        label: event.label,
        state: event.state,
      },
    ],
  };
}

export function selectPrimaryTab(state: ArtifactState): ArtifactTab {
  if (state.reportSections.length > 0) return "report";
  if (state.rows.length > 0) return "data";
  if (state.chartSeries.length > 0) return "charts";
  if (state.files.length > 0) return "files";
  return "summary";
}
