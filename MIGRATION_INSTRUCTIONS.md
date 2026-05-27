# Helix Migration Instructions

*Updated based on the exact `app/helix_agent/` folder structure.*

Since we have fully refactored this staging repository to mirror your production **Helix** environment, your migration is now a simple 1:1 copy operation! You can drag and drop the `app/helix_agent/` folder and the `files/` folder directly into your workspace.

## 1. Agent Logic (The Core Brains)
You will migrate your Python agent definitions. We use `agents.py` rather than YAML configs and `agent_utils.py`.

- **The Entry Point**: [app/helix_agent/agent.py](./app/helix_agent/agent.py)
  - *This file exports your Orchestrator as `root_agent`.*
- **The Agents**: [app/helix_agent/agents.py](./app/helix_agent/agents.py)
  - *This file contains all your native Python `Agent` definitions.*

## 2. Tools (Capabilities)
All custom Python tools have been consolidated into a single file to match Helix conventions.

- **Tools & Registry**: [app/helix_agent/tools.py](./app/helix_agent/tools.py)
  - *Contains the DuckDB query tool (`execute_duckdb_query`), the Skill Reader tools (`list_skills`, `read_skill`), the PDF generator (`generate_pdf_report`), the PPTX generator (`generate_ppt_report`), and the `REGISTRY` map.*
- **Database Files**: `data/*.csv`
  - *IMPORTANT: You must migrate `data/issues.csv` and `data/risk_metrics.csv` to your root directory. The DuckDB tool queries these local CSV files!*
- **Reporting Templates**: `data/designs/`
  - *You must migrate the `data/designs/` directory containing `template.html` and `template.pptx` for the Citi-branded reporting to work.*

## 3. Dependencies
Our custom code introduced net-new third-party dependencies that are not part of the standard ADK. You MUST migrate these into your Helix environment's `pyproject.toml` (or `requirements.txt`), and sync your environment.

- **Dependencies**: Add `duckdb`, `pandas`, `xhtml2pdf`, `jinja2`, and `python-pptx` to your Helix environment.
  - *Reference: See the `dependencies` array in our local [pyproject.toml](./pyproject.toml).*

## 4. Skills (Knowledge Base)
You should migrate your markdown files to the skills directory.

- Example: [app/helix_agent/skills/regulator_perspective.md](./app/helix_agent/skills/regulator_perspective.md)

## 5. Environment & Evaluation (Testing)
- **Environment**: [files/config/.env](./files/config/.env)
- **Evalset**: [tests/eval/evalsets/hierarchy_evalset.json](./tests/eval/evalsets/hierarchy_evalset.json)
- **Rubrics/Metrics**: [tests/eval/eval_config.json](./tests/eval/eval_config.json)

## 6. Critical Edge Cases & Gotchas
Before spinning up your Helix environment, verify the following:

- **The DuckDB Working Directory Trap**: In your agent definitions, the agent is told to query `'data/issues.csv'`. If your Helix startup script (`app.sh`) executes Python from inside the `app/` folder instead of the project root, DuckDB will try to find `app/data/issues.csv` and crash. If this happens, update the agent definitions to use absolute paths (e.g., `'/app/workspace/data/issues.csv'`) or relative paths (`'../data/issues.csv'`).
- **API Keys & Quotas**: Ensure your Helix secret manager has the `GOOGLE_API_KEY` correctly configured. The agent definitions hardcode the model to `gemini-2.5-flash`; ensure your environment has quota for this specific model variant to prevent 404/429 errors.
