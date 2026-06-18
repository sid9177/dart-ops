import { describe, expect, it } from "vitest";
import {
  createInitialCanvasState,
  applySurfaceRegistration,
  type SurfaceSpec,
} from "./surface-types";

describe("canvas state helpers", () => {
  it("starts with no surfaces", () => {
    const state = createInitialCanvasState();
    expect(state.surfaces).toEqual([]);
  });

  it("registers a surface and appends to the list", () => {
    const surface: SurfaceSpec = {
      surfaceId: "surface-1",
      component: "MarkdownSummary",
      props: { title: "Summary", content: "Text" },
    };
    const state = applySurfaceRegistration(
      createInitialCanvasState(),
      surface,
    );
    expect(state.surfaces).toHaveLength(1);
    expect(state.surfaces[0].surfaceId).toBe("surface-1");
    expect(state.surfaces[0].component).toBe("MarkdownSummary");
  });

  it("dedups by surfaceId (replace, not append)", () => {
    const first: SurfaceSpec = {
      surfaceId: "surface-1",
      component: "MarkdownSummary",
      props: { title: "First", content: "A" },
    };
    const updated: SurfaceSpec = {
      surfaceId: "surface-1",
      component: "DataTable",
      props: { rows: [{ id: 1 }] },
    };

    const afterFirst = applySurfaceRegistration(
      createInitialCanvasState(),
      first,
    );
    const afterUpdate = applySurfaceRegistration(afterFirst, updated);

    expect(afterUpdate.surfaces).toHaveLength(1);
    expect(afterUpdate.surfaces[0].component).toBe("DataTable");
  });

  it("preserves order of other surfaces when replacing one", () => {
    const a: SurfaceSpec = {
      surfaceId: "a",
      component: "MarkdownSummary",
      props: { title: "A", content: "A" },
    };
    const b: SurfaceSpec = {
      surfaceId: "b",
      component: "DataTable",
      props: { rows: [] },
    };
    const aUpdated: SurfaceSpec = {
      surfaceId: "a",
      component: "KpiCard",
      props: { label: "KPI", value: "42" },
    };

    let state = createInitialCanvasState();
    state = applySurfaceRegistration(state, a);
    state = applySurfaceRegistration(state, b);
    state = applySurfaceRegistration(state, aUpdated);

    expect(state.surfaces.map((s) => s.surfaceId)).toEqual(["a", "b"]);
    expect(state.surfaces[0].component).toBe("KpiCard");
  });
});