from app.helix_agent.agents import orchestrator, issues_chapter, risk_metrics_chapter, analyst, reporter
from app.helix_agent.tools import REGISTRY

def test_agents_configured_correctly():
    # Verify the agents exist
    assert orchestrator.name == "orchestrator"
    assert issues_chapter.name == "issues_chapter"
    assert risk_metrics_chapter.name == "risk_metrics_chapter"
    assert analyst.name == "analyst"
    assert reporter.name == "reporter"


    
    # Verify reporter instruction matches what was previously in the YAML
    assert "Generates final compliance reports" in reporter.description
