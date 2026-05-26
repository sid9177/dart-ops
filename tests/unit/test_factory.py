import os
from dart_ops.factory import create_chapter_agents

def test_create_chapter_agents(tmp_path):
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
    assert agents["Issues"].name == "Issues_Agent"
