# Helix Migration Instructions

*Updated based on Helix architecture being a wrapper around ADK.*

Since this repository serves as a staging environment for your production **Helix** environment, this guide outlines exactly which files and configurations you need to copy over to successfully recreate your new architecture. Because Helix uses the exact same ADK primitives, your migration is essentially a 1:1 code transfer!

## 1. Agent Logic & Factories (The Core Brains)
You will migrate both your YAML configurations AND your Python agent definitions. Helix will run this exact same code, but it will seamlessly wrap it with its own observability, guardrails, and model API handlers.

- **The Entry Point**: [dart_ops/agent.py](./dart_ops/agent.py)
  - *This file exports your Orchestrator as `root_agent`. Since Helix wraps ADK, it will use this exact file as the main entry point to load your entire agent hierarchy!*
- **The Factory**: [dart_ops/agent_factory.py](./dart_ops/agent_factory.py)
  - *This file contains the `create_all_agents` logic that instantiates the ADK `Agent()` objects and wires them together with `AgentTool`s.*
- **The Config Reader**: [dart_ops/config_reader.py](./dart_ops/config_reader.py)
  - *A lightweight utility script that the factory uses to parse the YAML files. Needs to be migrated alongside the factory.*
- **The Configs**: `config/agents/*.yaml`
  - *The YAML files that `agent_factory.py` reads to dynamically inject the `instruction`, `model`, and `description`.*

## 2. Tools (Capabilities)
You will migrate the custom Python tools we built, as Helix's ADK environment natively supports `FunctionTool`.

- **Skill Reader Tool**: [dart_ops/skill_tool.py](./dart_ops/skill_tool.py)
  - *Contains `list_skills` and `read_skill`.*
- **Database Query Tool**: [dart_ops/duckdb_tool.py](./dart_ops/duckdb_tool.py)
  - *Contains `execute_duckdb_query`.*
- **Database Files**: `data/*.csv`
  - *IMPORTANT: You must migrate `data/issues.csv` and `data/risk_metrics.csv`. The DuckDB tool is hardcoded to query these local CSV files!*
- **Tool Registry**: [dart_ops/tool_registry.py](./dart_ops/tool_registry.py)
  - *The dictionary mapping that allows the factory to assign tools dynamically.*

## 3. Skills (Knowledge Base)
You should migrate any markdown files you placed in the `skills/` directory.

- Example: [skills/regulator_perspective.md](./skills/regulator_perspective.md)
  - *Ensure this directory is placed in a location where `skill_tool.py` can correctly resolve the path in your Helix environment.*

## 4. Evaluation Data (Testing)
Helix likely supports or runs the standard `agents-cli eval` suite, so you can directly migrate your test cases to verify the agents work correctly in production.

- **Evalset**: [tests/eval/evalsets/hierarchy_evalset.json](./tests/eval/evalsets/hierarchy_evalset.json)
- **Rubrics/Metrics**: [tests/eval/eval_config.json](./tests/eval/eval_config.json)
