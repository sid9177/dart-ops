# Config-Driven Agent Registry Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement the agent registry class (`AgentRegistry`) in `registry.py` to dynamically load YAML configs from `config/agents/` and `config/reviewers/`, initialize DuckDB tables for chapter agents, attach SQL schema/query tools to them, and expose all loaded agents as coordation tools.

**Architecture:** `AgentRegistry` acts as a factory and container. It parses configs, populates the shared `DuckDBHelper` instance, defines dynamically-named Python functions wrapping DuckDB query capability, instantiates the `Agent` objects with those tools, and generates coordinating wrapper functions for agent-to-agent calling.

**Tech Stack:** Python 3.11+, google-adk, PyYAML, DuckDB, pytest.

---

## File Structure & Dependencies

- Create: `registry.py` - Contains the `AgentRegistry` class implementing configuration loading, agent building, and tool generation.
- Create: `tests/test_registry.py` - Contains pytest unit tests verifying the registry logic.

---

## Tasks

### Task 1: Create Unit Tests for AgentRegistry

Verify configuration loading, agent initialization, DuckDB integration, tool assignment, and P2P wrapper generation using a mocked directory structure.

**Files:**
- Create: `tests/test_registry.py`

- [ ] **Step 1: Write failing unit tests for the registry**
  Create `tests/test_registry.py` with mock configs and assert registry behavior.
  ```python
  import os
  import yaml
  import pytest
  from unittest.mock import patch, MagicMock
  from registry import AgentRegistry

  def test_registry_initialization():
      registry = AgentRegistry(config_dir="dummy_config")
      assert registry.config_dir == "dummy_config"
      assert isinstance(registry.agents, dict)
      assert len(registry.agents) == 0

  def test_registry_load_and_register(tmp_path):
      # Create mock config files
      agents_dir = tmp_path / "agents"
      reviewers_dir = tmp_path / "reviewers"
      os.makedirs(agents_dir, exist_ok=True)
      os.makedirs(reviewers_dir, exist_ok=True)

      # 1. Chapter agent config (with DB and file)
      issues_config = {
          "name": "issues_agent",
          "model": "gemini-2.5-flash",
          "description": "Queries issues.",
          "instruction": "Find open issues.",
          "database_table": "issues",
          "file_path": "dummy_issues.csv"
      }
      with open(agents_dir / "issues.yaml", "w", encoding="utf-8") as f:
          yaml.safe_dump(issues_config, f)

      # Create dummy csv in the tmp path
      dummy_csv = tmp_path / "dummy_issues.csv"
      dummy_csv.write_text("id,severity\n1,High\n", encoding="utf-8")

      # 2. Reviewer agent config (no DB/file)
      reviewer_config = {
          "name": "second_lod_agent",
          "model": "gemini-2.5-pro",
          "description": "2nd LOD Officer.",
          "instruction": "Review draft.",
      }
      with open(reviewers_dir / "second_lod.yaml", "w", encoding="utf-8") as f:
          yaml.safe_dump(reviewer_config, f)

      # We will mock the base_dir check in registry.py to use tmp_path for resolving relative CSV paths
      with patch("os.path.dirname", return_value=str(tmp_path)):
          registry = AgentRegistry(config_dir=str(tmp_path))
          registry.load_configs()

      # Assert agents are instantiated correctly
      assert "issues_agent" in registry.agents
      assert "second_lod_agent" in registry.agents

      issues_agent = registry.agents["issues_agent"]
      second_lod_agent = registry.agents["second_lod_agent"]

      assert issues_agent.name == "issues_agent"
      assert issues_agent.model == "gemini-2.5-flash"
      assert issues_agent.description == "Queries issues."
      assert issues_agent.instruction == "Find open issues."
      
      # Verify chapter agent gets DuckDB tools
      assert len(issues_agent.tools) == 2
      tool_names = [t.__name__ for t in issues_agent.tools]
      assert "get_issues_schema" in tool_names
      assert "query_issues" in tool_names

      # Verify reviewer gets no tools
      assert len(second_lod_agent.tools) == 0

      # Verify DuckDB loader was called
      schema = registry.db.get_table_schema("issues")
      assert "id" in schema
      assert "severity" in schema

      # Verify get_all_tools generates wrapper callables
      tools = registry.get_all_tools()
      assert len(tools) == 2
      p2p_tool_names = [t.__name__ for t in tools]
      assert "call_issues_agent" in p2p_tool_names
      assert "call_second_lod_agent" in p2p_tool_names

      # Verify docs are set correctly
      issues_tool = next(t for t in tools if t.__name__ == "call_issues_agent")
      assert "Queries issues." in issues_tool.__doc__
  ```

- [ ] **Step 2: Run test to verify it fails**
  Run: `python -m pytest tests/test_registry.py -v`
  Expected: FAIL (ModuleNotFoundError: No module named 'registry')

---

### Task 2: Implement AgentRegistry in registry.py

Write the registry loader, DuckDB table creation, dynamic tool creation, agent instantiation, and wrapper generation.

**Files:**
- Create: `registry.py`

- [ ] **Step 1: Write minimal registry implementation**
  Create `registry.py` matching the code template provided.
  ```python
  import os
  import yaml
  from google.adk.agents.llm_agent import Agent
  from db_helper import DuckDBHelper

  class AgentRegistry:
      def __init__(self, config_dir: str = "config"):
          self.config_dir = config_dir
          self.agents = {}
          self.db = DuckDBHelper()

      def load_configs(self):
          # Load chapter agents
          agents_path = os.path.join(self.config_dir, "agents")
          if os.path.exists(agents_path):
              for f in os.listdir(agents_path):
                  if f.endswith(".yaml") or f.endswith(".yml"):
                      with open(os.path.join(agents_path, f), "r") as stream:
                          config = yaml.safe_load(stream)
                          self._register_agent(config, is_reviewer=False)
                          
          # Load reviewer agents
          reviewers_path = os.path.join(self.config_dir, "reviewers")
          if os.path.exists(reviewers_path):
              for f in os.listdir(reviewers_path):
                  if f.endswith(".yaml") or f.endswith(".yml"):
                      with open(os.path.join(reviewers_path, f), "r") as stream:
                          config = yaml.safe_load(stream)
                          self._register_agent(config, is_reviewer=True)

      def _register_agent(self, config: dict, is_reviewer: bool):
          name = config.get("name")
          model = config.get("model", "gemini-2.5-flash")
          instruction = config.get("instruction", "")
          description = config.get("description", "")
          
          file_path = config.get("file_path")
          table_name = config.get("database_table")
          
          agent_tools = []
          if not is_reviewer and file_path and table_name:
              # Resolve relative file path relative to project root (or module directory)
              base_dir = os.path.dirname(os.path.abspath(__file__))
              full_path = os.path.join(base_dir, file_path) if not os.path.isabs(file_path) else file_path
              
              if os.path.exists(full_path):
                  self.db.load_csv(table_name, full_path)
                  
                  # Define schema discovery and query tools
                  def get_schema(table=table_name):
                      return self.db.get_table_schema(table)
                  
                  def run_query(sql: str):
                      return self.db.run_sql_query(sql)
                      
                  get_schema.__name__ = f"get_{table_name}_schema"
                  get_schema.__doc__ = f"Get column names and schema for table '{table_name}'."
                  run_query.__name__ = f"query_{table_name}"
                  run_query.__doc__ = f"Run read-only SQL queries on table '{table_name}'."
                  
                  agent_tools = [get_schema, run_query]

          agent = Agent(
              name=name,
              model=model,
              instruction=instruction,
              description=description,
              tools=agent_tools
          )
          self.agents[name] = agent

      def get_all_tools(self) -> list:
          # Wrap each agent as an ADK tool
          tools = []
          for name, agent in self.agents.items():
              def make_agent_tool(a_name=name, a_agent=agent):
                  def call_agent(query: str) -> str:
                      return a_agent.run(query)
                  call_agent.__name__ = f"call_{a_name}"
                  call_agent.__doc__ = f"Query {a_name} agent to analyze: {a_agent.description}"
                  return call_agent
              tools.append(make_agent_tool())
          return tools
  ```

- [ ] **Step 2: Run pytest to verify all tests pass**
  Run: `python -m pytest tests/test_registry.py -v`
  Expected: PASS

---

### Task 3: Run Full Test Suite and Commit

Ensure no regressions exist in the workspace and commit our changes.

- [ ] **Step 3.1: Run all tests in the workspace**
  Run: `python -m pytest`
  Expected: PASS (all tests including test_registry.py pass)

- [ ] **Step 3.2: Commit Task 4 changes**
  Run: `git add registry.py tests/test_registry.py`
  Run: `git commit -m "feat: implement config-driven agent registry and dynamic tools"`
