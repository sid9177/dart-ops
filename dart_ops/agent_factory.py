import os
from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from dart_ops.tool_registry import REGISTRY
from dart_ops.config_reader import load_chapters_config

def create_all_agents() -> dict:
    """Reads all agent YAML configs, builds them, and returns a dictionary of Agents."""
    config_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config", "agents")
    agents = {}
    
    # First pass: Build all chapter agents
    for filename in os.listdir(config_dir):
        if filename.endswith(".yaml") and filename != "orchestrator.yaml":
            file_path = os.path.join(config_dir, filename)
            config = load_chapters_config(file_path)
            
            agent_tools = []
            from google.adk.tools import BaseTool
            for tool_name in config.get("tools", []):
                if tool_name in REGISTRY:
                    tool_obj = REGISTRY[tool_name]
                    if isinstance(tool_obj, BaseTool):
                        agent_tools.append(tool_obj)
                    else:
                        agent_tools.append(FunctionTool(func=tool_obj))
            
            agent = Agent(
                name=config.get("name", filename.replace(".yaml", "")),
                model=config.get("model", "gemini-2.5-flash"),
                instruction=config.get("instruction", ""),
                tools=agent_tools
            )
            agents[config.get("name")] = agent
            
            from google.adk.tools import AgentTool
            agent.description = config.get("description", f"Use this agent for queries related to {config.get('name')}.")
            chapter_caller = AgentTool(agent)
            
            REGISTRY[chapter_caller.name] = chapter_caller

    # Second pass: Build Orchestrator
    orchestrator_path = os.path.join(config_dir, "orchestrator.yaml")
    if os.path.exists(orchestrator_path):
        orch_config = load_chapters_config(orchestrator_path)
        
        orch_tools = []
        for tool_name in orch_config.get("tools", []):
            if tool_name in REGISTRY:
                tool_obj = REGISTRY[tool_name]
                if isinstance(tool_obj, BaseTool):
                    orch_tools.append(tool_obj)
                else:
                    orch_tools.append(FunctionTool(func=tool_obj))
                
        orchestrator = Agent(
            name=orch_config.get("name", "expert_analyst_orchestrator"),
            model=orch_config.get("model", "gemini-2.5-flash"),
            instruction=orch_config.get("instruction", ""),
            tools=orch_tools
        )
        agents["orchestrator"] = orchestrator
        
    return agents

# Instantiate and export the orchestrator so it can be auto-discovered by ADK
all_agents = create_all_agents()
orchestrator_agent = all_agents.get("orchestrator")
