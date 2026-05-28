from google.adk.agents import Agent
from .issues_chapter import issues_chapter_tool
from .risk_metrics_chapter import risk_metrics_chapter_tool

orchestrator = Agent(
    name="orchestrator",
    model="gemini-2.5-flash",
    description="Central router for user requests.",
    instruction="You are the Central Orchestrator for Operational Risk.\nYou receive questions from users. You do NOT perform analysis or write reports.\nYou MUST route the user's question to the appropriate Chapter SME tool (issues_chapter or risk_metrics_chapter).\nCRITICAL: You must present the final draft report from the Chapter SME to the user and ask for approval BEFORE concluding.\n",
    tools=[issues_chapter_tool, risk_metrics_chapter_tool]
)
