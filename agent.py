import os
from google.adk.agents import BaseAgent
from registry import AgentRegistry
from db_helper import DuckDBHelper

from typing import Any

class OperationalRiskCoordinator(BaseAgent):
    """The root agent orchestrating Operational Risk chapters."""
    db: Any = None
    registry: Any = None
    
    def __init__(self, name: str = "operational_risk_coordinator", **kwargs):
        super().__init__(name=name, **kwargs)
        self.db = DuckDBHelper()
        self.registry = AgentRegistry(self.db)
        
        # Load agents from config
        config_path = os.path.join(os.path.dirname(__file__), "config", "agents")
        self.registry.load_chapter_agents(config_path)

    def run(self, user_input: str) -> str:
        # For now, just route to a specific chapter if requested
        if "issue" in user_input.lower():
            issues_agent = self.registry.agents.get("issues_agent")
            if issues_agent:
                response = issues_agent(user_input)
                return response.text
        
        return "I am the Operational Risk Coordinator. Which chapter do you want to query?"

# This exposes the root agent for `agents-cli playground`
agent = OperationalRiskCoordinator()
