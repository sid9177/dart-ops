# YAML Tool Registry Design

## Goal
To strictly adhere to the "Configuration Over Code Changes" architecture constraint by moving all agents (including the Orchestrator) to a YAML-driven configuration, while introducing a stable and explicit way to assign Python tools to agents via a Tool Registry.

## Architecture & Components

### 1. The Tool Registry (`dart_ops/tool_registry.py`)
A central dictionary mapping string names to actual Python tool functions.
This separates configuration (strings) from implementation (Python functions).
- `REGISTRY`: A dictionary initialized with statically available tools (e.g., `execute_duckdb_query`).

### 2. YAML Configuration Updates
All agent configurations (both Chapter Agents and Orchestrator) will include a `tools` list.
Example:
`config/agents/expert_analyst_agent.yaml`
```yaml
name: "Expert_Analyst_Orchestrator"
instruction: "..."
tools:
  - "ask_issues_chapter"
  - "ask_risk_metrics_chapter"
```

### 3. Dynamic Registry Updates
The `factory.py` will dynamically create the "chapter caller" functions (which allow the Orchestrator to query chapter agents). Instead of directly binding them to the Orchestrator, it will inject them into the `REGISTRY` at runtime.

### 4. Refactoring `factory.py`
The factory logic will be updated to:
- Read the `tools` array from the parsed YAML dictionary.
- Iterate over the tool names and fetch the corresponding Python function from the `REGISTRY`.
- Wrap the function in a Google ADK `FunctionTool` and attach it to the `Agent` instance.

### 5. Refactoring `orchestrator.py`
The current hardcoded instruction and name in `orchestrator.py` will be removed. The file will be simplified to utilize the factory to build the orchestrator from `config/agents/expert_analyst_agent.yaml`.

## Open Questions / Clarifications
- None. This design strictly adheres to the ADK constraints and project architecture.

## Verification
- Test that chapter agents successfully receive `execute_duckdb_query` through the registry.
- Test that the Orchestrator successfully receives the dynamically registered chapter-calling tools.
- Test the full agent loop using `agents-cli playground` or running pytest.
