import asyncio
import os
import pytest
from unittest.mock import MagicMock, patch
from agent import OperationalRiskCoordinator
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

def run_async_generator(runner, user_id, session_id, message_text=None):
    """Helper to consume events from runner.run_async and return them as a list."""
    new_message = None
    if message_text is not None:
        new_message = types.Content(
            role="user",
            parts=[types.Part.from_text(text=message_text)]
        )
    
    events = []
    async def collect():
        async for event in runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=new_message
        ):
            events.append(event)
    
    asyncio.run(collect())
    return events

def test_coordinator_happy_path_with_revision():
    # Patch load_configs to not do real directory listing/loading
    with patch("registry.AgentRegistry.load_configs"):
        coordinator = OperationalRiskCoordinator()
        
        # Configure mocked registry agents
        issues_mock = MagicMock()
        metrics_mock = MagicMock()
        analyst_mock = MagicMock()
        second_lod_mock = MagicMock()
        
        coordinator._registry.agents = {
            "issues_agent": issues_mock,
            "risk_metrics_agent": metrics_mock,
            "expert_analyst_agent": analyst_mock,
            "second_lod_agent": second_lod_mock
        }
        coordinator._registry.reviewer_names = ["second_lod_agent"]
        
        # Define mock behaviors
        issues_mock.run.return_value = "Issues: MOCK_ISSUES"
        metrics_mock.run.return_value = "Metrics: MOCK_METRICS"
        analyst_mock.run.side_effect = ["Draft Report v1", "Draft Report v2 (Revised)"]
        second_lod_mock.run.return_value = "Review: Looks good, no challenges."
        
        # Setup runner
        session_service = InMemorySessionService()
        user_id = "test_user"
        session_id = "session_1"
        asyncio.run(session_service.create_session(app_name="app", user_id=user_id, session_id=session_id))
        
        runner = Runner(agent=coordinator, app_name="app", session_service=session_service)
        
        # --- TURN 1: Start (Generate Draft Report v1) ---
        events_1 = run_async_generator(runner, user_id, session_id, "Start generating report")
        
        # Assertions for Turn 1
        assert len(events_1) >= 2
        assert "Initializing report generation..." in events_1[0].content.parts[0].text
        assert "Draft Report v1" in events_1[1].content.parts[0].text
        assert "Gate 1 (Draft Review)" in events_1[1].content.parts[0].text
        
        # Check persisted session state
        session = asyncio.run(session_service.get_session(app_name="app", user_id=user_id, session_id=session_id))
        assert session.state["stage"] == "gate_1_review"
        assert session.state["draft_report"] == "Draft Report v1"
        
        # --- TURN 2: User requests revision ---
        events_2 = run_async_generator(runner, user_id, session_id, "Add Citigroup guidelines info")
        
        # Assertions for Turn 2
        assert len(events_2) == 1
        assert "Draft Report v2 (Revised)" in events_2[0].content.parts[0].text
        
        session = asyncio.run(session_service.get_session(app_name="app", user_id=user_id, session_id=session_id))
        assert session.state["stage"] == "gate_1_review"
        assert session.state["draft_report"] == "Draft Report v2 (Revised)"
        
        # --- TURN 3: User approves ---
        events_3 = run_async_generator(runner, user_id, session_id, "APPROVE")
        
        # Assertions for Turn 3
        assert len(events_3) >= 2
        assert "Draft approved! Starting Lines of Defense" in events_3[0].content.parts[0].text
        assert "FINAL REPORT FOR SIGN-OFF" in events_3[1].content.parts[0].text
        assert "Draft Report v2 (Revised)" in events_3[1].content.parts[0].text
        assert "Review: Looks good, no challenges." in events_3[1].content.parts[0].text
        
        session = asyncio.run(session_service.get_session(app_name="app", user_id=user_id, session_id=session_id))
        assert session.state["stage"] == "gate_3_signoff"
        
        # --- TURN 4: User sign-off ---
        with patch("agent.export_report_to_pdf") as pdf_mock, patch("agent.export_report_to_pptx") as pptx_mock:
            events_4 = run_async_generator(runner, user_id, session_id, "SIGN-OFF")
            
            assert len(events_4) == 1
            assert "Report signed off and saved" in events_4[0].content.parts[0].text
            pdf_mock.assert_called_once()
            pptx_mock.assert_called_once()
            
            session = asyncio.run(session_service.get_session(app_name="app", user_id=user_id, session_id=session_id))
            assert session.state.get("stage") is None

def test_coordinator_reviewer_challenge_and_sequential():
    with patch("registry.AgentRegistry.load_configs"):
        coordinator = OperationalRiskCoordinator()
        
        issues_mock = MagicMock()
        metrics_mock = MagicMock()
        analyst_mock = MagicMock()
        second_lod_mock = MagicMock()
        third_lod_mock = MagicMock()
        
        coordinator._registry.agents = {
            "issues_agent": issues_mock,
            "risk_metrics_agent": metrics_mock,
            "expert_analyst_agent": analyst_mock,
            "second_lod_agent": second_lod_mock,
            "third_lod_agent": third_lod_mock
        }
        # Run two reviewers sequentially
        coordinator._registry.reviewer_names = ["second_lod_agent", "third_lod_agent"]
        
        issues_mock.run.return_value = "Issues: OK"
        metrics_mock.run.return_value = "Metrics: OK"
        analyst_mock.run.return_value = "Draft Report v1"
        
        # second_lod challenges first, then is satisfied. third_lod is immediately satisfied.
        second_lod_mock.run.side_effect = [
            "[CHALLENGE]: Why is Amber metric M002 not covered by issues?",
            "Resolved. Looks good now."
        ]
        third_lod_mock.run.return_value = "Third LOD comments: Pass."
        
        session_service = InMemorySessionService()
        user_id = "test_user"
        session_id = "session_2"
        asyncio.run(session_service.create_session(app_name="app", user_id=user_id, session_id=session_id))
        
        runner = Runner(agent=coordinator, app_name="app", session_service=session_service)
        
        # --- TURN 1: Start ---
        run_async_generator(runner, user_id, session_id, "Start")
        
        # --- TURN 2: Approve (trigging challenges) ---
        events_2 = run_async_generator(runner, user_id, session_id, "APPROVE")
        
        # Check that we received the challenge from second_lod_agent
        assert len(events_2) >= 2
        assert "Draft approved!" in events_2[0].content.parts[0].text
        assert "second_lod_agent raised a challenge" in events_2[1].content.parts[0].text
        assert "Why is Amber metric M002 not covered" in events_2[1].content.parts[0].text
        
        session = asyncio.run(session_service.get_session(app_name="app", user_id=user_id, session_id=session_id))
        assert session.state["stage"] == "gate_2_challenge"
        assert session.state["active_reviewer"] == "second_lod_agent"
        assert "second_lod_agent" not in session.state["satisfied_reviewers"]
        
        # --- TURN 3: Answer challenge ---
        events_3 = run_async_generator(runner, user_id, session_id, "Because issue I003 mitigates M002")
        
        # second_lod re-evaluates, passes, then loop runs third_lod which also passes immediately
        assert len(events_3) >= 2
        assert "LOD Challenge successfully resolved" in events_3[0].content.parts[0].text
        assert "FINAL REPORT FOR SIGN-OFF" in events_3[-1].content.parts[0].text
        
        session = asyncio.run(session_service.get_session(app_name="app", user_id=user_id, session_id=session_id))
        assert session.state["stage"] == "gate_3_signoff"
        assert "second_lod_agent" in session.state["satisfied_reviewers"]
        assert "third_lod_agent" in session.state["satisfied_reviewers"]
        
        # --- TURN 4: Revise instead of sign-off ---
        events_4 = run_async_generator(runner, user_id, session_id, "REVISE")
        assert len(events_4) == 1
        assert "Resetting process" in events_4[0].content.parts[0].text
        
        session = asyncio.run(session_service.get_session(app_name="app", user_id=user_id, session_id=session_id))
        assert session.state["stage"] == "start"
