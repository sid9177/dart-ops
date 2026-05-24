# Dart-Ops Multi-Agent System Design

## 1. Overview
The goal is to rebuild the Operational Risk multi-agent system from a clean slate. The new architecture provides a highly extensible, performant framework that separates application code (managed in Git) from domain content (managed securely on the user's work machine).

## 2. Environment Strategy
- **Development (Personal Machine)**: Framework code, mock YAML configurations, mock CSV/Excel files, placeholder skills.
- **Production (Work Machine)**: Same framework code, but loaded with real Citi policies, real operational risk data (CSV/Excel), and real instruction sets.

## 3. Layered Architecture (Approach B)

### Layer 1: Data Engine
- **Technology**: DuckDB (in-memory) + pandas.
- **Responsibility**: Scans the `data/` directory on startup and automatically loads all `.csv`, `.xlsx`, and `.xls` files into DuckDB tables.
- **Capabilities**: Provides SQL querying and schema discovery tools dynamically to upper layers.

### Layer 2: Chapter Agents
- **Extensibility**: 100% config-driven. Adding a new chapter requires zero Python code.
- **Configuration**: Defined by YAML files (e.g., `issues.yaml`, `internal_losses.yaml`) specifying the agent's name, instruction, and the `tables_access` list restricting its SQL tools to specific datasets.

### Layer 3: Analysts
- **Expert Analyst**: Has cross-chapter query access to synthesize outputs from multiple chapter agents and identify correlations or discrepancies.
- **Reporting Agent**: Formats the synthesized findings into structured reports (Executive Summary, Gaps, Recommendations).

### Layer 4: Multi-Perspective Reviewer
- **Architecture**: A single highly capable Reviewer Agent.
- **Skills (Policies)**: Perspectives (1st LOD, 2nd LOD, Internal Audit, Regulator) are implemented as markdown files containing specific policies and criteria.
- **Execution**: The Reviewer Agent is run sequentially on the draft report, each time injected with a different perspective skill.

### Layer 5: Orchestrator & Fully Interactive HITL
- **Workflow**: The `PipelineOrchestrator` manages the end-to-end flow.
- **Human-in-the-Loop (HITL)**: The workflow pauses at every significant step for human review and approval:
  1. **Data Load Review**: Confirms which datasets and schemas were loaded.
  2. **Chapter Findings Review**: Presents the raw analytical findings from each chapter agent.
  3. **Draft Report Review**: Presents the synthesized report from the Analyst.
  4. **LOD Challenge Review**: If any perspective skill raises a challenge, the system halts, waits for human context/override, and then resumes.
  5. **Final Sign-Off**: The human approves the final vetted report for export.

## 4. Implementation Boundaries
Code lives in `dart_ops/*.py` and `agent.py` (root). Configurations live in `config/agents/`. Skills live in `skills/perspectives/`. Data lives in `data/`.

## 5. Next Steps
Once this design is approved, the implementation plan will involve setting up a clean scaffold, implementing the Data Engine and Chapter Factory, and then wiring the Fully Interactive Orchestrator.
