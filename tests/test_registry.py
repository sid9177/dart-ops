from registry import AgentRegistry
from db_helper import DuckDBHelper

def test_registry_initialization():
    db = DuckDBHelper()
    registry = AgentRegistry(db)
    assert len(registry.agents) == 0

def test_registry_load_and_register():
    db = DuckDBHelper()
    registry = AgentRegistry(db)
    # The registry should be able to load agents from config/agents directory
    registry.load_chapter_agents("config/agents")
    # Should at least find issues and risk_metrics
    assert "issues_agent" in registry.agents
    assert "risk_metrics_agent" in registry.agents
