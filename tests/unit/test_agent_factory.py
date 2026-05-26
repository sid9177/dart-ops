from dart_ops.agent_factory import create_all_agents

def test_create_all_agents():
    agents = create_all_agents()
    assert "orchestrator" in agents
    assert "issues_chapter" in agents
    assert "risk_metrics_chapter" in agents
    assert "analyst" in agents
    assert "reporter" in agents
    
    from dart_ops.tool_registry import REGISTRY
    assert "ask_analyst" in REGISTRY
    assert "ask_reporter" in REGISTRY
    
    # Check that docstrings use the description from yaml
    assert "Synthesizes raw data" in REGISTRY["ask_reporter"].__doc__
