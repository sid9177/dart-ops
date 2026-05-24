import pytest
import pytest_asyncio
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from agent import OperationalRiskCoordinator

@pytest.mark.asyncio
async def test_coordinator_loads_registry_and_runs():
    coordinator = OperationalRiskCoordinator()
    assert coordinator.db is not None
    assert coordinator.registry is not None
    assert "issues_agent" in coordinator.registry.agents

    session_service = InMemorySessionService()
    await session_service.create_session(app_name="app", user_id="user", session_id="s1")
    runner = Runner(agent=coordinator, app_name="app", session_service=session_service)
    
    responses = []
    async for event in runner.run_async(
        user_id="user",
        session_id="s1",
        new_message=types.Content(role="user", parts=[types.Part.from_text(text="I have an issue")])
    ):
        if event.content and event.content.parts:
            for part in event.content.parts:
                if part.text:
                    responses.append(part.text)
                    
    response_text = "".join(responses)
    assert "I would call the issues agent here" in response_text
