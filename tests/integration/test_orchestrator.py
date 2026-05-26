# tests/integration/test_orchestrator.py
from dart_ops.orchestrator import create_orchestrator
from google.adk.agents import Agent

def test_orchestrator_initialization():
    dummy_chapter = Agent(name="Dummy", model="gemini-flash-latest", instruction="test")
    chapter_agents = {"Dummy": dummy_chapter}
    
    orchestrator = create_orchestrator(chapter_agents)
    assert orchestrator.name == "Expert_Analyst_Orchestrator"
    # Ensure it has a tool to call the chapter agent
    assert len(orchestrator.tools) > 0
