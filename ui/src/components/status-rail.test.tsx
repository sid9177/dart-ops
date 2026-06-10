// @vitest-environment jsdom

import "@testing-library/jest-dom/vitest";
import { cleanup, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it } from "vitest";
import { applyStatusEvent, createInitialArtifactState } from "@/lib/artifacts";
import { StatusRail } from "./status-rail";

afterEach(() => {
  cleanup();
});

describe("StatusRail", () => {
  it("renders an idle state when no activity exists", () => {
    render(<StatusRail statusItems={createInitialArtifactState().statusItems} />);

    expect(screen.getByText("Agent Activity")).toBeInTheDocument();
    expect(screen.getByText("No agent activity yet.")).toBeInTheDocument();
  });

  it("renders status items with state labels", () => {
    const state = applyStatusEvent(createInitialArtifactState(), {
      label: "Drafting executive summary",
      state: "running",
    });

    render(<StatusRail statusItems={state.statusItems} />);

    expect(screen.getByText("Drafting executive summary")).toBeInTheDocument();
    expect(screen.getByText("running")).toBeInTheDocument();
  });
});
