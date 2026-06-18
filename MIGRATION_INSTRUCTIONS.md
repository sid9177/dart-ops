# Helix Migration Instructions

Because your Helix environment has drifted from this staging repository, **do not perform a 1:1 copy of the files.** Instead, manually apply the following structural and logical updates to your environment to sync the new capabilities without overwriting your custom logic.

## 1. Tools Architecture Refactor
We shifted away from a monolithic `tools.py` file to a scalable `tools/` package.

**What you need to do:**
1. Create a `tools/` directory inside your agent app folder.
2. Split your existing tools into domain-specific files (e.g., `duckdb_tool.py` for database queries, `report_tool.py` for PPTX/PDF generation).
3. Create a `tools/__init__.py` file to re-export your tools and maintain your `REGISTRY` map. For example:
   ```python
   from .duckdb_tool import execute_duckdb_query
   from .report_tool import generate_pdf_report, generate_ppt_report

   REGISTRY = {
       "execute_duckdb_query": execute_duckdb_query,
       "generate_pdf_report": generate_pdf_report,
       "generate_ppt_report": generate_ppt_report,
   }
   ```
4. Delete your old monolithic `tools.py` file and verify all agent imports point to the new package (e.g., `from app.helix_agent.tools import execute_duckdb_query`).

## 2. Removal of Dynamic Skill Reading
We determined that agents dynamically scanning the filesystem for their instructions (`list_skills`, `read_skill`) is an anti-pattern. Context should be injected directly into the agent's prompts.

**What you need to do:**
1. **Delete Tool Implementations**: Remove `list_skills`, `read_skill`, and `get_skills_dir` from your tools entirely.
2. **Update Agent Tool Lists**: Go into your agent definitions (specifically the orchestrator and any chapter agents like `issues_chapter`) and remove the skill reading tools from their `tools=[...]` array.
3. **Update Agent Instructions**: Edit the `instruction` or `system_prompt` for these agents. Remove any text that instructs the agent to "use list_skills to consult guidelines" or "read skills from the filesystem."
4. **Shift to Injection**: Instead of the agent fetching skills at runtime, ensure your application logic injects the contents of those markdown guidelines directly into the agent's instruction string when initializing the agent.

## 3. Dependency Updates
Ensure your environment's `pyproject.toml` or `requirements.txt` matches any new dependencies required by the decoupled tools.
- Verify `duckdb`, `pandas`, `xhtml2pdf`, `jinja2`, and `python-pptx` are installed.

## 4. Critical Edge Cases
- **DuckDB Pathing**: If your agents use relative paths (like `data/issues.csv`) in their instructions, ensure the DuckDB tool is aware of the exact working directory your Helix application boots from to prevent file-not-found crashes.

## 5. Lightweight Observability Plugin
We added native ADK observability to provide clean terminal output showing agent handoffs, tool usage, and LLM reasoning without massive data dumps.

**What you need to do:**
1. **Create the Plugin**: Add a `plugins.py` file to your agent directory containing a custom `LightweightObservabilityPlugin` class that inherits from `google.adk.plugins.base_plugin.BasePlugin`.
2. **Implement Callbacks**: In your custom plugin, override `before_agent_callback`, `before_tool_callback`, and `after_model_callback` to print concise logs (e.g., `print(f"[OBSERVABILITY] Agent '{callback_context.agent_name}' taken over")`). Ensure you gracefully handle missing attributes since the context models may occasionally lack them.
3. **Register the Plugin**: In your main application file (e.g., `agent.py`), import your new plugin and pass it to the `App` configuration:
   ```python
   from .plugins import LightweightObservabilityPlugin

   app = App(
       name="OpsDART",
       root_agent=root_agent,
       plugins=[LightweightObservabilityPlugin()]
   )
   ```

## 6. CopilotKit A2UI Frontend (Next.js UI)

> **IMPORTANT — This section replaces the old Section 6 (triple-pane layout)
> and Section 7 (Zero-Chat / Action-Only paradigm).** Those approaches are
> deprecated. The UI has been completely rebuilt as a CopilotKit v2 + A2UI
> native reporting workspace with official Citi design tokens.

The `ui/` directory now contains a **CopilotKit v2 + A2UI native reporting
workspace** that replaces the previous triple-pane shell. Key changes:

- **Two-pane layout**: `CopilotSidebar` (chat) on the left + `CanvasPane`
  (auto-composing report workspace) on the right. The old 3-pane shell
  (chat / artifact canvas / status rail) has been deleted.
- **A2UI catalog**: 13 hand-rolled Citi-styled React renderers (StatusChip,
  SuggestionButtons, ApprovalGate, MarkdownSummary, DataTable, ChartBar,
  ChartColumn, ChartLine, ChartDonut, KpiCard, HeatMap, ReportSection,
  FileLink) registered via `createCatalog()` from `@copilotkit/a2ui-renderer`.
- **Official Citi design system**: `globals.css` now uses the complete token
  ramp (100+ CSS variables) extracted directly from citigroup.com's live CSS.
  Includes the official Citi logo SVG, Overpass font (Google Fonts fallback
  for Citi-Sans), flat design (no box-shadows), regular-weight headings,
  2px/6px radius split, 200ms transitions.
- **Dedicated UI agent** in the ADK backend that receives analysis payloads
  from chapter SMEs and emits A2UI surfaces (see Section 7 below).
- **`useFrontendTool("register_surface")`** mirrors surface specs from the
  UI agent into the canvas pane state.
- **`useHumanInTheLoop("approval_gate")`** renders an HITL approval card
  in chat with Approve/Decline buttons (replaces the old Zero-Chat paradigm).

### What you need to do

1. **Copy the `ui/` Directory**: Copy the entire `ui/` directory from this
   repository into your Helix environment (or wherever your frontend is hosted).

2. **Install Dependencies**: Run `npm install` inside the `ui/` directory.
   All dependencies are on public npm registries:
   - `@copilotkit/react-core`, `@copilotkit/react-ui`, `@copilotkit/runtime`,
     `@copilotkit/a2ui-renderer`
   - `@ag-ui/client`
   - `next` (16.x), `react` (19.x), `zod`
   - No new charting or UI-kit dependencies (charts are hand-rolled SVG)

3. **Configure the ADK Backend URL**: Copy `ui/.env.example` to
   `ui/.env.local` and set `COPILOTKIT_AGENT_URL` to your Helix ADK
   FastAPI endpoint:
   ```bash
   # ui/.env.local
   COPILOTKIT_AGENT_URL=http://127.0.0.1:${APP_PORT}/
   ```
   The URL **MUST end with a trailing slash** because `ag-ui-adk` mounts
   the AG-UI SSE endpoint at `path="/"`.

   **Your Helix backend uses two environment variables:**
   - `APP_PORT` — the port number the FastAPI server listens on
   - `RUN_MODE` — controls the host:
     - `RUN_MODE=cluster` → backend binds to `0.0.0.0` (all interfaces)
     - `RUN_MODE=<other>` → backend binds to `127.0.0.1` (localhost only)

   When both UI and backend run on the same machine, use
   `http://127.0.0.1:${APP_PORT}/` regardless of `RUN_MODE`. When the UI
   runs on a different machine and `RUN_MODE=cluster`, use the backend
   machine's hostname: `http://your-helix-host:${APP_PORT}/`.

   **How to find your work laptop's APP_PORT and RUN_MODE:**
   - Check your Helix environment variables:
     `echo %APP_PORT%` and `echo %RUN_MODE%` (Windows)
     or `echo $APP_PORT` and `echo $RUN_MODE` (Linux/Mac)
   - Run `netstat -ano | findstr LISTENING` on the work laptop to see
     which ports have servers
   - Test: `curl http://127.0.0.1:${APP_PORT}/` — if you get a response
     (not "connection refused"), that's the right URL

4. **Runtime Route**: The Next.js API route at
   `src/app/api/copilotkit/route.ts` (and the catch-all at
   `src/app/api/copilotkit/[[...slug]]/route.ts`) creates a `CopilotRuntime`
   with `a2ui: {}` which advertises A2UI capability via the `/info`
   endpoint. No changes needed unless you change the basePath.

5. **Deploy the Frontend**: Deploy the Next.js application independently of
   the Python backend (e.g., using Vercel, Node server, or your internal
   hosting). The backend remains purely Python and does not need to serve
   the frontend files.

### What was deleted (do NOT carry these over)

If you previously copied the old UI, remove these files — they no longer
exist in the new `ui/`:
- `src/components/app-shell.tsx` (and `.test.tsx`)
- `src/components/artifact-canvas.tsx` (and `.test.tsx`)
- `src/components/chat-panel.tsx`
- `src/components/status-rail.tsx` (and `.test.tsx`)
- `src/components/copilot-agent-bridge.tsx`
- `src/lib/artifacts.ts` (and `.test.ts`) — replaced by `surface-types.ts`

### Verification after migration

1. `cd ui && npm test` — 13 tests should pass
2. `cd ui && npx tsc --noEmit` — no type errors
3. `cd ui && npm run lint` — 0 errors
4. Start the ADK backend, then `cd ui && npm run dev`, open
   `http://localhost:3000` — the page should load with the Citi logo, a
   chat sidebar, and the canvas empty state ("Ask Copilot to generate
   analysis, tables, charts, or reports."). Console should show 0 errors.

## 7. Dedicated UI Agent in ADK Backend

A new `ui_agent` has been added to the ADK multi-agent system. It receives
analysis payloads from the orchestrator (after chapter SMEs produce content)
and composes A2UI surfaces for the reporting workspace.

### What you need to do

1. **Copy the UI agent file**: Copy `app/helix_agent/agents/ui_agent.py`
   to your Helix environment's agents directory.

2. **Copy the UI agent instruction**: Copy `app/helix_agent/skills/ui_agent.md`
   to your Helix environment's skills directory. This markdown file is the
   UI agent's instruction (configuration-over-code — not hardcoded in
   Python). It documents all 13 catalog components and the rules for when
   to emit each.

3. **Update the orchestrator**: Add `ui_agent_tool` to the orchestrator's
   tools list so it can route to the UI agent after chapter SMEs return:

   ```python
   from .ui_agent import ui_agent_tool

   orchestrator = Agent(
       name="orchestrator",
       # ... existing config ...
       tools=[issues_chapter_tool, risk_metrics_chapter_tool, ui_agent_tool]
   )
   ```

   Also update the orchestrator's instruction to route to the UI agent:
   ```
   After receiving analysis from the Chapter SME, you MUST route the result
   to the ui_agent tool to compose the reporting workspace surfaces.
   CRITICAL: You must ask for approval via the ui_agent's approval_gate
   BEFORE concluding.
   ```

4. **No new Python dependencies**: The UI agent uses `google.adk.agents.Agent`
   and `google.adk.tools.AgentTool` (already in ADK 1.31). A2UI operations
   are emitted via `ag-ui-adk` which is already in your environment.

### How the UI agent works

The UI agent's instruction (`ui_agent.md`) tells it:
- The 13 available A2UI catalog components and their Zod props schemas
- When to emit each (e.g., "use ChartBar for category comparisons,
  ChartLine for trends, ChartDonut for distribution, HeatMap for risk
  matrices, KpiCard for single metrics")
- To emit surfaces in the order they should appear in the report
- To call the `register_surface` frontend tool once per surface (for the
  canvas mirror)
- To call the `approval_gate` frontend tool when the orchestrator needs
  approval (HITL)
- To emit StatusChip at the start and end of composition
- To emit SuggestionButtons with 2-3 follow-up prompts at the end

### Frontend tools the UI agent calls

Two frontend tools are registered by `ui/src/components/surface-bridge.tsx`:

1. **`register_surface`** (via `useFrontendTool`): The UI agent calls this
   once per A2UI surface it emits. The frontend stores the surface spec in
   canvas state. The canvas pane renders all registered surfaces in emit
   order.

2. **`approval_gate`** (via `useHumanInTheLoop`): The UI agent calls this
   when the orchestrator needs user approval. The frontend renders an
   approval card in chat with Approve/Decline buttons. The agent run pauses
   until the user responds. This replaces the old "Zero-Chat / Action-Only"
   paradigm from the previous Section 7.

## 8. Official Citi Design System

The UI now uses the **official Citi design system** extracted directly from
citigroup.com's live CSS (not an approximation). This is critical for the
UI to look like the Citi UI team designed it.

### Key design tokens (all in `ui/src/app/globals.css`)

| Category | Token | Hex | Usage |
|----------|-------|-----|-------|
| Primary brand | `--citi-blue-300` | `#002D72` | Deep navy (header, footer, table headers) |
| Action blue | `--citi-action` | `#255BE3` | Links, primary buttons, focus rings |
| Brand blue | `--citi-blue-200` | `#0041A5` | Secondary brand blue |
| Bright blue | `--citi-blue-100` | `#005FF1` | Bright accent |
| Accent cyan | `--citi-cyan` | `#00BDF2` | Cyan accent |
| App background | `--gray-050` | `#F6F8FA` | Main background |
| Panel surface | `--white` | `#FFFFFF` | Cards, panels |
| Border | `--gray-150` | `#D9E2EA` | All borders |
| Text primary | `--gray-900` | `#1D2834` | Body text |
| Text muted | `--gray-600` | `#4F6F90` | Secondary text |
| Error | `--red-300` | `#B60000` | Errors / critical |
| Success | `--forest-200` | `#00B755` | Positive / success |
| Warning | `--yellow-200` | `#FFCD00` | Warning |
| Alert | `--orange-200` | `#ED8B00` | Alert |

### Critical Citi design rules

1. **Flat design**: `box-shadow: none` on all components. Depth via color
   contrast, not shadows.
2. **Regular-weight headings (400)**: H1/H2/H3 use `font-weight: 400`, NOT
   bold. Only eyebrow labels are 700 + uppercase + 2.22px letter-spacing.
3. **2px radius for panels, 6px for buttons/inputs**: Subtle, not
   pill-shaped.
4. **200ms transitions** with `cubic-bezier(0.6, 0, 1, 1)`.
5. **`#255BE3` is the single action color** for all interactive elements.
6. **`#FF3C28` red is logo-arc-only** — never use in UI chrome.

### Logo

The official Citi logo SVG is at `ui/public/brand/citi-logo.svg`. It was
decoded from citigroup.com's live base64. The logo has:
- Wordmark "citi" (lowercase) in `#255BE3` (action blue)
- Arc over the "i" in `#FF3C28` (signature red)
- ViewBox: `0 0 204 118`, flat, no gradients

### Fonts

- **Primary**: `Citi-Sans-Text-Regular` (proprietary — uses locally-installed
  Citi-Sans if present on the work laptop)
- **Fallback 1**: `Interstate_Light` (proprietary — older Citi standard)
- **Fallback 2**: `Overpass` (open-source, OFL, loaded from Google Fonts via
  `next/font/google` — citigroup.com itself uses this as the official
  fallback)
- **Final fallback**: `system-ui, sans-serif`

No action needed — the font stack is already in `globals.css` and Overpass
is loaded in `layout.tsx`. If Citi-Sans or Interstate is installed on the
work laptop, it will be used automatically.

## 9. Deprecated: Zero-Chat / Action-Only Paradigm

The previous Section 7 ("Zero-Chat / Action-Only UI Integration") is
**deprecated and removed**. The `display_in_center` and
`provide_suggestions` tools are no longer used. The new architecture uses:

- **A2UI surfaces** for all agent-generated UI (charts, tables, reports,
  summaries, file links)
- **`register_surface` frontend tool** for canvas composition
- **`approval_gate` frontend tool** (via `useHumanInTheLoop`) for HITL
- **`StatusChip` A2UI component** for progress indicators
- **`SuggestionButtons` A2UI component** for follow-up prompts

If you previously implemented the Zero-Chat paradigm, remove
`display_in_center` and `provide_suggestions` tools from your agents and
delete any frontend code that intercepts them.