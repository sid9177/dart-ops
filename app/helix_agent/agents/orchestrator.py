from google.adk.agents import Agent
from .issues_chapter import issues_chapter_tool
from .risk_metrics_chapter import risk_metrics_chapter_tool
from .ui_agent import ui_agent_tool

orchestrator = Agent(
    name="orchestrator",
    model="gemini-2.5-flash",
    description="Central router for user requests.",
    instruction="You are the Central Orchestrator for Operational Risk.\nYou receive questions from users. You do NOT perform analysis or write reports.\nYou MUST route the user's question to the appropriate Chapter SME tool (issues_chapter or risk_metrics_chapter).\nAfter receiving analysis from the Chapter SME, you MUST route the result to the ui_agent tool to compose the reporting workspace surfaces.\nCRITICAL: You must ask for approval via the ui_agent's approval_gate BEFORE concluding.\n",
    tools=[issues_chapter_tool, risk_metrics_chapter_tool, ui_agent_tool]
)
