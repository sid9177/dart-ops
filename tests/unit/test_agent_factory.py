from dart_ops.agent_factory import create_all_agents

def test_create_all_agents():
    agents = create_all_agents()
    assert "orchestrator" in agents
    assert "issues_chapter" in agents
    assert "risk_metrics_chapter" in agents
    assert "analyst" in agents
    assert "reporter" in agents
    
    from dart_ops.tool_registry import REGISTRY
    assert "analyst" in REGISTRY
    assert "reporter" in REGISTRY
    
    # Check that tool descriptions use the description from yaml
    assert "Synthesizes raw data" in REGISTRY["reporter"].description
