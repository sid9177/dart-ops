# Operational Risk Chat UI (Artifact Viewer) - Prompt Generation Design

## Goal
Design a set of highly optimized prompts that the user can feed to their work-provided coding agent. The coding agent will build a premium, enterprise-grade (Citigroup standards) Chat UI prototype with a Claude-like "Universal Artifact Viewer". The goal is to minimize the number of requests used (due to a 300 requests/month quota) by providing extremely comprehensive, zero-shot/few-shot capable prompts.

## Deliverable
Instead of building the code here, we will deliver a single Markdown file containing the sequenced prompts. These prompts will act as an airtight specification for the work agent to generate the UI flawlessly.

## Application Design (To be encoded into the prompts)

### 1. Architecture & Tech Stack
- **Framework:** Pure HTML, Vanilla CSS, Vanilla JS.
- **Constraints:** NO React, NO npm installs, NO complex build tools. 
- **Dependencies:** Google Fonts (Inter/Roboto), CDNs for markdown/diagram rendering (e.g., `marked.js`, `mermaid.js`).
- **File Structure:** `index.html`, `style.css`, `script.js` (or a single self-contained HTML file to save agent requests).

### 2. Layout & Components
- **Top Brand Bar:** Sleek, dark Citigroup-blue (`#002D72`) with the app title.
- **Left Panel (Chat Interface - 35%):** Modern chat bubbles, smooth scrolling, polished text input area.
- **Right Panel (Universal Artifact Viewer - 65%):** A dynamic canvas that renders different types of content based on tags in the chat.

### 3. Artifact Capabilities
The Artifact Viewer must support multiple rendering modes via simple JS parsing:
1. **Rich Markdown:** For formal Risk Assessments (using marked.js).
2. **Data Grids:** For interactive anomalies/risk events tables.
3. **Mermaid Diagrams:** For escalation flowcharts (using mermaid.js).
4. **Interactive UIs:** For remediation forms and approvals.

### 4. Aesthetics & Vibe
- **Enterprise Premium:** Soft shadows, crisp borders, glassmorphism elements, high information density but clean spacing.
- **Micro-animations:** Smooth fade-ins when the right panel populates, typing indicators in chat.

## Prompt Strategy (Optimizing for < 5 Requests)

To conserve the 300-request quota, the prompts will be structured to build the app in large, deterministic chunks:
1. **Prompt 1: The Master Layout & Styling System.** Builds the split-screen layout, CSS variables (Citi theme), and the base HTML structure.
2. **Prompt 2: The Chat Engine.** Implements the Vanilla JS for adding messages, typing indicators, and detecting `<artifact>` tags.
3. **Prompt 3: The Universal Artifact Renderer.** Implements the right-panel logic to render Markdown, Data Grids, Forms, and Mermaid diagrams using CDNs.
4. **Prompt 4: The Prototype Mock Script.** A hardcoded sequence demonstrating the UI (typing a query, receiving a reply, and rendering a rich artifact).

## Open Questions / Review
- Do the prompt chunks above make sense for your agent, or would your agent handle a single "Mega Prompt" better?
- Should the prompts instruct the agent to build this all in one `index.html` file to avoid file-switching errors, or separate files (`html/css/js`)?
