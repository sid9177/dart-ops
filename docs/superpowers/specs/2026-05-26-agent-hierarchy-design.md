# Agent Hierarchy & Orchestration Design

## Purpose
Transition the existing flat agent architecture in `dart-ops` to a hierarchical delegation model. This addresses the vision of having a generic orchestrator, Chapter Subject Matter Experts (SMEs), and generic Analyst and Reporting agents.

## Architecture

### The Orchestrator
- **Role**: A lightweight router.
- **Responsibilities**: Receives user questions and delegates them to the appropriate Chapter SME based on the topic. It does not perform any data analysis or report formatting.

### Chapter SMEs (e.g., Issues, Risk Metrics)
- **Role**: Domain experts and "mini-managers" for their specific chapters.
- **Responsibilities**: Own the business logic and context for their domain. When they receive a request from the Orchestrator, they formulate data queries and presentation requirements. They delegate data extraction to the Analyst and formatting to the Reporter.

### The Analyst
- **Role**: Generic data query agent.
- **Responsibilities**: Executes DuckDB queries (or interacts with data sources) based on instructions from Chapter SMEs and returns raw data.

### The Reporter
- **Role**: Generic presentation agent.
- **Responsibilities**: Takes raw data and formatting instructions from Chapter SMEs to synthesize professional Markdown reports.

## Data Flow
1. User -> Orchestrator: "Show me high severity issues."
2. Orchestrator -> Issues SME: Forwards request.
3. Issues SME -> Analyst (via `ask_analyst` tool): "Query `data/issues.csv` for high severity issues."
4. Analyst -> Issues SME: Returns raw JSON data.
5. Issues SME -> Reporter (via `ask_reporter` tool): "Format this JSON into a Markdown summary."
6. Reporter -> Issues SME: Returns formatted Markdown.
7. Issues SME -> Orchestrator: Returns final report.
8. Orchestrator -> User.

## Required Code & Configuration Changes

1. **New Agents (`config/agents/`)**
   - Create `analyst.yaml`: Configured with the DuckDB execution tool.
   - Create `reporter.yaml`: Configured for text synthesis and markdown formatting.

2. **Update Existing Agents (`config/agents/`)**
   - Modify `issues.yaml` & `risk_metrics.yaml`: Remove `execute_duckdb_query` tool. Add `ask_analyst` and `ask_reporter` tools.
   - Modify `orchestrator.yaml`: Simplify instruction to act strictly as a router.

3. **Update Agent Factory (`dart_ops/agent_factory.py`)**
   - Extend `create_all_agents` to register `ask_analyst` and `ask_reporter` tools and attach them to the SMEs. 
   - Ensure the Analyst and Reporter agents are properly instantiated.

4. **Update Architecture Documentation (`ARCHITECTURE.md`)**
   - Explicitly document the "Hierarchical Delegation" pattern as a core project constraint.

## Error Handling & Testing
- If an Analyst query fails, the SME must be instructed to either retry with a corrected query or report the failure upstream to the Orchestrator.
- Test the flow via CLI to ensure the `ask_analyst` and `ask_reporter` tools correctly route requests and return string responses.
