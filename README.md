# dart-ops (Staging Environment for Helix)

This repository serves as a staging and development area for building Operational Risk AI Agents using the Google Agent Development Kit (ADK). The code here is designed to be highly portable so that it can be cleanly copy-pasted directly into the production **Helix** environment.

## Project Architecture

The agent architecture is written entirely in modular Python to match the target Helix environment structure. 

```text
dart-ops/
├── app/
│   └── helix_agent/
│       ├── agent.py               # Main entry point exporting the `app` and `root_agent` (Orchestrator)
│       ├── agents/                # Individual agent definitions
│       │   ├── orchestrator.py    # Central router
│       │   ├── analyst.py         # Data extraction specialist
│       │   ├── reporter.py        # Report generation specialist
│       │   ├── issues_chapter.py  # Domain SME for Issues
│       │   └── risk_metrics_chapter.py # Domain SME for Risk Metrics
│       └── tools/                 # Agent capabilities
│           ├── __init__.py        # Exports the central tool REGISTRY
│           ├── duckdb_tool.py     # SQL execution on local CSVs
│           └── report_tool.py     # PDF and PPTX report generation
├── data/                          # Mock data and templates
│   ├── issues.csv                 # Queried by DuckDB
│   ├── risk_metrics.csv           # Queried by DuckDB
│   └── designs/                   # HTML/PPTX templates for the reporter
├── files/                         # Output directory for generated reports
├── tests/                         # Unit and integration tests
├── MIGRATION_INSTRUCTIONS.md      # Instructions for porting to Helix
└── pyproject.toml                 # Project dependencies
```

## Core Workflows & Design Patterns

1. **Modular Agents**: Each agent is defined in its own file under `app/helix_agent/agents/` and exported as an `AgentTool` so it can be delegated to by other agents. The `orchestrator` acts as the central router and root agent.
2. **Specialized Tools**: Tools are logically separated in the `app/helix_agent/tools/` package. Agents are only given the tools they strictly need to perform their jobs. We intentionally avoid giving agents dynamic file-system readers for skills; instead, any necessary instructional context should be injected at initialization.
3. **In-Memory Data**: For development and staging, tabular data is queried directly from local CSVs in the `data/` folder using `duckdb`.

## Development & Testing

This project uses `uv` for dependency management and `pytest` for testing.

```bash
# Install dependencies
uv sync

# Run the test suite
uv run pytest tests/unit tests/integration

# Test locally using the interactive playground
uv run agents-cli playground
```

## Migrating to Production (Helix)

Because this repository acts as a staging ground, we do not deploy infrastructure directly from here. When an agent or feature is ready, refer to the [MIGRATION_INSTRUCTIONS.md](MIGRATION_INSTRUCTIONS.md) file for the exact steps to safely migrate the code into the target Helix environment.

> **Note for AI Assistants**: When continuing development in this repository, follow the `GEMINI.md` guidelines strictly. Prioritize making robust, portable changes to `app/helix_agent/` and ensuring `MIGRATION_INSTRUCTIONS.md` stays up to date.
