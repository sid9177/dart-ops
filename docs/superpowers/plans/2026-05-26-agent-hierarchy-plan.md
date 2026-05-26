# Agent Hierarchy Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement the hierarchical delegation agent architecture by introducing Analyst and Reporter agents and updating existing configurations.

**Architecture:** The Orchestrator routes requests to Chapter SMEs. SMEs delegate data extraction to the Analyst and formatting to the Reporter.

**Tech Stack:** Python, Google ADK 1.31, YAML

---

### Task 1: Create Analyst and Reporter Configurations

**Files:**
- Create: `config/agents/analyst.yaml`
- Create: `config/agents/reporter.yaml`

- [ ] **Step 1: Create the Analyst agent config**

```yaml
# In config/agents/analyst.yaml
name: "analyst"
model: "gemini-2.5-flash"
description: "Executes database queries to extract requested data."
instruction: |
  You are a generic Data Analyst agent.
  You receive data extraction requests from Chapter SMEs.
  Use the execute_duckdb_query tool to run SQL queries against the specified database tables and return the raw JSON data.
tools:
  - execute_duckdb_query
```

- [ ] **Step 2: Create the Reporter agent config**

```yaml
# In config/agents/reporter.yaml
name: "reporter"
model: "gemini-2.5-flash"
description: "Synthesizes raw data into professional markdown reports."
instruction: |
  You are a generic Reporting agent.
  You receive raw data and formatting instructions from Chapter SMEs.
  Format the provided data into a professional markdown report. Do not invent data.
tools: []
```

- [ ] **Step 3: Commit**

```bash
git add config/agents/analyst.yaml config/agents/reporter.yaml
git commit -m "feat: add analyst and reporter agent configs"
```

### Task 2: Update Agent Factory for Generic Docstrings

**Files:**
- Modify: `tests/unit/test_agent_factory.py`
- Modify: `dart_ops/agent_factory.py`

- [ ] **Step 1: Update the agent factory test**

```python
# Replace tests/unit/test_agent_factory.py with:
from dart_ops.agent_factory import create_all_agents

def test_create_all_agents():
    agents = create_all_agents()
    assert "orchestrator" in agents
    assert "issues_chapter" in agents
    assert "risk_metrics_chapter" in agents
    assert "analyst" in agents
    assert "reporter" in agents
    
    from dart_ops.tool_registry import REGISTRY
    assert "ask_analyst" in REGISTRY
    assert "ask_reporter" in REGISTRY
    
    # Check that docstrings use the description from yaml
    assert "Synthesizes raw data" in REGISTRY["ask_reporter"].__doc__
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/unit/test_agent_factory.py -v`
Expected: FAIL (because docstring still uses the hardcoded 'chapter' template)

- [ ] **Step 3: Modify agent_factory.py**

```python
# In dart_ops/agent_factory.py, replace lines 37-38:
#             chapter_caller.__name__ = f"ask_{safe_name}"
#             chapter_caller.__doc__ = f"Use this tool to ask questions and get data from the {config.get('name')} chapter."
#
# With:
            chapter_caller.__name__ = f"ask_{safe_name}"
            chapter_caller.__doc__ = config.get("description", f"Use this tool to ask questions and get data from the {config.get('name')} chapter.")
```

- [ ] **Step 4: Run test to verify it passes**

Run: `uv run pytest tests/unit/test_agent_factory.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add tests/unit/test_agent_factory.py dart_ops/agent_factory.py
git commit -m "feat: use yaml description for dynamically generated tool docstrings"
```

### Task 3: Update Chapter SMEs and Orchestrator Configs

**Files:**
- Modify: `config/agents/issues.yaml`
- Modify: `config/agents/risk_metrics.yaml`
- Modify: `config/agents/orchestrator.yaml`

- [ ] **Step 1: Update issues.yaml**

```yaml
# Replace content of config/agents/issues.yaml with:
name: "issues_chapter"
model: "gemini-2.5-flash"
description: "Domain expert for Operational Risk Issues and Action Plans."
instruction: |
  You are the Issues Chapter Agent for Operational Risk.
  When queried about issues, you MUST delegate data extraction to the Analyst using the ask_analyst tool.
  Tell the Analyst to query the 'issues' table at 'data/issues.csv' for high severity open issues.
  Once you receive the data from the Analyst, delegate the report generation to the Reporter using the ask_reporter tool.
  Return the formatted report to the Orchestrator.
tools:
  - ask_analyst
  - ask_reporter
```

- [ ] **Step 2: Update risk_metrics.yaml**

```yaml
# Replace content of config/agents/risk_metrics.yaml with:
name: "risk_metrics_chapter"
model: "gemini-2.5-flash"
description: "Domain expert for Key Risk Indicators (KRIs)."
instruction: |
  You are the Risk Metrics Chapter Agent. 
  When queried about risk metrics, delegate data extraction to the Analyst using the ask_analyst tool.
  Tell the Analyst to query the 'risk_metrics' table at 'data/risk_metrics.csv' for Amber or Red metrics.
  If the data is ambiguous, explicitly state what information is missing.
  Once you receive the data, use the ask_reporter tool to format the final response.
tools:
  - ask_analyst
  - ask_reporter
```

- [ ] **Step 3: Update orchestrator.yaml**

```yaml
# Replace content of config/agents/orchestrator.yaml with:
name: "orchestrator"
model: "gemini-2.5-flash"
description: "Central router for user requests."
instruction: |
  You are the Central Orchestrator for Operational Risk.
  You receive questions from users. You do NOT perform analysis or write reports.
  You MUST route the user's question to the appropriate Chapter SME tool (ask_issues_chapter or ask_risk_metrics_chapter).
  CRITICAL: You must present the final draft report from the Chapter SME to the user and ask for approval BEFORE concluding.
tools:
  - ask_issues_chapter
  - ask_risk_metrics_chapter
```

- [ ] **Step 4: Run tests to ensure configs load correctly**

Run: `uv run pytest tests/unit/test_agent_factory.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add config/agents/issues.yaml config/agents/risk_metrics.yaml config/agents/orchestrator.yaml
git commit -m "refactor: update configs for hierarchical delegation"
```
