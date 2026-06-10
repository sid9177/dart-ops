// @vitest-environment jsdom

import "@testing-library/jest-dom/vitest";
import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { AppShell } from "./app-shell";

describe("AppShell", () => {
  it("renders fallback Citi branding and workspace regions", () => {
    render(
      <AppShell
        runtimeLabel="Local sample runtime"
        chat={<div>Chat panel</div>}
        canvas={<div>Artifact canvas</div>}
        status={<div>Status rail</div>}
      />,
    );

    expect(screen.getByText("Citi | Ops Risk")).toBeInTheDocument();
    expect(screen.getByText("Reporting Analyst Workspace")).toBeInTheDocument();
    expect(screen.getByText("Local sample runtime")).toBeInTheDocument();
    expect(screen.getByLabelText("Copilot chat panel")).toBeInTheDocument();
    expect(screen.getByLabelText("Artifact workspace")).toBeInTheDocument();
    expect(screen.getByLabelText("Agent activity rail")).toBeInTheDocument();
  });
});
