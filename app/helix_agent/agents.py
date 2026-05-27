from google.adk.agents import Agent
from google.adk.tools import AgentTool
from app.helix_agent.tools import (
    execute_duckdb_query, 
    generate_pdf_report, 
    generate_ppt_report, 
    list_skills, 
    read_skill
)

# 1. Analyst Agent
analyst = Agent(
    name="analyst",
    model="gemini-2.5-flash",
    description="Executes database queries to extract requested data.",
    instruction="You are a generic Data Analyst agent.\nYou receive data extraction requests from Chapter SMEs.\nUse the execute_duckdb_query tool to run SQL queries against the specified database tables and return the raw JSON data.\n",
    tools=[execute_duckdb_query]
)
analyst_tool = AgentTool(analyst)

# 2. Reporter Agent
reporter = Agent(
    name="reporter",
    model="gemini-2.5-flash",
    description="Generates final compliance reports in PDF and PPTX formats",
    instruction="You are the Final Reporting Agent. Your job is to take the final assessments from other agents and format them into Citi-branded PDF or PPTX reports. \nWhen a user asks for a report, use the available tools to generate it and provide them with the path to the generated file.\nThe available designs are: \"executive_summary\".\n",
    tools=[generate_pdf_report, generate_ppt_report]
)
reporter_tool = AgentTool(reporter)

# 3. Issues Chapter Agent
issues_chapter = Agent(
    name="issues_chapter",
    model="gemini-2.5-flash",
    description="Domain expert for Operational Risk Issues and Action Plans.",
    instruction="You are the Issues Chapter Agent for Operational Risk.\nWhen queried about issues, you MUST delegate data extraction to the Analyst using the ask_analyst tool.\nTell the Analyst to query the 'issues' table at 'data/issues.csv' for high severity open issues.\nOnce you receive the data from the Analyst, delegate the report generation to the Reporter using the reporter tool.\nReturn the formatted report to the Orchestrator.\n",
    tools=[analyst_tool, reporter_tool, list_skills, read_skill]
)
issues_chapter_tool = AgentTool(issues_chapter)

# 4. Risk Metrics Chapter Agent
risk_metrics_chapter = Agent(
    name="risk_metrics_chapter",
    model="gemini-2.5-flash",
    description="Domain expert for Key Risk Indicators (KRIs).",
    instruction="You are the Risk Metrics Chapter Agent. \nWhen queried about risk metrics, delegate data extraction to the Analyst using the ask_analyst tool.\nTell the Analyst to query the 'risk_metrics' table at 'data/risk_metrics.csv' for Amber or Red metrics.\nIf the data is ambiguous, explicitly state what information is missing.\nOnce you receive the data, use the reporter tool to format the final response.\n",
    tools=[analyst_tool, reporter_tool]
)
risk_metrics_chapter_tool = AgentTool(risk_metrics_chapter)

# 5. Orchestrator Agent
orchestrator = Agent(
    name="orchestrator",
    model="gemini-2.5-flash",
    description="Central router for user requests.",
    instruction="You are the Central Orchestrator for Operational Risk.\nYou receive questions from users. You do NOT perform analysis or write reports.\nYou MUST route the user's question to the appropriate Chapter SME tool (issues_chapter or risk_metrics_chapter).\nCRITICAL: You must present the final draft report from the Chapter SME to the user and ask for approval BEFORE concluding.\nIf you need specific guidance or operational rules, use the list_skills and read_skill tools to consult your internal markdown guidelines.\n",
    tools=[issues_chapter_tool, risk_metrics_chapter_tool, list_skills, read_skill]
)
