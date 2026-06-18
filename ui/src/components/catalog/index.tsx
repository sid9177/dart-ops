import { createCatalog } from "@copilotkit/a2ui-renderer";
import { catalogDefinitions } from "@/lib/catalog-definitions";
import { StatusChip } from "./status-chip";
import { SuggestionButtons } from "./suggestion-buttons";
import { ApprovalGate } from "./approval-gate";
import { MarkdownSummary } from "./markdown-summary";
import { DataTable } from "./data-table";
import { ChartBar } from "./chart-bar";
import { ChartColumn } from "./chart-column";
import { ChartLine } from "./chart-line";
import { ChartDonut } from "./chart-donut";
import { KpiCard } from "./kpi-card";
import { HeatMap } from "./heat-map";
import { ReportSection } from "./report-section";
import { FileLink } from "./file-link";

export const catalog = createCatalog(
  catalogDefinitions,
  {
    StatusChip,
    SuggestionButtons,
    ApprovalGate,
    MarkdownSummary,
    DataTable,
    ChartBar,
    ChartColumn,
    ChartLine,
    ChartDonut,
    KpiCard,
    HeatMap,
    ReportSection,
    FileLink,
  },
  { includeBasicCatalog: true },
);