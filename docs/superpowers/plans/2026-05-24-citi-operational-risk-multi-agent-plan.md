# Citi Operational Risk Multi-Agent System Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a config-driven, low-latency multi-agent Operational Risk reporting system using the Google ADK and DuckDB, featuring interactive peer-to-peer chapter querying, a Python sandbox, and custom Citigroup-styled PDF/PPTX report exports with 3 human-in-the-loop checkpoints.

**Architecture:** A coordinator agent manages a state machine with 3 HITL checkpoints. It orchestrates dynamic chapter agents (built from local YAML config files) which query a DuckDB database using schema discovery and run-sql tools. The drafted report is reviewed, challenged by LOD agents, and exported using themed templates.

**Tech Stack:** Python 3.11+, google-adk, DuckDB, python-pptx, reportlab, matplotlib, pytest.

---

## File Structure & Dependencies

We will create and modify the following files:
1.  **Modify**: [agent.py](file:///c:/Users/siddi/Projects/adk-workspace/dart-ops/agent.py) - Bootstraps the coordinator agent, state machine, and triggers the ADK interface.
2.  **Create**: [db_helper.py](file:///c:/Users/siddi/Projects/adk-workspace/dart-ops/db_helper.py) - Initializes DuckDB, runs schema discovery, and executes SQL queries.
3.  **Create**: [tools.py](file:///c:/Users/siddi/Projects/adk-workspace/dart-ops/tools.py) - Python sandbox execution and Citigroup-branded PDF/PPTX report export helper functions.
4.  **Create**: [registry.py](file:///c:/Users/siddi/Projects/adk-workspace/dart-ops/registry.py) - Loads configuration YAML files and instantiates Chapter and LOD agents.
5.  **Create**: `config/` and `data/` directories with mock files and configuration templates.
6.  **Create**: `tests/` directory with `pytest` unit tests for local validation.

---

## Tasks

### Task 1: Setup Workspace & Mock Data
Initialize the workspace directories, mock CSV data files, and configurations.

**Files:**
- Create: [data/issues.csv](file:///c:/Users/siddi/Projects/adk-workspace/dart-ops/data/issues.csv)
- Create: [data/risk_metrics.csv](file:///c:/Users/siddi/Projects/adk-workspace/dart-ops/data/risk_metrics.csv)
- Create: [config/agents/issues.yaml](file:///c:/Users/siddi/Projects/adk-workspace/dart-ops/config/agents/issues.yaml)
- Create: [config/agents/risk_metrics.yaml](file:///c:/Users/siddi/Projects/adk-workspace/dart-ops/config/agents/risk_metrics.yaml)
- Create: [config/reviewers/second_lod.yaml](file:///c:/Users/siddi/Projects/adk-workspace/dart-ops/config/reviewers/second_lod.yaml)

- [ ] **Step 1: Create mock CSV file for Issues**
  Write issues CSV data to `data/issues.csv`.
  ```csv
  issue_id,title,severity,status,open_date,due_date
  I001,Unauth Trading Limit Breach,High,Open,2026-01-15,2026-06-30
  I002,Phishing Control Failure,Medium,Open,2026-02-10,2026-05-15
  I003,Stale MCA Controls,Low,Closed,2025-10-01,2026-01-01
  ```

- [ ] **Step 2: Create mock CSV file for Risk Metrics**
  Write risk metrics CSV data to `data/risk_metrics.csv`.
  ```csv
  metric_id,metric_name,value,threshold,status,date
  M001,System Downtime Hours,4.5,5.0,Amber,2026-03-31
  M002,Failed Key Controls,12.0,10.0,Red,2026-03-31
  M003,Key Person Risk Score,2.0,4.0,Green,2026-03-31
  ```

- [ ] **Step 3: Create YAML configuration for Issues Chapter Agent**
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

- [ ] **Step 4: Create YAML configuration for Risk Metrics Chapter Agent**
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

- [ ] **Step 5: Create YAML configuration for 2nd LOD Reviewer Agent**
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

- [ ] **Step 6: Commit Task 1**
  ```bash
  git add data/ config/
  git commit -m "chore: set up mock data and agent configuration files"
  ```

---

### Task 2: Implement DuckDB Database Helper
Create the database layer using DuckDB to support SQL queries and schema discovery.

**Files:**
- Create: [db_helper.py](file:///c:/Users/siddi/Projects/adk-workspace/dart-ops/db_helper.py)
- Create: [tests/test_db_helper.py](file:///c:/Users/siddi/Projects/adk-workspace/dart-ops/tests/test_db_helper.py)

- [ ] **Step 1: Write a unit test for the DuckDB helper**
  Write the test file `tests/test_db_helper.py` to verify connection and schema discovery.
  ```python
  import os
  import pytest
  from db_helper import DuckDBHelper

  def test_duckdb_helper_flow():
      # Create a temporary CSV file
      temp_csv = "tests/temp_test.csv"
      os.makedirs("tests", exist_ok=True)
      with open(temp_csv, "w") as f:
          f.write("col_a,col_b\n1,hello\n2,world\n")

      helper = DuckDBHelper()
      helper.load_csv("test_table", temp_csv)

      # Test schema discovery
      schema = helper.get_table_schema("test_table")
      assert "col_a" in schema
      assert "col_b" in schema

      # Test query execution
      res = helper.run_sql_query("SELECT * FROM test_table WHERE col_a = 1")
      assert "hello" in res

      # Clean up
      if os.path.exists(temp_csv):
          os.remove(temp_csv)
  ```

- [ ] **Step 2: Run test to verify it fails**
  Run: `uv run pytest tests/test_db_helper.py -v`
  Expected: FAIL (ModuleNotFoundError: No module named 'db_helper')

- [ ] **Step 3: Implement `db_helper.py`**
  Write the database manager to `db_helper.py`.
  ```python
  import duckdb
  import pandas as pd

  class DuckDBHelper:
      def __init__(self):
          self.conn = duckdb.connect(database=":memory:")

      def load_csv(self, table_name: str, file_path: str):
          # Supports both CSV and Excel loader via pandas
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
              # Return detailed error to help agent self-correct
              return f"SQL Error: {str(e)}"
  ```

- [ ] **Step 4: Run test to verify it passes**
  Run: `uv run pytest tests/test_db_helper.py -v`
  Expected: PASS

- [ ] **Step 5: Commit Task 2**
  ```bash
  git add db_helper.py tests/test_db_helper.py
  git commit -m "feat: implement DuckDB helper and schema discovery tools"
  ```

---

### Task 3: Implement Python Sandbox & Report Exporters
Implement code execution and Citigroup corporate-branded document exports.

**Files:**
- Create: [tools.py](file:///c:/Users/siddi/Projects/adk-workspace/dart-ops/tools.py)
- Create: [tests/test_tools.py](file:///c:/Users/siddi/Projects/adk-workspace/dart-ops/tests/test_tools.py)

- [ ] **Step 1: Write a unit test for sandbox and report export tools**
  Write tests in `tests/test_tools.py`.
  ```python
  import os
  from tools import execute_python_code, export_report_to_pdf, export_report_to_pptx

  def test_python_sandbox():
      code = "a = 5\nb = 10\nprint(f'sum={a+b}')"
      out = execute_python_code(code)
      assert "sum=15" in out

  def test_report_export():
      md_report = """# Operational Risk Report\n\n## KRI Status\n* KRI Downtime is Red\n\n## Open Issues\n* Limit Breach open since Jan."""
      pdf_path = "reports/test_report.pdf"
      pptx_path = "reports/test_report.pptx"
      
      os.makedirs("reports", exist_ok=True)
      export_report_to_pdf(md_report, pdf_path)
      export_report_to_pptx(md_report, pptx_path)
      
      assert os.path.exists(pdf_path)
      assert os.path.exists(pptx_path)
      
      # Clean up
      os.remove(pdf_path)
      os.remove(pptx_path)
  ```

- [ ] **Step 2: Run test to verify it fails**
  Run: `uv run pytest tests/test_tools.py -v`
  Expected: FAIL (ModuleNotFoundError: No module named 'tools')

- [ ] **Step 3: Implement `tools.py`**
  Write the Python sandbox and Citigroup presentation builders in `tools.py`. We'll use basic standard libraries and conditional importing for external dependencies (`reportlab`, `python-pptx`, `matplotlib`) to avoid runtime crashes.
  ```python
  import sys
  import io
  import os
  import traceback

  # Sandbox python executor
  def execute_python_code(code: str) -> str:
      # Redirect output
      old_stdout = sys.stdout
      sys.stdout = buffer = io.StringIO()
      
      # Global context for execution
      exec_globals = {}
      try:
          exec(code, exec_globals)
          sys.stdout = old_stdout
          return buffer.getvalue()
      except Exception as e:
          sys.stdout = old_stdout
          return f"Execution Error:\n{traceback.format_exc()}"

  # PDF Exporter matching Citi Visual Elements
  def export_report_to_pdf(markdown_content: str, output_path: str):
      try:
          from reportlab.lib.pagesizes import letter
          from reportlab.lib import colors
          from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
          from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
      except ImportError:
          # Simple fallback if ReportLab not installed
          with open(output_path, "w") as f:
              f.write(f"PDF FALLBACK - MOCK GENERATED\n\n{markdown_content}")
          return

      doc = SimpleDocTemplate(output_path, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
      styles = getSampleStyleSheet()
      
      # Custom Citigroup Styles
      # Citi Blue (#003B70), Citi Red Accent (#EE3124), Charcoal Text (#222222)
      citi_blue = colors.HexColor("#003B70")
      citi_red = colors.HexColor("#EE3124")
      charcoal = colors.HexColor("#222222")

      title_style = ParagraphStyle(
          'CitiTitle',
          parent=styles['Heading1'],
          fontName='Helvetica-Bold',
          fontSize=22,
          textColor=citi_blue,
          spaceAfter=15
      )
      
      body_style = ParagraphStyle(
          'CitiBody',
          parent=styles['Normal'],
          fontName='Helvetica',
          fontSize=10.5,
          textColor=charcoal,
          spaceAfter=8,
          leading=14
      )

      story = []
      
      # Visual Red Arc accent bar (as table)
      header_bar = Table([[""]], colWidths=[540])
      header_bar.setStyle(TableStyle([
          ('BACKGROUND', (0,0), (-1,-1), citi_red),
          ('BOTTOMPADDING', (0,0), (-1,-1), 4),
          ('TOPPADDING', (0,0), (-1,-1), 0),
      ]))
      story.append(header_bar)
      story.append(Spacer(1, 15))

      lines = markdown_content.split("\n")
      for line in lines:
          line = line.strip()
          if not line:
              continue
          if line.startswith("# "):
              story.append(Paragraph(line[2:], title_style))
          elif line.startswith("## "):
              h2_style = ParagraphStyle('CitiH2', parent=title_style, fontSize=16, spaceBefore=10)
              story.append(Paragraph(line[3:], h2_style))
          elif line.startswith("### "):
              h3_style = ParagraphStyle('CitiH3', parent=title_style, fontSize=12, spaceBefore=8)
              story.append(Paragraph(line[4:], h3_style))
          elif line.startswith("* ") or line.startswith("- "):
              story.append(Paragraph(f"• {line[2:]}", body_style))
          else:
              story.append(Paragraph(line, body_style))

      # Add confidentiality footer
      confidential_style = ParagraphStyle('CitiConf', parent=body_style, fontSize=8, textColor=colors.gray, alignment=1)
      story.append(Spacer(1, 25))
      story.append(Paragraph("CITI INTERNAL USE ONLY - STRICTLY CONFIDENTIAL", confidential_style))
      
      doc.build(story)

  # PPTX Exporter matching Citi Widescreen (16:9) Layout
  def export_report_to_pptx(markdown_content: str, output_path: str):
      try:
          from pptx import Presentation
          from pptx.util import Inches, Pt
          from pptx.dml.color import RGBColor
      except ImportError:
          # Simple fallback if python-pptx not installed
          with open(output_path, "w") as f:
              f.write(f"PPTX FALLBACK - MOCK GENERATED\n\n{markdown_content}")
          return

      prs = Presentation()
      # Set 16:9 ratio
      prs.slide_width = Inches(13.333)
      prs.slide_height = Inches(7.5)
      
      # Citi Branding colors
      citi_blue_rgb = RGBColor(0, 59, 112)
      citi_red_rgb = RGBColor(238, 49, 36)
      charcoal_rgb = RGBColor(34, 34, 34)

      # Create title slide
      slide_layout = prs.slide_layouts[5] # title only
      slide = prs.slides.add_slide(slide_layout)
      
      # Draw blue header card
      shapes = slide.shapes
      header_box = shapes.add_textbox(Inches(0.5), Inches(0.5), Inches(12.333), Inches(1.5))
      tf = header_box.text_frame
      tf.word_wrap = True
      p = tf.paragraphs[0]
      p.text = "Citi Operational Risk Analytics Report"
      p.font.size = Pt(36)
      p.font.bold = True
      p.font.color.rgb = citi_blue_rgb

      # Add accent line
      line = shapes.add_shape(1, Inches(0.5), Inches(2.0), Inches(12.333), Inches(0.08)) # rectangle shape
      line.fill.solid()
      line.fill.fore_color.rgb = citi_red_rgb

      # Add bullet slide for contents
      slide = prs.slides.add_slide(prs.slide_layouts[1]) # Bullet layout
      shapes = slide.shapes
      title_shape = shapes.title
      title_shape.text = "Executive Summary & Findings"
      title_shape.text_frame.paragraphs[0].font.color.rgb = citi_blue_rgb
      
      body_shape = shapes.placeholders[1]
      tf = body_shape.text_frame
      tf.word_wrap = True
      
      lines = markdown_content.split("\n")
      for line in lines:
          line = line.strip()
          if line.startswith("* ") or line.startswith("- "):
              p = tf.add_paragraph()
              p.text = line[2:]
              p.level = 0
              p.font.color.rgb = charcoal_rgb

      prs.save(output_path)
  ```

- [ ] **Step 4: Run test to verify it passes**
  Run: `uv run pytest tests/test_tools.py -v`
  Expected: PASS

- [ ] **Step 5: Commit Task 3**
  ```bash
  git add tools.py tests/test_tools.py
  git commit -m "feat: implement execution sandbox and Citigroup styled exporters"
  ```

---

### Task 4: Implement Config-Driven Registry
Implement the agent registry to load configuration YAML files, construct ADK agents dynamically, and expose them as tools to one another.

**Files:**
- Create: [registry.py](file:///c:/Users/siddi/Projects/adk-workspace/dart-ops/registry.py)
- Create: [tests/test_registry.py](file:///c:/Users/siddi/Projects/adk-workspace/dart-ops/tests/test_registry.py)

- [ ] **Step 1: Write a unit test for the registry**
  Write tests in `tests/test_registry.py` to verify dynamic loading.
  ```python
  import pytest
  from registry import AgentRegistry

  def test_registry_load():
      registry = AgentRegistry(config_dir="config")
      registry.load_configs()
      
      # Verify chapter agents loaded
      assert "issues_agent" in registry.agents or "issues" in registry.agents
      # Verify tools generated
      tools = registry.get_all_tools()
      assert len(tools) > 0
  ```

- [ ] **Step 2: Run test to verify it fails**
  Run: `uv run pytest tests/test_registry.py -v`
  Expected: FAIL (ModuleNotFoundError: No module named 'registry')

- [ ] **Step 3: Implement `registry.py`**
  Write the YAML config parser and ADK builder to `registry.py`.
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
          
          # Initialize data source if defined in config
          file_path = config.get("file_path")
          table_name = config.get("database_table")
          if file_path and table_name:
              self.db.load_csv(table_name, file_path)

          # Define the dynamic database tools for chapters
          agent_tools = []
          if not is_reviewer:
              # Wrap methods as standard functions for ADK compatibility
              def get_schema(table=table_name):
                  return self.db.get_table_schema(table)
              def run_query(sql: str):
                  return self.db.run_sql_query(sql)
                  
              get_schema.__name__ = f"get_{table_name}_schema"
              run_query.__name__ = f"query_{table_name}"
              
              agent_tools = [get_schema, run_query]

          # Create ADK Agent
          agent = Agent(
              name=name,
              model=model,
              instruction=instruction,
              description=description,
              tools=agent_tools
          )
          
          self.agents[name] = agent

      def get_all_tools(self) -> list:
          # Converts chapter agents into P2P tools for the Coordinator
          tools = []
          for name, agent in self.agents.items():
              def make_agent_tool(a_name=name, a_agent=agent):
                  def call_agent(query: str) -> str:
                      return a_agent.run(query)
                  call_agent.__name__ = f"call_{a_name}"
                  call_agent.__doc__ = f"Ask the {a_name} agent to analyze: {a_agent.description}"
                  return call_agent
              tools.append(make_agent_tool())
          return tools
  ```

- [ ] **Step 4: Run test to verify it passes**
  Run: `uv run pytest tests/test_registry.py -v`
  Expected: PASS

- [ ] **Step 5: Commit Task 4**
  ```bash
  git add registry.py tests/test_registry.py
  git commit -m "feat: implement config-driven agent loader and P2P tool wrapper"
  ```

---

### Task 5: Boot Coordinator & Implement HITL State Machine
Connect the dynamic registry, custom tool wrappers, and Coordinator logic into the primary entrypoint with interactive user-gating.

**Files:**
- Modify: [agent.py](file:///c:/Users/siddi/Projects/adk-workspace/dart-ops/agent.py)

- [ ] **Step 1: Replace `agent.py`**
  Modify [agent.py](file:///c:/Users/siddi/Projects/adk-workspace/dart-ops/agent.py) to parse config-driven agents and implement the three HITL checkpoints via the CLI/Playground.
  ```python
  from google.adk.agents.llm_agent import Agent
  from registry import AgentRegistry
  from tools import execute_python_code, export_report_to_pdf, export_report_to_pptx
  import os

  # Load configurations dynamically
  registry = AgentRegistry(config_dir="config")
  registry.load_configs()

  # Create a wrapper for custom tools
  python_sandbox = execute_python_code

  # Gather P2P tools (chapter agents as tools)
  p2p_tools = registry.get_all_tools()
  # Add Python execution sandbox
  p2p_tools.append(python_sandbox)

  # State storage for draft/reviews
  report_state = {
      "draft": "",
      "final": "",
      "challenges": []
  }

  # Root Coordinator Agent
  root_agent = Agent(
      model='gemini-2.5-flash',
      name='coordinator_agent',
      description='Citi Operational Risk Multi-Agent Reporting Director.',
      instruction="""
      You are the Citi Operational Risk Reporting Director (Coordinator).
      You coordinate the reporting process. 
      Steps:
      1. Delegate analytical queries to Chapter agents (call_issues_agent, call_risk_metrics_agent) and the Python sandbox.
      2. Synthesize findings into a draft report.
      3. Trigger Gate 1 by explicitly outputting: '[GATE 1: DRAFT_READY] <your drafted report content>' and wait.
      4. Once approved, present to LOD Reviewers (e.g. call_second_lod_agent).
      5. If an LOD Reviewer outputs '[CHALLENGE]: <question>', halt and print: '[GATE 2: LOD_CHALLENGE] <challenge text>' and wait.
      6. Once all challenges are resolved, output: '[GATE 3: FINAL_REPORT] <your final report>' and wait for sign-off.
      """,
      tools=p2p_tools
  )
  ```

- [ ] **Step 2: Commit Task 5**
  ```bash
  git add agent.py
  git commit -m "feat: orchestrate agent coordination and integrate custom tools in main script"
  ```

---

### Task 6: End-to-End Local Playground Verification
Manually verify DuckDB querying, P2P calling, and the three HITL gates using the ADK Playground.

- [ ] **Step 1: Start ADK local playground**
  Run: `agents-cli playground`
  Expected: Command launches a local web-based user interface.

- [ ] **Step 2: Query the agents**
  Submit a query: `Verify Q1 status of high severity issues and failed metrics.`
  Verify: Chapter agents load and execute SQL commands on DuckDB.

- [ ] **Step 3: Test Gate 1 (Draft Review)**
  Verify: Coordinator agent prints a draft report and triggers the draft pause. Approve it in the UI.

- [ ] **Step 4: Test Gate 2 (LOD Challenge)**
  Verify: The 2nd LOD agent challenges the breach of `Failed Key Controls` as there are no corresponding issues. Response provided by the user is routed back.

- [ ] **Step 5: Test Gate 3 (Final Sign-off)**
  Confirm the generation and formatting of the PDF and PPTX files in the `reports/` directory.

- [ ] **Step 6: Verify exported reports**
  Verify `reports/` contains correctly generated PDF and PPTX matching Citigroup colors and layouts.
