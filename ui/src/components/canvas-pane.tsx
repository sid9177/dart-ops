"use client";

import type { CanvasState, SurfaceSpec } from "@/lib/surface-types";
import { MarkdownSummary } from "@/components/catalog/markdown-summary";
import { DataTable } from "@/components/catalog/data-table";
import { ChartBar } from "@/components/catalog/chart-bar";
import { ChartColumn } from "@/components/catalog/chart-column";
import { ChartLine } from "@/components/catalog/chart-line";
import { ChartDonut } from "@/components/catalog/chart-donut";
import { KpiCard } from "@/components/catalog/kpi-card";
import { HeatMap } from "@/components/catalog/heat-map";
import { ReportSection } from "@/components/catalog/report-section";
import { FileLink } from "@/components/catalog/file-link";

type AnyComponent = React.FC<{ props: Record<string, unknown> }>;

const componentMap = {
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
} as unknown as Record<string, AnyComponent>;

function renderSurface(surface: SurfaceSpec) {
  const Component = componentMap[surface.component];
  if (!Component) return null;
  return <Component props={surface.props} />;
}

interface CanvasPaneProps {
  state: CanvasState;
}

export function CanvasPane({ state }: CanvasPaneProps) {
  if (state.surfaces.length === 0) {
    return (
      <div className="canvas-empty">
        <p>Ask Copilot to generate analysis, tables, charts, or reports.</p>
      </div>
    );
  }

  return (
    <>
      <div className="canvas-header">
        <div>
          <p className="eyebrow dark">Generated output</p>
          <h2>Reporting Workspace</h2>
        </div>
      </div>
      <div className="canvas-body">
        {state.surfaces.map((surface) => (
          <section
            key={surface.surfaceId}
            id={`surface-${surface.surfaceId}`}
            className="surface-section"
          >
            {renderSurface(surface)}
          </section>
        ))}
      </div>
    </>
  );
}