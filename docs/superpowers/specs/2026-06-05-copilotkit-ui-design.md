# CopilotKit UI Design Specification

## Overview
This document outlines the design and architecture for adding a CopilotKit UI to the `dart-ops` Operational Risk agentic application. The goal is to provide an enterprise-grade, premium UI for a top-tier bank while keeping the frontend strictly separated from the ADK Python backend, ensuring the backend remains portable to the Helix environment.

## Architecture & Technology Stack
* **Isolation:** The frontend will be isolated in a new `ui/` directory at the repository root. This ensures `dart-ops` remains a clean Python backend staging area.
* **Framework:** Next.js (App Router).
* **CopilotKit Version:** `@next` tag (latest next version) for all CopilotKit dependencies (e.g., `@copilotkit/react@next`, `@copilotkit/core@next`).
* **Styling:** Pure Vanilla CSS with a polished, premium design system (custom CSS variables, modern typography like Inter/Roboto, subtle glassmorphism) tailored for an enterprise banking aesthetic.

## Components & Layout
* **Global Layout:** 
  * A persistent top navigation bar featuring the bank logo and user profile.
  * A main central content area.
  * A collapsible right-hand drawer (the Copilot Sidebar).
* **Main Content Area:** A polished enterprise dashboard displaying tabular operational risk data, such as a "Risk Metrics Overview" and "Active Issues Tracker."
* **Copilot Sidebar:** Powered by `@copilotkit/react-ui`. This sidebar will be heavily customized using CSS to match the dark/light mode premium aesthetic of the bank, avoiding a generic widget look.

## Data Flow & Integration
1. **The Connection:** The CopilotKit React UI will use the `runtimeUrl` property on the `<CopilotKitProvider>` to point to the local Python ADK backend endpoint.
2. **The Backend:** The ADK Python backend will expose an endpoint to serve the CopilotKit protocol.
3. **The Interaction:** When the user types a message in the sidebar, CopilotKit sends the chat history and current frontend state to the Python backend. The ADK `orchestrator` agent receives the payload, delegates to sub-agents (`analyst`, `reporter`), and streams the final response back to the UI.

## Verification & Migration
* **Verification:** The UI will be tested locally against the `agents-cli playground` or a local FastAPI wrapper serving the ADK agents.
* **Migration:** Since the UI is isolated in `ui/`, the Python code in `app/helix_agent/` remains unpolluted and can be cleanly copy-pasted into the Helix environment per the `ARCHITECTURE.md` guidelines.
