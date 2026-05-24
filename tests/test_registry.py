import os
import yaml
import pytest
from registry import AgentRegistry

class MockDuckDBHelper:
    def __init__(self):
        self.loaded = []
        self.queries = []
        
    def load_csv(self, table_name, file_path):
        self.loaded.append((table_name, file_path))
        
    def get_table_schema(self, table_name):
        return f"schema_for_{table_name}"
        
    def run_sql_query(self, sql_query):
        self.queries.append(sql_query)
        return "mock_result"

def test_registry_initialization():
    db = MockDuckDBHelper()
    registry = AgentRegistry(db)
    assert len(registry.agents) == 0

def test_registry_load_and_register(tmp_path):
    db = MockDuckDBHelper()
    registry = AgentRegistry(db)
    
    # Create mock configs
    config_dir = tmp_path / "agents"
    config_dir.mkdir()
    
    # create dummy csv file to pass os.path.exists
    csv_path = tmp_path / "data1.csv"
    csv_path.write_text("dummy,csv\n1,2")
    
    # Agent 1 with db table
    agent1_file = config_dir / "agent1.yaml"
    agent1_data = {
        "name": "test_agent_1",
        "model": "test-model",
        "instruction": "Test instructions 1",
        "database_table": "test_table_1",
        "file_path": str(csv_path)
    }
    with open(agent1_file, "w") as f:
        yaml.dump(agent1_data, f)
        
    # Agent 2 without db table
    agent2_file = config_dir / "agent2.yaml"
    agent2_data = {
        "name": "test_agent_2",
        "instruction": "Test instructions 2"
    }
    with open(agent2_file, "w") as f:
        yaml.dump(agent2_data, f)
        
    registry.load_chapter_agents(str(config_dir))
    
    # 1. Verify agents loaded
    assert "test_agent_1" in registry.agents
    assert "test_agent_2" in registry.agents
    
    # 2. Verify data loaded
    assert len(db.loaded) == 1
    assert db.loaded[0] == ("test_table_1", str(csv_path))
    
    # 3. Verify tool coverage for Agent 1
    agent1 = registry.agents["test_agent_1"]
    assert len(agent1.tools) == 2
    
    get_schema_tool = next(t for t in agent1.tools if t.__name__ == "get_test_table_1_schema")
    run_sql_tool = next(t for t in agent1.tools if t.__name__ == "query_test_table_1_table")
    
    assert "test_table_1" in get_schema_tool.__doc__
    assert "test_table_1" in run_sql_tool.__doc__
    
    # Verify execution of the generated tools
    schema_res = get_schema_tool()
    assert schema_res == {"schema": "schema_for_test_table_1"}
    
    sql_res = run_sql_tool("SELECT * FROM test")
    assert sql_res == {"result": "mock_result"}
    assert db.queries == ["SELECT * FROM test"]
    
    # 4. Verify no tools for Agent 2
    agent2 = registry.agents["test_agent_2"]
    assert len(agent2.tools) == 0
