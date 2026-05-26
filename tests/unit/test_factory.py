from dart_ops.factory import create_chapter_agents

def test_create_chapter_agents():
    # Dummy config
    config = {
        "chapters": {
            "Issues": {
                "data_source": "data/issues.csv",
                "instructions": "You are Issues."
            }
        }
    }
    
    agents = create_chapter_agents(config)
    assert "Issues" in agents
    
    agent = agents["Issues"]
    assert agent.name == "Issues_Agent"
    assert "You are Issues." in agent.instruction
    assert "data/issues.csv" in agent.instruction
    assert len(agent.tools) == 1
