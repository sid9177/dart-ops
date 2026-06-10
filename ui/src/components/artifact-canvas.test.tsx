// @vitest-environment jsdom

import "@testing-library/jest-dom/vitest";
import { cleanup, fireEvent, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it } from "vitest";
import {
  applyArtifactEvent,
  createInitialArtifactState,
} from "@/lib/artifacts";
import { ArtifactCanvas } from "./artifact-canvas";

afterEach(() => {
  cleanup();
});

describe("ArtifactCanvas", () => {
  it("renders the empty reporting workspace", () => {
    render(<ArtifactCanvas state={createInitialArtifactState()} />);

    expect(
      screen.getByRole("heading", {
        level: 2,
        name: "Reporting Workspace",
      }),
    ).toBeInTheDocument();
    expect(
      screen.getByText(
        "Ask Copilot to generate analysis, tables, charts, reports, or file links.",
      ),
    ).toBeInTheDocument();
  });

  it("renders data tables from artifact state", () => {
    const state = applyArtifactEvent(createInitialArtifactState(), {
      type: "data-table",
      rows: [{ riskId: "RSK-001", severity: "High", status: "Open" }],
    });

    render(<ArtifactCanvas state={state} />);

    expect(screen.getByRole("button", { name: "Data" })).toHaveAttribute(
      "aria-pressed",
      "true",
    );
    expect(screen.getByText("RSK-001")).toBeInTheDocument();
    expect(screen.getByText("High")).toBeInTheDocument();
  });

  it("switches tabs when a tab button is clicked", () => {
    const state = applyArtifactEvent(createInitialArtifactState(), {
      type: "report",
      reportTitle: "Operational Risk Brief",
      sections: [{ heading: "Top Findings", body: "Payment risks increased." }],
      files: [{ label: "Download PPTX", href: "/files/report.pptx" }],
    });

    render(<ArtifactCanvas state={state} />);
    fireEvent.click(screen.getByRole("button", { name: "Files" }));

    expect(screen.getByRole("link", { name: "Download PPTX" })).toHaveAttribute(
      "href",
      "/files/report.pptx",
    );
  });
});
