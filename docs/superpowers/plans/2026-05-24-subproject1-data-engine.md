# Sub-Project 1: Core Data Engine & Chapter Agents Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the foundational DuckDB in-memory database engine and the config-driven registry that dynamically instantiates chapter agents with scoped SQL tools.

**Architecture:** Clean slate rewrite of `db_helper.py`, `registry.py`, and `agent.py`. The system starts by scanning `data/` to load CSVs into DuckDB, then scans `config/agents/` to create agents with `query_database` and `get_schema` tools.

**Tech Stack:** Python, Google ADK, DuckDB, pandas.

---

### Task 1: Setup Workspace & Mock Data

**Files:**
- Create: `data/issues.csv`
- Create: `data/risk_metrics.csv`
- Create: `config/agents/issues.yaml`
- Create: `config/agents/risk_metrics.yaml`
- Create: `config/reviewers/second_lod.yaml`

- [x] **Step 1: Create mock CSV file for Issues**
Write issues CSV data to `data/issues.csv`.
```csv
issue_id,title,severity,status,open_date,due_date
I001,Unauth Trading Limit Breach,High,Open,2026-01-15,2026-06-30
I002,Phishing Control Failure,Medium,Open,2026-02-10,2026-05-15
I003,Stale MCA Controls,Low,Closed,2025-10-01,2026-01-01
```

- [x] **Step 2: Create mock CSV file for Risk Metrics**
Write risk metrics CSV data to `data/risk_metrics.csv`.
```csv
metric_id,metric_name,value,threshold,status,date
M001,System Downtime Hours,4.5,5.0,Amber,2026-03-31
M002,Failed Key Controls,12.0,10.0,Red,2026-03-31
M003,Key Person Risk Score,2.0,4.0,Green,2026-03-31
```

- [x] **Step 3: Create YAML configuration for Issues Chapter Agent**
Write the YAML to `config/agents/issues.yaml`.
```yaml
name: "issues_agent"
model: "gemini-2.5-flash"
description: "Queries and analyzes Operational Risk Issues and Action Plans."
instruction: |
  You are the Issues Chapter Agent for Operational Risk.
  Query the 'issues' table in DuckDB to identify high severity open issues.
  Suggest remediation based on open dates.
database_table: "issues"
file_path: "data/issues.csv"
```

- [x] **Step 4: Create YAML configuration for Risk Metrics Chapter Agent**
Write the YAML to `config/agents/risk_metrics.yaml`.
```yaml
name: "risk_metrics_agent"
model: "gemini-2.5-flash"
description: "Monitors and analyzes Key Risk Indicators (KRIs)."
instruction: |
  You are the Risk Metrics Chapter Agent for Operational Risk.
  Query the 'risk_metrics' table in DuckDB to identify Amber or Red metrics.
database_table: "risk_metrics"
file_path: "data/risk_metrics.csv"
```

- [x] **Step 5: Create YAML configuration for 2nd LOD Reviewer Agent**
Write the YAML to `config/reviewers/second_lod.yaml`.
```yaml
name: "second_lod_agent"
model: "gemini-2.5-pro"
description: "Second Line of Defense Risk Officer."
instruction: |
  You are the Second Line of Defense (2nd LOD) Risk Officer.
  Review the draft report. Challenge any metrics breach that does not have an open issue.
  To challenge, output a clear question starting with '[CHALLENGE]: <question>'.
```

- [x] **Step 6: Commit Task 1**
```bash
git add data/ config/
git commit -m "chore: set up mock data and agent configuration files"
```

---

### Task 2: Implement DuckDB Database Helper

**Files:**
- Create: `db_helper.py`
- Create: `tests/test_db_helper.py`

- [x] **Step 1: Write a unit test for the DuckDB helper**
Write the test file `tests/test_db_helper.py` to verify connection and schema discovery.
Ensure file paths in tests are resolved dynamically using `pathlib.Path` relative to `__file__` to avoid relative execution issues.
```python
import os
from pathlib import Path
import pytest
from db_helper import DuckDBHelper

def test_duckdb_helper_flow():
    base_dir = Path(__file__).parent
    temp_csv = base_dir / "temp_test.csv"
    
    with open(temp_csv, "w") as f:
        f.write("col_a,col_b\n1,hello\n2,world\n")

    try:
        helper = DuckDBHelper()
        helper.load_csv("test_table", str(temp_csv))

        # Test schema discovery
        schema = helper.get_table_schema("test_table")
        assert "col_a" in schema
        assert "col_b" in schema

        # Test query execution
        res = helper.run_sql_query("SELECT * FROM test_table WHERE col_a = 1")
        assert "hello" in res
    finally:
        # Clean up
        if temp_csv.exists():
            os.remove(temp_csv)
```

- [ ] **Step 2: Run test to verify it fails**
Run: `uv run pytest tests/test_db_helper.py -v`
Expected: FAIL (ModuleNotFoundError: No module named 'db_helper')

- [x] **Step 3: Implement `db_helper.py`**
Write the database manager to `db_helper.py`.
It must support loading CSV and Excel (via pandas) files, fetching schema via DESCRIBE queries, and running SQL queries with try-except blocks to catch SQL exceptions and return clear error messages.
```python
import duckdb
import pandas as pd

class DuckDBHelper:
    def __init__(self):
        self.conn = duckdb.connect(database=":memory:")

    def load_csv(self, table_name: str, file_path: str):
        if file_path.endswith((".xlsx", ".xls")):
            df = pd.read_excel(file_path)
            self.conn.register(table_name, df)
        else:
            self.conn.execute(f"CREATE TABLE {table_name} AS SELECT * FROM read_csv_auto('{file_path}')")

    def get_table_schema(self, table_name: str) -> str:
        try:
            res = self.conn.execute(f"DESCRIBE {table_name}").fetchall()
            schema_lines = [f"{row[0]} ({row[1]})" for row in res]
            return f"Table '{table_name}' columns:\n" + "\n".join(schema_lines)
        except Exception as e:
            return f"Error fetching schema: {str(e)}"

    def run_sql_query(self, sql_query: str) -> str:
        try:
            df = self.conn.execute(sql_query).df()
            return df.to_string(index=False)
        except Exception as e:
            return f"SQL Error: {str(e)}"
```

- [ ] **Step 4: Run test to verify it passes**
Run: `uv run pytest tests/test_db_helper.py -v`
Expected: PASS

- [x] **Step 5: Commit Task 2**
```bash
git add db_helper.py tests/test_db_helper.py
git commit -m "feat: implement DuckDB helper and schema discovery tools"
```

---

### Task 3: Implement Agent Registry

**Files:**
- Create: `registry.py`
- Create: `tests/test_registry.py`

- [ ] **Step 1: Write failing test for Agent Registry**
Write test `tests/test_registry.py` using `pytest`.
```python
from registry import AgentRegistry
from db_helper import DuckDBHelper

def test_registry_initialization():
    db = DuckDBHelper()
    registry = AgentRegistry(db)
    assert len(registry.agents) == 0

def test_registry_load_and_register():
    db = DuckDBHelper()
    registry = AgentRegistry(db)
    # The registry should be able to load agents from config/agents directory
    registry.load_chapter_agents("config/agents")
    # Should at least find issues and risk_metrics
    assert "issues_agent" in registry.agents
    assert "risk_metrics_agent" in registry.agents
```

- [ ] **Step 2: Run test to verify it fails**
Run: `uv run pytest tests/test_registry.py -v`
Expected: FAIL (ModuleNotFoundError: No module named 'registry')

- [ ] **Step 3: Implement `registry.py`**
Write `registry.py`. It needs to read YAML files, load data into DuckDB, and instantiate ADK Agents with custom tools per table.
```python
import os
import yaml
from google.adk.agents import Agent
from google.adk.tools import Tool
from db_helper import DuckDBHelper

class AgentRegistry:
    def __init__(self, db_helper: DuckDBHelper):
        self.db_helper = db_helper
        self.agents: dict[str, Agent] = {}

    def load_chapter_agents(self, config_dir: str):
        if not os.path.exists(config_dir):
            return

        for filename in os.listdir(config_dir):
            if filename.endswith(".yaml") or filename.endswith(".yml"):
                filepath = os.path.join(config_dir, filename)
                with open(filepath, "r") as f:
                    config = yaml.safe_load(f)

                # 1. Load data into DuckDB if specified
                table_name = config.get("database_table")
                file_path = config.get("file_path")
                if table_name and file_path and os.path.exists(file_path):
                    try:
                        self.db_helper.load_csv(table_name, file_path)
                    except Exception as e:
                        print(f"Warning: Failed to load data for {config['name']}: {e}")

                # 2. Create tools bounded to this table
                tools = []
                if table_name:
                    def get_schema() -> str:
                        """Get the schema of the assigned database table."""
                        return self.db_helper.get_table_schema(table_name)
                    
                    def run_sql(sql_query: str) -> str:
                        """Run a SQL query against the database."""
                        return self.db_helper.run_sql_query(sql_query)

                    tools = [
                        Tool(get_schema, name=f"get_{table_name}_schema"),
                        Tool(run_sql, name=f"query_{table_name}_table")
                    ]

                # 3. Instantiate ADK Agent
                agent = Agent(
                    name=config["name"],
                    model=config.get("model", "gemini-2.5-flash"),
                    instructions=config.get("instruction", ""),
                    tools=tools
                )
                self.agents[config["name"]] = agent
```

- [ ] **Step 4: Run test to verify it passes**
Run: `uv run pytest tests/test_registry.py -v`
Expected: PASS

- [ ] **Step 5: Commit Task 3**
```bash
git add registry.py tests/test_registry.py
git commit -m "feat: implement config-driven agent registry and dynamic tools"
```

---

### Task 4: Implement Basic Coordinator

**Files:**
- Create: `agent.py`
- Modify: `tests/test_agent.py`

- [ ] **Step 1: Write failing test for Coordinator**
Write test `tests/test_agent.py` to verify the coordinator delegates to chapter agents.
```python
import pytest
from google.adk.testing import AgentRunner
from agent import OperationalRiskCoordinator

def test_coordinator_loads_registry():
    coordinator = OperationalRiskCoordinator()
    assert coordinator.db is not None
    assert coordinator.registry is not None
    assert "issues_agent" in coordinator.registry.agents
```

- [ ] **Step 2: Run test to verify it fails**
Run: `uv run pytest tests/test_agent.py -v`
Expected: FAIL

- [ ] **Step 3: Implement basic `agent.py`**
Implement `OperationalRiskCoordinator` as an ADK `BaseAgent`. For now, it just initializes the registry. We will build the full HITL state machine in the next subproject.
```python
from google.adk.agents import BaseAgent
from registry import AgentRegistry
from db_helper import DuckDBHelper

class OperationalRiskCoordinator(BaseAgent):
    """The root agent orchestrating Operational Risk chapters."""
    
    def __init__(self, name: str = "operational_risk_coordinator", **kwargs):
        super().__init__(name=name, **kwargs)
        self.db = DuckDBHelper()
        self.registry = AgentRegistry(self.db)
        
        # Load agents from config
        self.registry.load_chapter_agents("config/agents")

    def run(self, user_input: str) -> str:
        # For now, just route to a specific chapter if requested
        if "issue" in user_input.lower():
            issues_agent = self.registry.agents.get("issues_agent")
            if issues_agent:
                response = issues_agent(user_input)
                return response.text
        
        return "I am the Operational Risk Coordinator. Which chapter do you want to query?"

# This exposes the root agent for `agents-cli playground`
agent = OperationalRiskCoordinator()
```

- [ ] **Step 4: Run test to verify it passes**
Run: `uv run pytest tests/test_agent.py -v`
Expected: PASS

- [ ] **Step 5: Commit Task 4**
```bash
git add agent.py tests/test_agent.py
git commit -m "feat: implement root coordinator with registry initialization"
```
