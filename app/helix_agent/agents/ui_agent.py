from pathlib import Path

from google.adk.agents import Agent
from google.adk.tools import AgentTool

_SKILLS_DIR = Path(__file__).resolve().parent.parent / "skills"


def _load_instruction() -> str:
    instruction_path = _SKILLS_DIR / "ui_agent.md"
    return instruction_path.read_text(encoding="utf-8")


ui_agent = Agent(
    name="ui_agent",
    model="gemini-2.5-flash",
    description="Composes A2UI surfaces from analysis payloads for the reporting workspace.",
    instruction=_load_instruction(),
    tools=[],
)

ui_agent_tool = AgentTool(ui_agent)