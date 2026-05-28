from typing import Any, Optional
from google.adk.plugins.base_plugin import BasePlugin
from google.adk.agents.callback_context import CallbackContext
from google.adk.tools.base_tool import BaseTool
from google.adk.tools.tool_context import ToolContext
from google.adk.agents.base_agent import BaseAgent
from google.adk.models.llm_response import LlmResponse
from google.genai import types

class LightweightObservabilityPlugin(BasePlugin):
    """A custom ADK plugin for lightweight console observability."""

    def __init__(self, name: str = "lightweight_observability"):
        super().__init__(name)

    def _log(self, message: str) -> None:
        print(f"\033[96m[OBSERVABILITY]\033[0m {message}")

    async def before_agent_callback(
        self, *, agent: BaseAgent, callback_context: CallbackContext
    ) -> Optional[types.Content]:
        agent_name = getattr(callback_context, "agent_name", "Unknown Agent")
        self._log(f"🚀 Agent '{agent_name}' has taken over...")
        return None

    async def before_tool_callback(
        self,
        *,
        tool: BaseTool,
        tool_args: dict[str, Any],
        tool_context: ToolContext,
    ) -> Optional[dict]:
        agent_name = getattr(tool_context, "agent_name", "Unknown Agent")
        self._log(f"🛠️  Agent '{agent_name}' is executing tool: {tool.name}")
        return None

    async def after_model_callback(
        self, *, callback_context: CallbackContext, llm_response: LlmResponse
    ) -> Optional[LlmResponse]:
        if llm_response and llm_response.content and llm_response.content.parts:
            for part in llm_response.content.parts:
                if part.text:
                    text = part.text.strip()
                    if text:
                        self._log(f"🧠 Reasoning: {text}")
        return None
