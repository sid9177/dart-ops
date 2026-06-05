# CopilotKit UI Design Specification

## Overview
This document outlines the design and architecture for adding a CopilotKit UI to the `dart-ops` Operational Risk agentic application. The goal is to provide an enterprise-grade, premium UI for a top-tier bank (Citigroup) while keeping the frontend strictly separated from the ADK Python backend, ensuring the backend remains portable to the Helix environment.

## Architecture & Technology Stack
* **Isolation:** The frontend will be isolated in a new `ui/` directory at the repository root.
* **Framework:** Next.js (App Router).
* **CopilotKit Version:** `@next` tag for all CopilotKit dependencies.
* **Styling:** Pure Vanilla CSS utilizing Citigroup's official aesthetic:
  * **Colors:** Citi Navy Blue (`#003B70`) for primary UI chrome/headers, crisp White for backgrounds, and Citi Red (`#FF0000`/`#C00000`) for primary action buttons and critical risk alerts.
  * **Typography:** Clean, legible sans-serif (e.g., matching Citi's corporate font styles like Interstate or Helvetica) with structured hierarchies.

## Components & Layout
The application will utilize a triple-pane layout:
1. **Left Sidebar (Agent Workflow Trace):** A collapsible panel that gives analysts transparency into the AI's "thought process." It will display a live feed of what the agents are doing (e.g., "Orchestrator delegating to Risk Analyst," "Querying DuckDB," "Generating PDF").
2. **Main Content Area (Center):** A polished enterprise dashboard displaying tabular operational risk data, such as a "Risk Metrics Overview" and an "Active Issues Tracker."
3. **Copilot Sidebar (Right):** The primary chat interface powered by `@copilotkit/react-ui`, highly customized to match the Citi aesthetic.

## Interaction Model
The Copilot will support a "tri-factor" interaction model:
1. **Workspace Control:** The agent can drive the main dashboard (e.g., applying complex natural-language filters to the data tables).
2. **Generative UI:** The agent can generate custom, interactive React components directly inside the chat stream (e.g., rendering a mini Risk Heatmap).
3. **Report Generation:** The agent can act as an async researcher, compiling heavy data into downloadable PDF/PPTX reports.

## Data Flow & Integration
1. **The Connection:** The CopilotKit React UI uses `runtimeUrl` to point to the local Python ADK backend endpoint.
2. **The Backend:** The ADK Python backend exposes an endpoint serving the CopilotKit protocol.
3. **The Interaction:** Chat history and state are sent to the backend. The ADK `orchestrator` agent receives the payload, delegates to sub-agents, and streams the final response (and tool calls for the Workflow Trace) back to the UI.

## Verification & Migration
* **Verification:** The UI will be tested locally against the `agents-cli playground` or a local FastAPI wrapper serving the ADK agents.
* **Migration:** Since the UI is isolated in `ui/`, the Python code in `app/helix_agent/` remains unpolluted and can be cleanly copy-pasted into the Helix environment per the `ARCHITECTURE.md` guidelines.
