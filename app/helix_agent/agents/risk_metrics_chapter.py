from google.adk.agents import Agent
from google.adk.tools import AgentTool
from .analyst import analyst_tool
from .reporter import reporter_tool

risk_metrics_chapter = Agent(
    name="risk_metrics_chapter",
    model="gemini-2.5-flash",
    description="Domain expert for Key Risk Indicators (KRIs).",
    instruction="You are the Risk Metrics Chapter Agent. \nWhen queried about risk metrics, delegate data extraction to the Analyst using the ask_analyst tool.\nTell the Analyst to query the 'risk_metrics' table at 'data/risk_metrics.csv' for Amber or Red metrics.\nIf the data is ambiguous, explicitly state what information is missing.\nOnce you receive the data, use the reporter tool to format the final response.\n",
    tools=[analyst_tool, reporter_tool]
)
risk_metrics_chapter_tool = AgentTool(risk_metrics_chapter)
