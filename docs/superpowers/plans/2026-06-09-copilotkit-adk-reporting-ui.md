# CopilotKit ADK Reporting UI Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a Citigroup-branded CopilotKit reporting analyst UI with a local sample FastAPI/ADK backend.

**Architecture:** The browser talks to a Next.js CopilotKit runtime at `/api/copilotkit`. That runtime proxies to a local or workplace FastAPI AG-UI backend through an `HttpAgent`, matching CopilotKit's documented proxy pattern. The UI stores generated artifacts in frontend state and renders them in a large report canvas while CopilotKit chat remains the primary command surface.

**Tech Stack:** Next.js App Router, React 19, CopilotKit `@copilotkit/react-core` and `@copilotkit/react-ui` next packages, `@copilotkit/runtime`, `@ag-ui/client`, FastAPI, `ag-ui-adk`, Google ADK, Vitest, React Testing Library, Pytest.

---

## Reference Docs

- CopilotKit ADK quickstart: `https://docs.copilotkit.ai/google-adk/quickstart`
- CopilotKit AG-UI runtime proxy docs: `https://docs.copilotkit.ai/google-adk/backend/ag-ui`
- CopilotKit tool rendering docs: `https://docs.copilotkit.ai/google-adk/generative-ui/tool-rendering`
- CopilotKit troubleshooting docs: `https://docs.copilotkit.ai/google-adk/troubleshooting/common-issues`

## File Structure

- Modify: `ui/package.json` - declare direct frontend dependencies and test scripts.
- Modify: `ui/package-lock.json` - updated by `npm install`.
- Create: `ui/src/lib/artifacts.ts` - pure artifact/status state helpers.
- Create: `ui/src/lib/artifacts.test.ts` - Vitest coverage for artifact/status helpers.
- Create: `ui/src/lib/runtime-config.ts` - pure runtime URL helpers.
- Create: `ui/src/lib/runtime-config.test.ts` - Vitest coverage for runtime helpers.
- Create: `ui/src/app/providers.tsx` - client CopilotKit provider wrapper.
- Modify: `ui/src/app/layout.tsx` - server layout shell, imports styles.
- Modify: `ui/src/app/page.tsx` - dashboard entrypoint that composes focused components.
- Create: `ui/src/components/app-shell.tsx` - Citi shell and workspace layout.
- Create: `ui/src/components/app-shell.test.tsx` - render tests for shell fallback branding.
- Create: `ui/src/components/artifact-canvas.tsx` - tabbed artifact/report canvas.
- Create: `ui/src/components/artifact-canvas.test.tsx` - render tests for artifact tabs.
- Create: `ui/src/components/status-rail.tsx` - collapsible agent trace rail.
- Create: `ui/src/components/status-rail.test.tsx` - render tests for status rail states.
- Create: `ui/src/components/chat-panel.tsx` - Copilot chat panel and starter prompts.
- Create: `ui/src/components/copilot-agent-bridge.tsx` - frontend tools and AG-UI event bridge.
- Create: `ui/src/app/api/copilotkit/route.ts` - Next.js CopilotKit runtime proxy.
- Modify: `ui/src/app/globals.css` - Citi design tokens and component styling.
- Create: `ui/public/brand/.gitkeep` - brand asset slot.
- Modify: `pyproject.toml` - add demo backend dependencies.
- Modify: `uv.lock` - updated by `uv lock`.
- Create: `sample_backend/config/reporting_agent.yaml` - demo agent config.
- Create: `sample_backend/prompts/reporting_agent.md` - demo agent prompt.
- Create: `sample_backend/demo_data.py` - deterministic sample data and artifact payloads.
- Create: `sample_backend/server.py` - FastAPI AG-UI backend wrapper.
- Create: `tests/unit/test_sample_backend_demo_data.py` - backend helper tests.
- Modify: `ui/README.md` - local run instructions.

## Notes For Execution

- The current worktree contains unrelated uncommitted files. Do not revert or stage unrelated changes.
- Use the `@copilotkit/react-core/v2` exports for the new UI, because the installed next package exposes v2 exports and the current CopilotKit ADK docs use those imports.
- Keep the UI's public runtime default as `/api/copilotkit`. Configure the downstream FastAPI agent URL with a server-side variable named `COPILOTKIT_AGENT_URL`.
- Keep the official logo as an asset slot. Do not fabricate Citi's official logo.

---

### Task 1: Frontend Dependency And Script Setup

**Files:**
- Modify: `ui/package.json`
- Modify: `ui/package-lock.json`

- [ ] **Step 1: Update frontend dependencies**

Run:

```powershell
npm install @ag-ui/client@0.0.52
npm install -D vitest@^3.2.4 @testing-library/react@^16.3.0 @testing-library/jest-dom@^6.6.3 jsdom@^26.1.0
```

Run from:

```powershell
cd C:\Users\siddi\Projects\adk-workspace\dart-ops\ui
```

- [ ] **Step 2: Add test scripts**

Update `ui/package.json` scripts to:

```json
{
  "dev": "next dev",
  "build": "next build",
  "start": "next start",
  "lint": "eslint",
  "test": "vitest run",
  "test:watch": "vitest"
}
```

- [ ] **Step 3: Verify dependency metadata**

Run:

```powershell
npm ls @copilotkit/react-core @copilotkit/react-ui @copilotkit/runtime @ag-ui/client vitest
```

Expected: dependency tree resolves with no missing direct dependency errors.

- [ ] **Step 4: Commit**

```powershell
git add ui/package.json ui/package-lock.json
git commit -m "chore: add UI testing and AG-UI dependencies"
```

---

### Task 2: Artifact State Domain Helpers

**Files:**
- Create: `ui/src/lib/artifacts.ts`
- Create: `ui/src/lib/artifacts.test.ts`

- [ ] **Step 1: Write the failing artifact helper tests**

Create `ui/src/lib/artifacts.test.ts`:

```typescript
import { describe, expect, it } from "vitest";
import {
  applyArtifactEvent,
  applyStatusEvent,
  createInitialArtifactState,
  selectPrimaryTab,
} from "./artifacts";

describe("artifact state helpers", () => {
  it("starts with a summary tab and no generated artifacts", () => {
    const state = createInitialArtifactState();

    expect(state.activeTab).toBe("summary");
    expect(state.summary).toBe("");
    expect(state.rows).toEqual([]);
    expect(state.chartSeries).toEqual([]);
    expect(state.files).toEqual([]);
    expect(state.statusItems).toEqual([]);
  });

  it("stores markdown summaries and selects the summary tab", () => {
    const state = applyArtifactEvent(createInitialArtifactState(), {
      type: "markdown",
      title: "Executive Summary",
      content: "High residual risk remains concentrated in payment operations.",
    });

    expect(state.summaryTitle).toBe("Executive Summary");
    expect(state.summary).toContain("High residual risk");
    expect(state.activeTab).toBe("summary");
  });

  it("stores table artifacts and selects the data tab", () => {
    const state = applyArtifactEvent(createInitialArtifactState(), {
      type: "data-table",
      rows: [
        { riskId: "RSK-001", severity: "High", status: "Open" },
        { riskId: "RSK-002", severity: "Medium", status: "Review" },
      ],
    });

    expect(state.rows).toHaveLength(2);
    expect(state.rows[0].riskId).toBe("RSK-001");
    expect(state.activeTab).toBe("data");
  });

  it("stores chart-ready artifacts and selects the charts tab", () => {
    const state = applyArtifactEvent(createInitialArtifactState(), {
      type: "chart",
      series: [
        { label: "Payments", value: 18 },
        { label: "Markets", value: 11 },
      ],
    });

    expect(state.chartSeries).toEqual([
      { label: "Payments", value: 18 },
      { label: "Markets", value: 11 },
    ]);
    expect(state.activeTab).toBe("charts");
  });

  it("stores report metadata and file links", () => {
    const state = applyArtifactEvent(createInitialArtifactState(), {
      type: "report",
      reportTitle: "Operational Risk Brief",
      sections: [
        { heading: "Top Findings", body: "Payment operations need review." },
      ],
      files: [{ label: "Download PPTX", href: "/files/report.pptx" }],
    });

    expect(state.reportTitle).toBe("Operational Risk Brief");
    expect(state.reportSections).toHaveLength(1);
    expect(state.files[0].href).toBe("/files/report.pptx");
    expect(state.activeTab).toBe("report");
  });

  it("records status events without changing the selected artifact tab", () => {
    const initial = applyArtifactEvent(createInitialArtifactState(), {
      type: "data-table",
      rows: [{ riskId: "RSK-001", severity: "High" }],
    });

    const state = applyStatusEvent(initial, {
      label: "Querying sample risk data",
      state: "running",
    });

    expect(state.activeTab).toBe("data");
    expect(state.statusItems).toEqual([
      {
        id: "status-1",
        label: "Querying sample risk data",
        state: "running",
      },
    ]);
  });

  it("selects the best available tab for an artifact state", () => {
    expect(selectPrimaryTab(createInitialArtifactState())).toBe("summary");
    expect(
      selectPrimaryTab(
        applyArtifactEvent(createInitialArtifactState(), {
          type: "data-table",
          rows: [{ riskId: "RSK-001" }],
        }),
      ),
    ).toBe("data");
  });
});
```

- [ ] **Step 2: Run the tests and verify they fail**

Run:

```powershell
npm test -- src/lib/artifacts.test.ts
```

Expected: FAIL because `./artifacts` does not exist.

- [ ] **Step 3: Implement the artifact helpers**

Create `ui/src/lib/artifacts.ts`:

```typescript
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
```

- [ ] **Step 4: Run the tests and verify they pass**

Run:

```powershell
npm test -- src/lib/artifacts.test.ts
```

Expected: PASS for all artifact helper tests.

- [ ] **Step 5: Commit**

```powershell
git add ui/src/lib/artifacts.ts ui/src/lib/artifacts.test.ts
git commit -m "feat: add reporting artifact state helpers"
```

---

### Task 3: Runtime Configuration Helpers

**Files:**
- Create: `ui/src/lib/runtime-config.ts`
- Create: `ui/src/lib/runtime-config.test.ts`

- [ ] **Step 1: Write the failing runtime config tests**

Create `ui/src/lib/runtime-config.test.ts`:

```typescript
import { describe, expect, it } from "vitest";
import {
  DEFAULT_AGENT_ID,
  DEFAULT_AGENT_URL,
  DEFAULT_RUNTIME_URL,
  resolveAgentUrl,
  resolveRuntimeUrl,
} from "./runtime-config";

describe("runtime config", () => {
  it("uses stable defaults for local development", () => {
    expect(DEFAULT_RUNTIME_URL).toBe("/api/copilotkit");
    expect(DEFAULT_AGENT_URL).toBe("http://127.0.0.1:8000/");
    expect(DEFAULT_AGENT_ID).toBe("ops-risk-reporting");
  });

  it("resolves a public runtime URL with a fallback", () => {
    expect(resolveRuntimeUrl(undefined)).toBe("/api/copilotkit");
    expect(resolveRuntimeUrl("")).toBe("/api/copilotkit");
    expect(resolveRuntimeUrl("http://localhost:3000/api/copilotkit")).toBe(
      "http://localhost:3000/api/copilotkit",
    );
  });

  it("resolves the downstream AG-UI agent URL with a fallback", () => {
    expect(resolveAgentUrl(undefined)).toBe("http://127.0.0.1:8000/");
    expect(resolveAgentUrl("")).toBe("http://127.0.0.1:8000/");
    expect(resolveAgentUrl("http://localhost:8000/")).toBe(
      "http://localhost:8000/",
    );
  });
});
```

- [ ] **Step 2: Run the tests and verify they fail**

Run:

```powershell
npm test -- src/lib/runtime-config.test.ts
```

Expected: FAIL because `./runtime-config` does not exist.

- [ ] **Step 3: Implement runtime config helpers**

Create `ui/src/lib/runtime-config.ts`:

```typescript
export const DEFAULT_RUNTIME_URL = "/api/copilotkit";
export const DEFAULT_AGENT_URL = "http://127.0.0.1:8000/";
export const DEFAULT_AGENT_ID = "ops-risk-reporting";

export function resolveRuntimeUrl(value: string | undefined): string {
  return value && value.trim().length > 0 ? value : DEFAULT_RUNTIME_URL;
}

export function resolveAgentUrl(value: string | undefined): string {
  return value && value.trim().length > 0 ? value : DEFAULT_AGENT_URL;
}
```

- [ ] **Step 4: Run the tests and verify they pass**

Run:

```powershell
npm test -- src/lib/runtime-config.test.ts
```

Expected: PASS for all runtime config tests.

- [ ] **Step 5: Commit**

```powershell
git add ui/src/lib/runtime-config.ts ui/src/lib/runtime-config.test.ts
git commit -m "feat: add CopilotKit runtime configuration helpers"
```

---

### Task 4: CopilotKit Provider And Runtime Proxy

**Files:**
- Create: `ui/src/app/providers.tsx`
- Modify: `ui/src/app/layout.tsx`
- Create: `ui/src/app/api/copilotkit/route.ts`

- [ ] **Step 1: Create the client provider**

Create `ui/src/app/providers.tsx`:

```tsx
"use client";

import { CopilotKit } from "@copilotkit/react-core/v2";
import "@copilotkit/react-core/v2/styles.css";
import "@copilotkit/react-ui/styles.css";
import { DEFAULT_AGENT_ID, resolveRuntimeUrl } from "@/lib/runtime-config";

export function Providers({ children }: { children: React.ReactNode }) {
  const runtimeUrl = resolveRuntimeUrl(
    process.env.NEXT_PUBLIC_COPILOTKIT_RUNTIME_URL,
  );

  return (
    <CopilotKit runtimeUrl={runtimeUrl}>{children}</CopilotKit>
  );
}
```

- [ ] **Step 2: Replace the root layout**

Replace `ui/src/app/layout.tsx` with:

```tsx
import type { Metadata } from "next";
import type { ReactNode } from "react";
import { Providers } from "./providers";
import "./globals.css";

export const metadata: Metadata = {
  title: "Citi Ops Risk Reporting",
  description: "CopilotKit reporting analyst workspace for ADK agents",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: ReactNode;
}>) {
  return (
    <html lang="en">
      <body>
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
```

- [ ] **Step 3: Create the Next runtime proxy route**

Create `ui/src/app/api/copilotkit/route.ts`:

```typescript
import {
  CopilotRuntime,
  ExperimentalEmptyAdapter,
  copilotRuntimeNextJSAppRouterEndpoint,
} from "@copilotkit/runtime";
import { HttpAgent } from "@ag-ui/client";
import { NextRequest } from "next/server";
import {
  DEFAULT_AGENT_ID,
  resolveAgentUrl,
} from "@/lib/runtime-config";

const serviceAdapter = new ExperimentalEmptyAdapter();

const runtime = new CopilotRuntime({
  agents: {
    [DEFAULT_AGENT_ID]: new HttpAgent({
      url: resolveAgentUrl(process.env.COPILOTKIT_AGENT_URL),
    }),
  },
});

export const POST = async (req: NextRequest) => {
  const { handleRequest } = copilotRuntimeNextJSAppRouterEndpoint({
    runtime,
    serviceAdapter,
    endpoint: "/api/copilotkit",
  });

  return handleRequest(req);
};
```

- [ ] **Step 4: Run TypeScript build verification**

Run:

```powershell
npm run build
```

Expected: build reaches the Next.js compilation phase without import errors for `@copilotkit/react-core/v2`, `@ag-ui/client`, or `@copilotkit/runtime`.

- [ ] **Step 5: Commit**

```powershell
git add ui/src/app/providers.tsx ui/src/app/layout.tsx ui/src/app/api/copilotkit/route.ts
git commit -m "feat: configure CopilotKit runtime proxy"
```

---

### Task 5: Citi App Shell

**Files:**
- Create: `ui/src/components/app-shell.tsx`
- Create: `ui/src/components/app-shell.test.tsx`
- Modify: `ui/src/app/page.tsx`
- Modify: `ui/src/app/globals.css`
- Create: `ui/public/brand/.gitkeep`

- [ ] **Step 1: Write the failing shell render test**

Create `ui/src/components/app-shell.test.tsx`:

```tsx
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
```

- [ ] **Step 2: Run the shell test and verify it fails**

Run:

```powershell
npm test -- src/components/app-shell.test.tsx
```

Expected: FAIL because `./app-shell` does not exist.

- [ ] **Step 3: Implement the app shell**

Create `ui/src/components/app-shell.tsx`:

```tsx
import Image from "next/image";
import type { ReactNode } from "react";

interface AppShellProps {
  runtimeLabel: string;
  chat: ReactNode;
  canvas: ReactNode;
  status: ReactNode;
}

export function AppShell({ runtimeLabel, chat, canvas, status }: AppShellProps) {
  return (
    <main className="app-shell">
      <header className="app-header">
        <div className="brand-lockup">
          <div className="brand-logo-frame">
            <Image
              src="/brand/citi-logo.svg"
              alt=""
              width={72}
              height={28}
              className="brand-logo"
              unoptimized
            />
            <span className="brand-fallback">Citi | Ops Risk</span>
          </div>
          <div>
            <p className="eyebrow">Analytics and reporting</p>
            <h1>Reporting Analyst Workspace</h1>
          </div>
        </div>
        <div className="runtime-pill" aria-label="Runtime connection">
          <span className="runtime-dot" />
          {runtimeLabel}
        </div>
      </header>

      <section className="workspace-layout">
        <aside className="chat-column" aria-label="Copilot chat panel">
          {chat}
        </aside>
        <section className="canvas-column" aria-label="Artifact workspace">
          {canvas}
        </section>
        <aside className="status-column" aria-label="Agent activity rail">
          {status}
        </aside>
      </section>
    </main>
  );
}
```

- [ ] **Step 4: Add the brand asset slot**

Run:

```powershell
New-Item -ItemType Directory -Force ui\public\brand
New-Item -ItemType File -Force ui\public\brand\.gitkeep
```

- [ ] **Step 5: Add Citi shell CSS**

Replace `ui/src/app/globals.css` with the component classes from this step. Use centralized variables only:

```css
:root {
  --citi-navy: #0f1632;
  --citi-blue: #0041a5;
  --citi-action: #255be3;
  --citi-red: #b60000;
  --surface: #ffffff;
  --surface-muted: #f4f7fb;
  --surface-strong: #e9eef6;
  --text-primary: #111827;
  --text-muted: #5f6b7a;
  --border: #d8dee9;
  --shadow-soft: 0 12px 30px rgba(15, 22, 50, 0.1);
  --radius: 8px;
}

* {
  box-sizing: border-box;
}

html,
body {
  height: 100%;
}

body {
  margin: 0;
  color: var(--text-primary);
  background: var(--surface-muted);
  font-family:
    Arial,
    Helvetica,
    sans-serif;
}

button,
input,
textarea {
  font: inherit;
}

.app-shell {
  display: flex;
  flex-direction: column;
  height: 100vh;
  min-height: 720px;
  overflow: hidden;
}

.app-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
  min-height: 76px;
  padding: 14px 22px;
  background: var(--citi-navy);
  color: var(--surface);
  box-shadow: var(--shadow-soft);
}

.brand-lockup {
  display: flex;
  align-items: center;
  gap: 18px;
  min-width: 0;
}

.brand-logo-frame {
  position: relative;
  display: flex;
  align-items: center;
  min-width: 120px;
  min-height: 38px;
}

.brand-logo {
  display: block;
  max-width: 96px;
  height: auto;
}

.brand-logo[src="/brand/citi-logo.svg"] + .brand-fallback {
  display: inline-flex;
}

.brand-fallback {
  align-items: center;
  min-height: 34px;
  padding: 0 12px;
  border: 1px solid rgba(255, 255, 255, 0.28);
  border-radius: 4px;
  color: var(--surface);
  font-weight: 700;
}

.eyebrow {
  margin: 0 0 4px;
  color: #c7d6ea;
  font-size: 12px;
  font-weight: 700;
  text-transform: uppercase;
}

h1 {
  margin: 0;
  font-size: 20px;
  font-weight: 700;
  letter-spacing: 0;
}

.runtime-pill {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  min-height: 34px;
  padding: 0 12px;
  border: 1px solid rgba(255, 255, 255, 0.25);
  border-radius: 999px;
  color: #dce8f7;
  font-size: 13px;
  white-space: nowrap;
}

.runtime-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #33c481;
}

.workspace-layout {
  display: grid;
  grid-template-columns: minmax(320px, 380px) minmax(460px, 1fr) minmax(230px, 280px);
  gap: 16px;
  flex: 1;
  min-height: 0;
  padding: 16px;
}

.chat-column,
.canvas-column,
.status-column {
  min-height: 0;
  overflow: hidden;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  box-shadow: var(--shadow-soft);
}

@media (max-width: 1120px) {
  .app-shell {
    min-height: 100vh;
    overflow: auto;
  }

  .workspace-layout {
    grid-template-columns: 1fr;
    overflow: visible;
  }

  .chat-column,
  .canvas-column,
  .status-column {
    min-height: 360px;
  }
}
```

- [ ] **Step 6: Wire the shell into the page with temporary child content**

Replace `ui/src/app/page.tsx` with:

```tsx
import { AppShell } from "@/components/app-shell";

export default function Page() {
  return (
    <AppShell
      runtimeLabel="Local sample runtime"
      chat={<div className="panel-placeholder">Copilot chat loading</div>}
      canvas={<div className="panel-placeholder">Artifact workspace</div>}
      status={<div className="panel-placeholder">Agent activity</div>}
    />
  );
}
```

- [ ] **Step 7: Run the test and build**

Run:

```powershell
npm test -- src/components/app-shell.test.tsx
npm run build
```

Expected: test passes and Next build succeeds.

- [ ] **Step 8: Commit**

```powershell
git add ui/src/components/app-shell.tsx ui/src/components/app-shell.test.tsx ui/src/app/page.tsx ui/src/app/globals.css ui/public/brand/.gitkeep
git commit -m "feat: add Citi reporting workspace shell"
```

---

### Task 6: Artifact Canvas And Status Rail

**Files:**
- Create: `ui/src/components/artifact-canvas.tsx`
- Create: `ui/src/components/artifact-canvas.test.tsx`
- Create: `ui/src/components/status-rail.tsx`
- Create: `ui/src/components/status-rail.test.tsx`
- Modify: `ui/src/app/globals.css`

- [ ] **Step 1: Write failing artifact canvas tests**

Create `ui/src/components/artifact-canvas.test.tsx`:

```tsx
import "@testing-library/jest-dom/vitest";
import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import {
  applyArtifactEvent,
  createInitialArtifactState,
} from "@/lib/artifacts";
import { ArtifactCanvas } from "./artifact-canvas";

describe("ArtifactCanvas", () => {
  it("renders the empty reporting workspace", () => {
    render(<ArtifactCanvas state={createInitialArtifactState()} />);

    expect(screen.getByText("Reporting Workspace")).toBeInTheDocument();
    expect(screen.getByText("Ask Copilot to generate analysis, tables, charts, reports, or file links.")).toBeInTheDocument();
  });

  it("renders data tables from artifact state", () => {
    const state = applyArtifactEvent(createInitialArtifactState(), {
      type: "data-table",
      rows: [{ riskId: "RSK-001", severity: "High", status: "Open" }],
    });

    render(<ArtifactCanvas state={state} />);

    expect(screen.getByRole("button", { name: "Data" })).toHaveAttribute("aria-pressed", "true");
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

    expect(screen.getByRole("link", { name: "Download PPTX" })).toHaveAttribute("href", "/files/report.pptx");
  });
});
```

- [ ] **Step 2: Write failing status rail tests**

Create `ui/src/components/status-rail.test.tsx`:

```tsx
import "@testing-library/jest-dom/vitest";
import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import {
  applyStatusEvent,
  createInitialArtifactState,
} from "@/lib/artifacts";
import { StatusRail } from "./status-rail";

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
```

- [ ] **Step 3: Run tests and verify they fail**

Run:

```powershell
npm test -- src/components/artifact-canvas.test.tsx src/components/status-rail.test.tsx
```

Expected: FAIL because both components do not exist.

- [ ] **Step 4: Implement artifact canvas**

Create `ui/src/components/artifact-canvas.tsx`:

```tsx
"use client";

import { useMemo, useState } from "react";
import type { ArtifactState, ArtifactTab } from "@/lib/artifacts";

const tabs: { id: ArtifactTab; label: string }[] = [
  { id: "summary", label: "Summary" },
  { id: "data", label: "Data" },
  { id: "charts", label: "Charts" },
  { id: "report", label: "Report" },
  { id: "files", label: "Files" },
];

export function ArtifactCanvas({ state }: { state: ArtifactState }) {
  const [manualTab, setManualTab] = useState<ArtifactTab | null>(null);
  const activeTab = manualTab ?? state.activeTab;
  const headers = useMemo(
    () => Array.from(new Set(state.rows.flatMap((row) => Object.keys(row)))),
    [state.rows],
  );

  return (
    <div className="artifact-canvas">
      <div className="artifact-toolbar">
        <div>
          <p className="eyebrow dark">Generated output</p>
          <h2>Reporting Workspace</h2>
        </div>
        <div className="artifact-tabs" role="toolbar" aria-label="Artifact tabs">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              type="button"
              aria-pressed={activeTab === tab.id}
              onClick={() => setManualTab(tab.id)}
            >
              {tab.label}
            </button>
          ))}
        </div>
      </div>

      <div className="artifact-body">
        {activeTab === "summary" && (
          <section>
            <h3>{state.summaryTitle}</h3>
            {state.summary ? (
              <p className="report-copy">{state.summary}</p>
            ) : (
              <p className="empty-copy">
                Ask Copilot to generate analysis, tables, charts, reports, or file links.
              </p>
            )}
          </section>
        )}

        {activeTab === "data" && (
          <section className="table-shell">
            {state.rows.length === 0 ? (
              <p className="empty-copy">No data table has been generated.</p>
            ) : (
              <table>
                <thead>
                  <tr>
                    {headers.map((header) => (
                      <th key={header}>{header}</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {state.rows.map((row, index) => (
                    <tr key={`row-${index}`}>
                      {headers.map((header) => (
                        <td key={header}>{String(row[header] ?? "")}</td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </section>
        )}

        {activeTab === "charts" && (
          <section className="chart-list">
            {state.chartSeries.length === 0 ? (
              <p className="empty-copy">No chart data has been generated.</p>
            ) : (
              state.chartSeries.map((point) => (
                <div className="chart-row" key={point.label}>
                  <span>{point.label}</span>
                  <div className="chart-track">
                    <span style={{ width: `${Math.min(point.value * 3, 100)}%` }} />
                  </div>
                  <strong>{point.value}</strong>
                </div>
              ))
            )}
          </section>
        )}

        {activeTab === "report" && (
          <section className="report-preview">
            <h3>{state.reportTitle || "Report Preview"}</h3>
            {state.reportSections.length === 0 ? (
              <p className="empty-copy">No report preview has been generated.</p>
            ) : (
              state.reportSections.map((section) => (
                <article key={section.heading}>
                  <h4>{section.heading}</h4>
                  <p>{section.body}</p>
                </article>
              ))
            )}
          </section>
        )}

        {activeTab === "files" && (
          <section className="file-list">
            {state.files.length === 0 ? (
              <p className="empty-copy">No file links have been generated.</p>
            ) : (
              state.files.map((file) => (
                <a href={file.href} key={file.href}>
                  {file.label}
                </a>
              ))
            )}
          </section>
        )}
      </div>
    </div>
  );
}
```

- [ ] **Step 5: Implement status rail**

Create `ui/src/components/status-rail.tsx`:

```tsx
import type { StatusItem } from "@/lib/artifacts";

export function StatusRail({ statusItems }: { statusItems: StatusItem[] }) {
  return (
    <div className="status-rail">
      <div className="rail-header">
        <p className="eyebrow dark">Trace</p>
        <h2>Agent Activity</h2>
      </div>
      {statusItems.length === 0 ? (
        <p className="empty-copy">No agent activity yet.</p>
      ) : (
        <ol className="status-list">
          {statusItems.map((item) => (
            <li key={item.id}>
              <span className={`status-marker ${item.state}`} />
              <div>
                <p>{item.label}</p>
                <span>{item.state}</span>
              </div>
            </li>
          ))}
        </ol>
      )}
    </div>
  );
}
```

- [ ] **Step 6: Add component CSS**

Append these classes to `ui/src/app/globals.css`:

```css
.panel-placeholder,
.artifact-canvas,
.status-rail {
  height: 100%;
}

.artifact-canvas,
.status-rail {
  display: flex;
  flex-direction: column;
  min-height: 0;
}

.artifact-toolbar,
.rail-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  padding: 18px;
  border-bottom: 1px solid var(--border);
}

.artifact-toolbar h2,
.rail-header h2 {
  margin: 0;
  color: var(--citi-navy);
  font-size: 18px;
}

.eyebrow.dark {
  color: var(--text-muted);
}

.artifact-tabs {
  display: inline-flex;
  padding: 3px;
  background: var(--surface-strong);
  border-radius: 6px;
}

.artifact-tabs button {
  min-height: 32px;
  padding: 0 10px;
  border: 0;
  border-radius: 4px;
  background: transparent;
  color: var(--text-muted);
  cursor: pointer;
}

.artifact-tabs button[aria-pressed="true"] {
  background: var(--surface);
  color: var(--citi-blue);
  box-shadow: 0 2px 8px rgba(15, 22, 50, 0.12);
}

.artifact-body {
  flex: 1;
  min-height: 0;
  overflow: auto;
  padding: 22px;
}

.artifact-body h3 {
  margin: 0 0 14px;
  color: var(--citi-navy);
}

.report-copy,
.empty-copy,
.report-preview p {
  color: var(--text-muted);
  line-height: 1.55;
}

.table-shell {
  overflow: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
  font-size: 14px;
}

th {
  background: var(--citi-navy);
  color: var(--surface);
  text-align: left;
}

th,
td {
  padding: 12px;
  border-bottom: 1px solid var(--border);
}

tbody tr:nth-child(even) {
  background: var(--surface-muted);
}

.chart-list {
  display: grid;
  gap: 12px;
}

.chart-row {
  display: grid;
  grid-template-columns: 130px 1fr 48px;
  align-items: center;
  gap: 12px;
}

.chart-track {
  height: 10px;
  overflow: hidden;
  background: var(--surface-strong);
  border-radius: 999px;
}

.chart-track span {
  display: block;
  height: 100%;
  background: var(--citi-action);
}

.report-preview article {
  padding: 16px 0;
  border-top: 1px solid var(--border);
}

.report-preview h4 {
  margin: 0 0 8px;
  color: var(--citi-blue);
}

.file-list {
  display: grid;
  gap: 10px;
}

.file-list a {
  display: inline-flex;
  align-items: center;
  min-height: 38px;
  padding: 0 12px;
  border: 1px solid var(--border);
  border-radius: 6px;
  color: var(--citi-action);
  font-weight: 700;
  text-decoration: none;
}

.status-rail {
  padding-bottom: 16px;
}

.status-list {
  display: grid;
  gap: 14px;
  margin: 0;
  padding: 18px;
  list-style: none;
}

.status-list li {
  display: grid;
  grid-template-columns: 12px 1fr;
  gap: 10px;
}

.status-marker {
  width: 10px;
  height: 10px;
  margin-top: 6px;
  border-radius: 50%;
  background: var(--text-muted);
}

.status-marker.running {
  background: var(--citi-action);
}

.status-marker.complete {
  background: #33c481;
}

.status-marker.error {
  background: var(--citi-red);
}

.status-list p {
  margin: 0 0 4px;
  color: var(--text-primary);
  font-weight: 700;
}

.status-list span {
  color: var(--text-muted);
  font-size: 12px;
  text-transform: uppercase;
}
```

- [ ] **Step 7: Run tests and build**

Run:

```powershell
npm test -- src/components/artifact-canvas.test.tsx src/components/status-rail.test.tsx
npm run build
```

Expected: tests pass and Next build succeeds.

- [ ] **Step 8: Commit**

```powershell
git add ui/src/components/artifact-canvas.tsx ui/src/components/artifact-canvas.test.tsx ui/src/components/status-rail.tsx ui/src/components/status-rail.test.tsx ui/src/app/globals.css
git commit -m "feat: add artifact canvas and activity rail"
```

---

### Task 7: Chat Panel And Agent Bridge

**Files:**
- Create: `ui/src/components/chat-panel.tsx`
- Create: `ui/src/components/copilot-agent-bridge.tsx`
- Modify: `ui/src/app/page.tsx`
- Modify: `ui/src/app/globals.css`

- [ ] **Step 1: Create the chat panel component**

Create `ui/src/components/chat-panel.tsx`:

```tsx
"use client";

import { CopilotChat, useDefaultRenderTool } from "@copilotkit/react-core/v2";

const starterPrompts = [
  "Summarize the top operational risks.",
  "Draft an executive risk report.",
  "Compare issue trends by business unit.",
  "Generate a report outline from the latest metrics.",
];

export function ChatPanel() {
  useDefaultRenderTool();

  return (
    <div className="chat-panel">
      <div className="chat-header">
        <p className="eyebrow dark">Copilot</p>
        <h2>Risk Reporting Assistant</h2>
      </div>
      <div className="starter-prompts">
        {starterPrompts.map((prompt) => (
          <button key={prompt} type="button">
            {prompt}
          </button>
        ))}
      </div>
      <div className="chat-frame">
        <CopilotChat
          agentId="ops-risk-reporting"
          labels={{
            initial: "Ask for analysis, report drafts, data tables, charts, or file links.",
          }}
        />
      </div>
    </div>
  );
}
```

- [ ] **Step 2: Create the agent bridge**

Create `ui/src/components/copilot-agent-bridge.tsx`:

```tsx
"use client";

import { useFrontendTool } from "@copilotkit/react-core/v2";
import { z } from "zod";
import type { ArtifactEvent, StatusEvent } from "@/lib/artifacts";

interface CopilotAgentBridgeProps {
  onArtifact: (event: ArtifactEvent) => void;
  onStatus: (event: StatusEvent) => void;
}

const artifactSchema = z.object({
  type: z.enum(["markdown", "data-table", "chart", "report", "file-link"]),
}).passthrough();

const statusSchema = z.object({
  label: z.string(),
  state: z.enum(["queued", "running", "complete", "error"]),
});

export function CopilotAgentBridge({
  onArtifact,
  onStatus,
}: CopilotAgentBridgeProps) {
  useFrontendTool({
    name: "render_artifact",
    description:
      "Render generated analytics or reporting output in the main artifact canvas.",
    parameters: z.object({ artifact: artifactSchema }),
    handler: async ({ artifact }: { artifact: ArtifactEvent }) => {
      onArtifact(artifact);
      return "Artifact rendered in the reporting workspace.";
    },
  });

  useFrontendTool({
    name: "append_status",
    description:
      "Append a concise agent progress event to the activity trace rail.",
    parameters: z.object({ status: statusSchema }),
    handler: async ({ status }: { status: StatusEvent }) => {
      onStatus(status);
      return "Status appended to the activity rail.";
    },
  });

  return null;
}
```

- [ ] **Step 3: Wire the real workspace state into the page**

Replace `ui/src/app/page.tsx` with:

```tsx
"use client";

import { useState } from "react";
import { AppShell } from "@/components/app-shell";
import { ArtifactCanvas } from "@/components/artifact-canvas";
import { ChatPanel } from "@/components/chat-panel";
import { CopilotAgentBridge } from "@/components/copilot-agent-bridge";
import { StatusRail } from "@/components/status-rail";
import {
  applyArtifactEvent,
  applyStatusEvent,
  createInitialArtifactState,
} from "@/lib/artifacts";

export default function Page() {
  const [artifactState, setArtifactState] = useState(createInitialArtifactState);

  return (
    <>
      <CopilotAgentBridge
        onArtifact={(event) =>
          setArtifactState((state) => applyArtifactEvent(state, event))
        }
        onStatus={(event) =>
          setArtifactState((state) => applyStatusEvent(state, event))
        }
      />
      <AppShell
        runtimeLabel="Local sample runtime"
        chat={<ChatPanel />}
        canvas={<ArtifactCanvas state={artifactState} />}
        status={<StatusRail statusItems={artifactState.statusItems} />}
      />
    </>
  );
}
```

- [ ] **Step 4: Add chat CSS**

Append these classes to `ui/src/app/globals.css`:

```css
.chat-panel {
  display: flex;
  flex-direction: column;
  height: 100%;
  min-height: 0;
}

.chat-header {
  padding: 18px;
  border-bottom: 1px solid var(--border);
}

.chat-header h2 {
  margin: 0;
  color: var(--citi-navy);
  font-size: 18px;
}

.starter-prompts {
  display: grid;
  gap: 8px;
  padding: 14px;
  border-bottom: 1px solid var(--border);
  background: var(--surface-muted);
}

.starter-prompts button {
  min-height: 36px;
  padding: 0 10px;
  border: 1px solid var(--border);
  border-radius: 6px;
  background: var(--surface);
  color: var(--citi-action);
  cursor: pointer;
  font-weight: 700;
  text-align: left;
}

.chat-frame {
  flex: 1;
  min-height: 0;
}

.chat-frame > * {
  height: 100%;
}
```

- [ ] **Step 5: Run build verification**

Run:

```powershell
npm run build
```

Expected: build succeeds with no CopilotKit hook import errors.

- [ ] **Step 6: Commit**

```powershell
git add ui/src/components/chat-panel.tsx ui/src/components/copilot-agent-bridge.tsx ui/src/app/page.tsx ui/src/app/globals.css
git commit -m "feat: connect Copilot chat to reporting workspace"
```

---

### Task 8: Sample Backend Dependencies

**Files:**
- Modify: `pyproject.toml`
- Modify: `uv.lock`

- [ ] **Step 1: Add the AG-UI ADK dependency**

Run:

```powershell
uv add ag-ui-adk fastapi uvicorn pyyaml
```

Expected: `pyproject.toml` includes `ag-ui-adk`, `fastapi`, `uvicorn`, and `pyyaml`.

- [ ] **Step 2: Verify imports**

Run:

```powershell
@'
import ag_ui_adk
import fastapi
import uvicorn
import yaml
print("sample backend dependencies import")
'@ | uv run python -
```

Expected: prints `sample backend dependencies import`.

- [ ] **Step 3: Commit**

```powershell
git add pyproject.toml uv.lock
git commit -m "chore: add sample AG-UI backend dependencies"
```

---

### Task 9: Sample Backend Data Helpers

**Files:**
- Create: `sample_backend/demo_data.py`
- Create: `tests/unit/test_sample_backend_demo_data.py`

- [ ] **Step 1: Write failing backend helper tests**

Create `tests/unit/test_sample_backend_demo_data.py`:

```python
from sample_backend.demo_data import build_demo_artifacts, build_demo_statuses


def test_build_demo_statuses_returns_reporting_trace():
    statuses = build_demo_statuses()

    assert statuses == [
        {"label": "Querying sample operational risk data", "state": "running"},
        {"label": "Drafting executive reporting summary", "state": "running"},
        {"label": "Preparing report artifacts", "state": "complete"},
    ]


def test_build_demo_artifacts_returns_all_template_artifact_types():
    artifacts = build_demo_artifacts()

    assert [artifact["type"] for artifact in artifacts] == [
        "markdown",
        "data-table",
        "chart",
        "report",
        "file-link",
    ]
    assert artifacts[0]["title"] == "Executive Summary"
    assert artifacts[1]["rows"][0]["riskId"] == "RSK-001"
    assert artifacts[2]["series"][0]["label"] == "Payments"
    assert artifacts[3]["reportTitle"] == "Operational Risk Brief"
    assert artifacts[4]["files"][0]["label"] == "Sample report link"
```

- [ ] **Step 2: Run tests and verify they fail**

Run:

```powershell
uv run pytest tests/unit/test_sample_backend_demo_data.py -q
```

Expected: FAIL because `sample_backend.demo_data` does not exist.

- [ ] **Step 3: Implement demo data helpers**

Create `sample_backend/demo_data.py`:

```python
from __future__ import annotations


def build_demo_statuses() -> list[dict[str, str]]:
    return [
        {"label": "Querying sample operational risk data", "state": "running"},
        {"label": "Drafting executive reporting summary", "state": "running"},
        {"label": "Preparing report artifacts", "state": "complete"},
    ]


def build_demo_artifacts() -> list[dict[str, object]]:
    return [
        {
            "type": "markdown",
            "title": "Executive Summary",
            "content": (
                "Payment operations and third-party controls show the highest "
                "sample residual risk. The recommended next step is an executive "
                "brief focused on remediation ownership and aging exceptions."
            ),
        },
        {
            "type": "data-table",
            "rows": [
                {
                    "riskId": "RSK-001",
                    "businessUnit": "Payments",
                    "severity": "High",
                    "status": "Open",
                },
                {
                    "riskId": "RSK-002",
                    "businessUnit": "Markets",
                    "severity": "Medium",
                    "status": "Review",
                },
                {
                    "riskId": "RSK-003",
                    "businessUnit": "Treasury",
                    "severity": "Medium",
                    "status": "Mitigating",
                },
            ],
        },
        {
            "type": "chart",
            "series": [
                {"label": "Payments", "value": 18},
                {"label": "Markets", "value": 11},
                {"label": "Treasury", "value": 9},
            ],
        },
        {
            "type": "report",
            "reportTitle": "Operational Risk Brief",
            "sections": [
                {
                    "heading": "Top Findings",
                    "body": "Sample analysis indicates concentrated exposure in payment operations.",
                },
                {
                    "heading": "Recommended Actions",
                    "body": "Prioritize remediation ownership, aging exceptions, and executive review cadence.",
                },
            ],
            "files": [{"label": "Sample report link", "href": "/files/sample-report.pdf"}],
        },
        {
            "type": "file-link",
            "files": [{"label": "Sample report link", "href": "/files/sample-report.pdf"}],
        },
    ]
```

- [ ] **Step 4: Run tests and verify they pass**

Run:

```powershell
uv run pytest tests/unit/test_sample_backend_demo_data.py -q
```

Expected: PASS for both backend helper tests.

- [ ] **Step 5: Commit**

```powershell
git add sample_backend/demo_data.py tests/unit/test_sample_backend_demo_data.py
git commit -m "feat: add sample reporting backend data"
```

---

### Task 10: Sample FastAPI ADK Backend

**Files:**
- Create: `sample_backend/config/reporting_agent.yaml`
- Create: `sample_backend/prompts/reporting_agent.md`
- Create: `sample_backend/server.py`

- [ ] **Step 1: Create the demo agent config**

Create `sample_backend/config/reporting_agent.yaml`:

```yaml
name: ops_risk_reporting_sample
model: gemini-2.5-flash
app_name: ops_risk_reporting_sample
user_id: local_demo_user
```

- [ ] **Step 2: Create the demo prompt**

Create `sample_backend/prompts/reporting_agent.md`:

```markdown
You are a sample operational risk reporting agent for a CopilotKit UI template.

When the user asks for analytics or reporting, explain the sample finding briefly
and use the available frontend tools to render:

- status updates through `append_status`
- markdown summaries, data tables, charts, report sections, and file links
  through `render_artifact`

Use only sample data. Do not claim that the sample data represents real
Citigroup production information.
```

- [ ] **Step 3: Create the FastAPI AG-UI server**

Create `sample_backend/server.py`:

```python
from __future__ import annotations

from pathlib import Path
from typing import Any

import uvicorn
import yaml
from ag_ui_adk import ADKAgent, AGUIToolset, add_adk_fastapi_endpoint
from fastapi import FastAPI
from google.adk.agents import LlmAgent

from sample_backend.demo_data import build_demo_artifacts, build_demo_statuses

ROOT = Path(__file__).resolve().parent
CONFIG_PATH = ROOT / "config" / "reporting_agent.yaml"
PROMPT_PATH = ROOT / "prompts" / "reporting_agent.md"


def load_agent_config() -> dict[str, Any]:
    return yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8"))


def load_agent_prompt() -> str:
    prompt = PROMPT_PATH.read_text(encoding="utf-8")
    statuses = build_demo_statuses()
    artifacts = build_demo_artifacts()
    return (
        prompt
        + "\n\nUse these deterministic sample status payloads when demonstrating "
        + f"activity trace updates:\n{statuses}\n\n"
        + "Use these deterministic sample artifact payloads when demonstrating "
        + f"the reporting workspace:\n{artifacts}\n"
    )


def create_root_agent() -> LlmAgent:
    config = load_agent_config()
    return LlmAgent(
        name=config["name"],
        model=config["model"],
        instruction=load_agent_prompt(),
        tools=[AGUIToolset()],
    )


def create_app() -> FastAPI:
    config = load_agent_config()
    root_agent = create_root_agent()
    adk_agent = ADKAgent(
        adk_agent=root_agent,
        app_name=config["app_name"],
        user_id=config["user_id"],
        session_timeout_seconds=3600,
        use_in_memory_services=True,
    )

    app = FastAPI(title="Sample Ops Risk Reporting AG-UI Backend")
    add_adk_fastapi_endpoint(app, adk_agent, path="/")
    return app


app = create_app()


if __name__ == "__main__":
    uvicorn.run("sample_backend.server:app", host="127.0.0.1", port=8000, reload=True)
```

- [ ] **Step 4: Run import verification**

Run:

```powershell
@'
from sample_backend.server import app
print(app.title)
'@ | uv run python -
```

Expected: prints `Sample Ops Risk Reporting AG-UI Backend`.

- [ ] **Step 5: Commit**

```powershell
git add sample_backend/config/reporting_agent.yaml sample_backend/prompts/reporting_agent.md sample_backend/server.py
git commit -m "feat: add sample ADK AG-UI backend"
```

---

### Task 11: Local Run Documentation

**Files:**
- Modify: `ui/README.md`

- [ ] **Step 1: Replace the UI README**

Replace `ui/README.md` with:

```markdown
# CopilotKit ADK Reporting UI

This UI is a Citigroup-branded reporting analyst workspace for ADK agents.

## Runtime Shape

The browser points at the local Next.js CopilotKit runtime:

```text
NEXT_PUBLIC_COPILOTKIT_RUNTIME_URL=/api/copilotkit
```

The Next.js runtime proxies to the AG-UI backend:

```text
COPILOTKIT_AGENT_URL=http://127.0.0.1:8000/
```

For workplace migration, keep the UI and replace `COPILOTKIT_AGENT_URL` with
the workplace FastAPI/AG-UI endpoint.

## Brand Asset

Place the internal logo asset here when available:

```text
ui/public/brand/citi-logo.svg
```

The app shows fallback text when the logo file is absent.

## Run Locally

From the repository root:

```powershell
uv run python -m sample_backend.server
```

From `ui/`:

```powershell
npm run dev
```

Open:

```text
http://localhost:3000
```

## Verify

From `ui/`:

```powershell
npm test
npm run lint
npm run build
```

From the repository root:

```powershell
uv run pytest tests/unit
```
```

- [ ] **Step 2: Commit**

```powershell
git add ui/README.md
git commit -m "docs: add CopilotKit ADK UI run guide"
```

---

### Task 12: Final Verification

**Files:**
- No new files.

- [ ] **Step 1: Run frontend tests**

Run from `ui/`:

```powershell
npm test
```

Expected: all Vitest tests pass.

- [ ] **Step 2: Run frontend lint**

Run from `ui/`:

```powershell
npm run lint
```

Expected: no ESLint errors.

- [ ] **Step 3: Run frontend build**

Run from `ui/`:

```powershell
npm run build
```

Expected: Next.js production build succeeds.

- [ ] **Step 4: Run backend tests**

Run from repo root:

```powershell
uv run pytest tests/unit -q
```

Expected: unit tests pass.

- [ ] **Step 5: Start the sample backend**

Run from repo root in one terminal:

```powershell
uv run python -m sample_backend.server
```

Expected: FastAPI server listens at `http://127.0.0.1:8000/`.

- [ ] **Step 6: Start the UI**

Run from `ui/` in another terminal:

```powershell
npm run dev
```

Expected: Next.js dev server starts at `http://localhost:3000`.

- [ ] **Step 7: Manual UI verification**

Open `http://localhost:3000` and verify:

- Citi fallback brand text appears in the top shell.
- Chat panel renders.
- Artifact canvas renders with tabs.
- Agent activity rail renders.
- Sending a sample reporting prompt does not crash the UI.
- If the backend is not reachable, the UI remains visible and the chat reports a runtime error rather than blanking the page.

- [ ] **Step 8: Final commit**

If final verification required small fixes, commit them:

```powershell
git add ui sample_backend tests pyproject.toml uv.lock
git commit -m "chore: verify CopilotKit ADK reporting UI"
```

If no files changed after prior task commits, skip this commit and report that verification completed with no final patch.

---

## Self-Review Checklist

- Spec coverage: UI shell, Copilot chat, artifact canvas, status rail, local sample backend, runtime configurability, logo asset slot, error visibility, and verification are each represented by at least one task.
- Placeholder scan: no task asks a worker to invent missing behavior without a concrete file, command, or code block.
- Type consistency: artifact event names and state fields match across tests, helpers, UI components, and bridge tools.
- Scope control: authentication, production deployment, persistent chat history, and real workplace datasets are excluded.
