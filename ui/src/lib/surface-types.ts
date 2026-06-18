export type SurfaceComponentName =
  | "StatusChip"
  | "SuggestionButtons"
  | "ApprovalGate"
  | "MarkdownSummary"
  | "DataTable"
  | "ChartBar"
  | "ChartColumn"
  | "ChartLine"
  | "ChartDonut"
  | "KpiCard"
  | "HeatMap"
  | "ReportSection"
  | "FileLink";

export interface SurfaceSpec {
  surfaceId: string;
  component: SurfaceComponentName;
  props: Record<string, unknown>;
}

export interface CanvasState {
  surfaces: SurfaceSpec[];
}

export function createInitialCanvasState(): CanvasState {
  return { surfaces: [] };
}

export function applySurfaceRegistration(
  state: CanvasState,
  surface: SurfaceSpec,
): CanvasState {
  const existingIndex = state.surfaces.findIndex(
    (s) => s.surfaceId === surface.surfaceId,
  );

  if (existingIndex === -1) {
    return { surfaces: [...state.surfaces, surface] };
  }

  const nextSurfaces = [...state.surfaces];
  nextSurfaces[existingIndex] = surface;
  return { surfaces: nextSurfaces };
}