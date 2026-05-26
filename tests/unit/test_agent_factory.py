from app.helix_agent.agent_utils import create_all_agents

def test_create_all_agents():
    agents = create_all_agents()
    assert "orchestrator" in agents
    assert "issues_chapter" in agents
    assert "risk_metrics_chapter" in agents
    assert "analyst" in agents
    assert "reporter" in agents
    
    from app.helix_agent.tools import REGISTRY
    assert "analyst" in REGISTRY
    assert "reporter" in REGISTRY
    
    # Check that tool descriptions use the description from yaml
    assert "Synthesizes raw data" in REGISTRY["reporter"].description
