# Operational Risk Multi-Agent System Design

## Purpose
A highly scalable, high-performance multi-agent system for Operational Risk Reporting and Analytics. The system uses Google ADK and handles large Excel/CSV datasets. It is designed as a "copy-paste" staging environment where users can configure chapters, policies, and perspectives purely through configuration files without altering Python code.

## Architecture
The system follows a Central Orchestrator pattern coupled with a Config-Driven Agent Factory.

### Components
1. **Agent Factory (`factory.py`)**: Dynamically instantiates ADK agents based on configuration.
2. **Configuration (`config/chapters.yaml`)**: The source of truth for all agents. Defines:
   - Agent names (Chapters, e.g., Issues, Risk Metrics)
   - Data sources (paths to large CSVs)
   - Instructions and Skill references
3. **Skills & Perspectives**: Stored as simple Markdown files (e.g., `skills/regulator_perspective.md`) that the YAML configuration references. This allows purely text-based modifications for 1st LOD, 2nd LOD, Audit, and Regulator views.
4. **Data Engine & Tools (`tools/duckdb_tool.py`)**: A generic, highly performant DuckDB tool given to Chapter Agents. It executes SQL against large files with zero lag.

### Scalability Guarantees
- **Scaling Agents**: Add a new block to `chapters.yaml`. Zero Python code changes required.
- **Scaling Skills**: Drop a new `.md` file into the `skills/` directory and reference its filename in the YAML. The orchestrator will automatically read and apply the new policy/perspective. Zero Python code changes required.
- **Scaling Tools**: The system will use a dynamic Tool Registry. While we are starting with DuckDB for data, if you ever need a new tool (e.g., an internal API fetcher), an engineer simply drops a new Python file into the `tools/` folder. You can then instantly assign that tool to any agent by simply typing its name in the YAML file (e.g., `tools: [duckdb_tool, internal_api_tool]`).

5. **Central Orchestrator**: The Expert Analyst agent that receives user queries, delegates to appropriate Chapter Agents, synthesizes results, and passes them to a Reporting Agent.

## Data Flow
1. User prompt is received.
2. Central Orchestrator parses the prompt and identifies required chapters and perspectives.
3. Orchestrator delegates tasks to dynamically generated Chapter Agents.
4. Chapter Agents use the DuckDB tool to execute SQL against their specific CSV files.
5. Chapter Agents return insights to Orchestrator.
6. Orchestrator synthesizes findings and sends them to the Reporting Agent.
7. Reporting Agent formats the final output.

## Error Handling
- DuckDB query failures (e.g., invalid SQL) are caught and returned to the agent for self-correction.
- Missing configuration files or invalid YAML syntax fail gracefully with clear, actionable human-readable messages.

## Scope & Implementation Notes
This project focuses purely on agent logic, configuration parsing, and local execution. No CI/CD, deployment, or infrastructure code will be developed, as the target Helix environment provides its own infrastructure.
