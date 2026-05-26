# dart_ops/orchestrator.py
from google.adk.agents import Agent
from google.adk.tools import FunctionTool

def create_orchestrator(chapter_agents: dict) -> Agent:
    """Creates the Central Orchestrator (Expert Analyst) that delegates to Chapters."""
    
    # We dynamically create a python tool for each chapter agent so the Orchestrator can call them
    orchestrator_tools = []
    
    for name, agent in chapter_agents.items():
        # A wrapper function that allows the orchestrator to send a prompt to the chapter agent
        def chapter_caller(query: str, agent_instance=agent) -> str:
            """Sends a query to a specific Operational Risk Chapter."""
            # Note: actual ADK invoke syntax used here
            return agent_instance.invoke(query)
            
        # Rename function to avoid collisions
        chapter_caller.__name__ = f"ask_{name.lower()}_chapter"
        chapter_caller.__doc__ = f"Use this tool to ask questions and get data from the {name} chapter."
        
        tool = FunctionTool(func=chapter_caller)
        orchestrator_tools.append(tool)
        
    orchestrator = Agent(
        name="Expert_Analyst_Orchestrator",
        model="gemini-flash-latest",
        instruction="You are the Central Expert Analyst for Operational Risk. You receive questions from users. Use your chapter tools to gather data, synthesize the results, and provide a final formatted report.",
        tools=orchestrator_tools
    )
    
    return orchestrator
