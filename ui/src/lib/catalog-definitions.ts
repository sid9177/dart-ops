import { z } from "zod";

export const catalogDefinitions = {
  StatusChip: {
    description:
      "Inline progress indicator showing agent activity status. Use for all status updates.",
    props: z.object({
      label: z.string().describe("Status message to display"),
      state: z.enum(["queued", "running", "complete", "error"]),
    }),
  },
  SuggestionButtons: {
    description:
      "Clickable follow-up prompt buttons rendered in chat. Provide 2-3 suggestions after each analysis.",
    props: z.object({
      prompts: z.array(z.string()).describe("Follow-up prompt texts"),
    }),
  },
  ApprovalGate: {
    description:
      "HITL card with Approve/Decline buttons. Use when orchestrator requires user approval before concluding.",
    props: z.object({
      question: z.string().describe("Approval question"),
      draftSummary: z.string().describe("Summary of what is being approved"),
    }),
  },
  MarkdownSummary: {
    description:
      "Titled card with formatted text. Use for executive summaries and analysis commentary.",
    props: z.object({
      title: z.string(),
      content: z.string().describe("Markdown-formatted text"),
    }),
  },
  DataTable: {
    description:
      "Styled data table with Citi navy headers and alternating rows. Use for tabular risk data.",
    props: z.object({
      columns: z.array(z.string()).optional(),
      rows: z.array(z.record(z.union([z.string(), z.number(), z.boolean(), z.null()]))),
    }),
  },
  ChartBar: {
    description:
      "Horizontal bar chart for category comparisons. Use to compare risk levels across business units.",
    props: z.object({
      title: z.string(),
      series: z.array(z.object({ label: z.string(), value: z.number() })),
    }),
  },
  ChartColumn: {
    description:
      "Vertical column chart for period comparisons. Use for quarterly trends.",
    props: z.object({
      title: z.string(),
      series: z.array(z.object({ label: z.string(), value: z.number() })),
    }),
  },
  ChartLine: {
    description:
      "Line chart for trend visualization over time. Use for risk trajectory across periods.",
    props: z.object({
      title: z.string(),
      points: z.array(z.object({ x: z.string(), y: z.number() })),
    }),
  },
  ChartDonut: {
    description:
      "Donut chart for distribution visualization. Use for risk category breakdowns.",
    props: z.object({
      title: z.string(),
      segments: z.array(z.object({ label: z.string(), value: z.number() })),
    }),
  },
  KpiCard: {
    description:
      "Large metric card with label and optional delta. Use for headline risk indicators.",
    props: z.object({
      label: z.string(),
      value: z.string(),
      delta: z.string().optional(),
    }),
  },
  HeatMap: {
    description:
      "Risk matrix heatmap grid. Use for likelihood x impact risk matrices.",
    props: z.object({
      title: z.string(),
      rows: z.array(
        z.object({
          label: z.string(),
          cells: z.array(
            z.object({ label: z.string(), value: z.number() }),
          ),
        }),
      ),
    }),
  },
  ReportSection: {
    description:
      "Titled card with heading and body text. Use to compose multi-section reports.",
    props: z.object({
      heading: z.string(),
      body: z.string(),
    }),
  },
  FileLink: {
    description:
      "Styled download button for generated PDF or PPTX reports. Use when reporter generates files.",
    props: z.object({
      label: z.string(),
      href: z.string(),
    }),
  },
} as const;

export const citiTheme = {
  colors: {
    primary: "#255BE3",
    primaryHover: "#0041A5",
    surface: "#FFFFFF",
    surfaceMuted: "#F6F8FA",
    surfaceStrong: "#F0F4F7",
    border: "#D9E2EA",
    text: "#1D2834",
    textMuted: "#4F6F90",
    navy: "#002D72",
    success: "#00B755",
    warning: "#FFCD00",
    danger: "#B60000",
  },
  radii: {
    panel: "2px",
    button: "6px",
    input: "6px",
  },
  fonts: {
    sans: '"Citi-Sans-Text-Regular", "Interstate_Light", "Overpass", system-ui, sans-serif',
    mono: '"OverpassMono", ui-monospace, monospace',
  },
  transitions: {
    duration: "200ms",
    easing: "cubic-bezier(0.6, 0, 1, 1)",
  },
};