from google.adk.agents import Agent
from google.adk.tools import AgentTool
from .analyst import analyst_tool
from .reporter import reporter_tool

issues_chapter = Agent(
    name="issues_chapter",
    model="gemini-2.5-flash",
    description="Domain expert for Operational Risk Issues and Action Plans.",
    instruction="You are the Issues Chapter Agent for Operational Risk.\nWhen queried about issues, you MUST delegate data extraction to the Analyst using the ask_analyst tool.\nTell the Analyst to query the 'issues' table at 'data/issues.csv' for high severity open issues.\nOnce you receive the data from the Analyst, delegate the report generation to the Reporter using the reporter tool.\nReturn the formatted report to the Orchestrator.\n",
    tools=[analyst_tool, reporter_tool]
)
issues_chapter_tool = AgentTool(issues_chapter)
