from google.adk.agents import Agent
from google.adk.tools import AgentTool
from app.helix_agent.tools import execute_duckdb_query

analyst = Agent(
    name="analyst",
    model="gemini-2.5-flash",
    description="Executes database queries to extract requested data.",
    instruction="You are a generic Data Analyst agent.\nYou receive data extraction requests from Chapter SMEs.\nUse the execute_duckdb_query tool to run SQL queries against the specified database tables and return the raw JSON data.\n",
    tools=[execute_duckdb_query]
)
analyst_tool = AgentTool(analyst)
