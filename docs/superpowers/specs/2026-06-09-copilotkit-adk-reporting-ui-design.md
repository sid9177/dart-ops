# CopilotKit ADK Reporting UI Design

## Overview

Build a Citigroup-branded Reporting Analyst Workspace for this ADK staging
project. The UI is a portable Next.js and CopilotKit template that can run
against a small local FastAPI sample backend during development, then be
repointed to workplace ADK agents by changing the CopilotKit runtime URL and
backend business logic.

The primary workflow is analytics and reporting:

1. Ask the agent for analysis.
2. Inspect generated artifacts.
3. Refine the analysis through chat.
4. Review report-ready output.
5. Export or follow generated file links where available.

This design intentionally prioritizes a chat-led reporting workspace over a
monitoring dashboard. The app should feel like an internal enterprise analyst
tool, not a marketing page.

## Goals

- Provide a reusable CopilotKit UI template for workplace ADK agents.
- Support analytics and reporting workflows as the main use case.
- Include a small local sample FastAPI backend so the template runs end to end.
- Keep the frontend isolated under `ui/` for easy migration.
- Use Citigroup-style UI structure, colors, logo placement, tables, status
  badges, tabs, buttons, and report surfaces.
- Keep all brand colors centralized as CSS variables.
- Provide a logo asset slot under `ui/public/brand/` and use fallback brand text
  when the official internal logo asset is absent.

## Non-Goals

- Do not add production deployment infrastructure.
- Do not add real Citi authentication or SSO.
- Do not add persistent chat history.
- Do not hardcode workplace datasets or business logic.
- Do not fabricate an official Citi logo; the UI should expect an internal
  asset to be supplied.
- Do not build full production PDF or PPTX generation unless existing sample
  tools already provide simple links.

## Product Shape

The first screen is a Reporting Analyst Workspace:

- Left panel: CopilotKit chat as the main command surface.
- Main canvas: artifact viewer for generated analysis, markdown reports, data
  tables, charts, report previews, and files.
- Slim status rail: collapsible agent activity feed for tool calls and progress.

This supports the workflow `ask -> analyze -> inspect artifact -> refine ->
report`. The chat drives the work, while the main canvas gives generated
outputs enough room to be useful.

## Frontend Architecture

The frontend remains isolated in `ui/` and uses the existing Next.js App Router
project.

Expected frontend elements:

- `CopilotKit` provider configured from an environment variable such as
  `NEXT_PUBLIC_COPILOTKIT_RUNTIME_URL`.
- Citi app shell with top bar, logo slot, title, runtime status, and compact
  utility actions.
- Copilot chat panel using CopilotKit React UI.
- Artifact canvas with tabs for `Summary`, `Data`, `Charts`, `Report`, and
  `Files`.
- Citi-styled report preview and table components.
- Collapsible status trace rail.
- Starter prompts for analytics and reporting tasks.
- Runtime connection state UI for connected, disconnected, and error states.

The UI should use reusable components rather than embedding the full experience
inside one page component. Suggested boundaries:

- App shell and layout.
- Chat panel.
- Artifact canvas.
- Artifact type renderers.
- Status trace rail.
- Runtime status indicator.
- Starter prompt controls.

## Backend Architecture

Add a small local FastAPI sample backend for development only. It should be
clearly marked as a demo backend and should not contain workplace business
logic.

The backend should expose a CopilotKit-compatible endpoint for the frontend
runtime URL. It should wrap a sample ADK agent and provide demonstration
behavior for:

- Producing a markdown analysis artifact.
- Producing a tabular JSON artifact.
- Producing chart-ready data.
- Emitting visible progress or status trace events.
- Returning simple report metadata or a generated-file link where available.

The workplace migration path is to replace the backend implementation and
runtime URL while keeping the UI shell and artifact renderers.

## Data Flow

1. The user sends a reporting or analytics prompt through the CopilotKit chat.
2. The frontend sends the request to `NEXT_PUBLIC_COPILOTKIT_RUNTIME_URL`.
3. The local sample FastAPI backend routes the request to the demo ADK agent.
4. Agent and tool responses update chat, the status rail, and artifact canvas.
5. The artifact canvas renders generic artifact state, not workplace-specific
   assumptions.
6. In a workplace migration, the frontend points to the real ADK backend with
   the same UI contract.

## UI Capabilities

### Citi App Shell

The shell includes a logo slot, app title, compact runtime indicator, and small
utility controls. If `ui/public/brand/citi-logo.svg` or an equivalent internal
asset is present, the shell uses it. Otherwise it shows fallback text such as
`Citi | Ops Risk`.

### Copilot Chat Panel

The chat panel is the main command surface. It should include starter prompts
such as:

- Summarize the top operational risks.
- Draft an executive risk report.
- Compare issue trends by business unit.
- Generate a report outline from the latest metrics.

### Artifact Canvas

The canvas provides enough horizontal space for generated outputs. Initial
artifact types are:

- Markdown summary.
- Data table.
- Chart-ready data.
- Report preview.
- File links.

The first implementation can use simple renderers and reserve richer charts or
document previews for later.

### Status Trace Rail

The status rail is collapsible and secondary. It should show steps such as:

- Connecting to runtime.
- Querying sample data.
- Drafting analysis.
- Preparing report preview.
- Returning file links.
- Tool or agent errors.

It should help analysts understand what the agent is doing without competing
with the report canvas.

## Error Handling

- Backend unavailable: show a connection banner and keep the rest of the UI
  usable.
- Agent or tool error: show the error in chat and status rail without crashing
  the artifact canvas.
- Missing logo asset: show fallback brand text.
- Empty artifact state: show starter prompts and a report workspace placeholder.
- Malformed artifact payload: show a readable error in the relevant artifact
  tab and preserve the raw metadata where useful for debugging.

## Testing And Verification

Frontend verification:

- Run the Next.js build or typecheck.
- Run UI linting.
- Add focused tests for artifact parsing or rendering helpers if the project
  test setup supports it cleanly.
- Manually verify the workspace renders locally and can point at the sample
  backend.

Backend verification:

- Run existing Python tests when backend code changes.
- Add focused tests for the sample backend contract if it introduces pure helper
  functions.
- Verify the sample endpoint can return demo chat, status, and artifact data.

End-to-end verification:

- Start the sample backend.
- Start the Next.js dev server.
- Send at least one reporting prompt.
- Confirm chat, status rail, and artifact canvas all update.

## Migration Notes

The UI should be easy to transfer into workplace projects because:

- It lives under `ui/`.
- Runtime URL is environment-driven.
- Brand assets are external files.
- Artifact renderers are generic.
- The sample backend is separate from workplace business logic.

The implementation plan should keep changes surgical and avoid coupling the
Next.js UI to `app/helix_agent/` internals beyond the local demo backend.
