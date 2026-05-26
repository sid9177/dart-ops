# Helix Migration Instructions

*Updated based on the exact `app/helix_agent/` folder structure.*

Since we have fully refactored this staging repository to mirror your production **Helix** environment, your migration is now a simple 1:1 copy operation! You can drag and drop the `app/helix_agent/` folder and the `files/` folder directly into your workspace.

## 1. Agent Logic & Factories (The Core Brains)
You will migrate both your YAML configurations AND your Python agent definitions.

- **The Entry Point**: [app/helix_agent/agent.py](./app/helix_agent/agent.py)
  - *This file exports your Orchestrator as `root_agent`.*
- **The Factory & Config Reader**: [app/helix_agent/agent_utils.py](./app/helix_agent/agent_utils.py)
  - *This file contains the `create_all_agents` logic that instantiates the ADK `Agent()` objects, as well as the YAML parsing logic.*
- **The Configs**: `app/helix_agent/sub_agents/*.yaml`
  - *The YAML files that `agent_utils.py` reads to dynamically inject the `instruction`, `model`, and `description`.*

## 2. Tools (Capabilities)
All custom Python tools have been consolidated into a single file to match Helix conventions.

- **Tools & Registry**: [app/helix_agent/tools.py](./app/helix_agent/tools.py)
  - *Contains the DuckDB query tool (`execute_duckdb_query`), the Skill Reader tools (`list_skills`, `read_skill`), and the `REGISTRY` map.*
- **Database Files**: `data/*.csv`
  - *IMPORTANT: You must migrate `data/issues.csv` and `data/risk_metrics.csv` to your root directory. The DuckDB tool queries these local CSV files!*

## 3. Skills (Knowledge Base)
You should migrate your markdown files to the skills directory.

- Example: [app/helix_agent/skills/regulator_perspective.md](./app/helix_agent/skills/regulator_perspective.md)

## 4. Environment & Evaluation (Testing)
- **Environment**: [files/config/.env](./files/config/.env)
- **Evalset**: [tests/eval/evalsets/hierarchy_evalset.json](./tests/eval/evalsets/hierarchy_evalset.json)
- **Rubrics/Metrics**: [tests/eval/eval_config.json](./tests/eval/eval_config.json)
