import pytest
from agent import OperationalRiskCoordinator

def test_coordinator_loads_registry():
    coordinator = OperationalRiskCoordinator()
    assert coordinator.db is not None
    assert coordinator.registry is not None
    assert "issues_agent" in coordinator.registry.agents
