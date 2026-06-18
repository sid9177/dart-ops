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

function renderSurface(surface: SurfaceSpec) {
  const props = { props: surface.props } as any;
  switch (surface.component) {
    case "MarkdownSummary":
      return <MarkdownSummary {...props} />;
    case "DataTable":
      return <DataTable {...props} />;
    case "ChartBar":
      return <ChartBar {...props} />;
    case "ChartColumn":
      return <ChartColumn {...props} />;
    case "ChartLine":
      return <ChartLine {...props} />;
    case "ChartDonut":
      return <ChartDonut {...props} />;
    case "KpiCard":
      return <KpiCard {...props} />;
    case "HeatMap":
      return <HeatMap {...props} />;
    case "ReportSection":
      return <ReportSection {...props} />;
    case "FileLink":
      return <FileLink {...props} />;
    default:
      return null;
  }
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