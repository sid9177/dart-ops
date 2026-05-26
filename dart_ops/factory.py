from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from dart_ops.duckdb_tool import execute_duckdb_query

def create_chapter_agents(config: dict) -> dict:
    """Dynamically creates ADK Agents based on the chapters config."""
    agents = {}
    
    # Create the generic tool once
    data_tool = FunctionTool(func=execute_duckdb_query)
    
    for chapter_name, details in config.get("chapters", {}).items():
        base_instructions = details.get("instructions", "")
        data_source = details.get("data_source", "")
        
        # Inject the file path into the prompt so the agent knows what to query
        full_instruction = f"{base_instructions}\n\nYou must query the data located at: {data_source}"
        
        agent = Agent(
            name=f"{chapter_name}_Agent",
            model="gemini-flash-latest",
            instruction=full_instruction,
            tools=[data_tool]
        )
        agents[chapter_name] = agent
        
    return agents
