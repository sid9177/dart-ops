# TODO: Copy the imports for `App` and `ResumabilityConfig` from your sample agent and paste them here!
# Example: from helix_internal_adk import App, ResumabilityConfig

from .agents import orchestrator as root_agent
from .plugins import LightweightObservabilityPlugin

app = App(
    name="OpsDART",
    root_agent=root_agent,
    resumability_config=ResumabilityConfig(is_resumable=False),
    plugins=[LightweightObservabilityPlugin()]
)
