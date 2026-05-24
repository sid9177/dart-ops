import os
from typing import Any, AsyncGenerator

from google.adk.agents import BaseAgent
from google.adk.agents.invocation_context import InvocationContext
from google.adk.events import Event, EventActions
from google.genai import types

from registry import AgentRegistry
from db_helper import DuckDBHelper

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

    async def _run_async_impl(self, ctx: InvocationContext) -> AsyncGenerator[Event, None]:
        user_input = ""
        if ctx.session.events:
            for ev in reversed(ctx.session.events):
                if ev.author == "user" and ev.content and ev.content.parts:
                    texts = [p.text for p in ev.content.parts if p.text]
                    if texts:
                        user_input = "".join(texts)
                        break
        
        # For now, just route to a specific chapter if requested
        if "issue" in user_input.lower():
            issues_agent = self.registry.agents.get("issues_agent")
            if issues_agent:
                yield Event(
                    author=self.name,
                    content=types.Content(
                        role="model",
                        parts=[types.Part.from_text(text="I would call the issues agent here.")]
                    )
                )
                return
        
        yield Event(
            author=self.name,
            content=types.Content(
                role="model",
                parts=[types.Part.from_text(text="I am the Operational Risk Coordinator. Which chapter do you want to query?")]
            )
        )

# This exposes the root agent for `agents-cli playground`
agent = OperationalRiskCoordinator()
