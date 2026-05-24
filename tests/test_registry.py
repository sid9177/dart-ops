import os
import yaml
import pytest
from unittest.mock import patch, MagicMock
from registry import AgentRegistry

def test_registry_initialization():
    registry = AgentRegistry(config_dir="dummy_config")
    assert registry.config_dir == "dummy_config"
    assert isinstance(registry.agents, dict)
    assert len(registry.agents) == 0

def test_registry_load_and_register(tmp_path):
    # Create mock config directories
    agents_dir = tmp_path / "agents"
    reviewers_dir = tmp_path / "reviewers"
    os.makedirs(agents_dir, exist_ok=True)
    os.makedirs(reviewers_dir, exist_ok=True)

    # 1. Chapter agent config (with DB and file)
    issues_config = {
        "name": "issues_agent",
        "model": "gemini-2.5-flash",
        "description": "Queries issues.",
        "instruction": "Find open issues.",
        "database_table": "issues",
        "file_path": "dummy_issues.csv"
    }
    with open(agents_dir / "issues.yaml", "w", encoding="utf-8") as f:
        yaml.safe_dump(issues_config, f)

    # Create dummy csv in the tmp path
    dummy_csv = tmp_path / "dummy_issues.csv"
    dummy_csv.write_text("id,severity\n1,High\n", encoding="utf-8")

    # 2. Reviewer agent config (no DB/file)
    reviewer_config = {
        "name": "second_lod_agent",
        "model": "gemini-2.5-pro",
        "description": "2nd LOD Officer.",
        "instruction": "Review draft.",
    }
    with open(reviewers_dir / "second_lod.yaml", "w", encoding="utf-8") as f:
        yaml.safe_dump(reviewer_config, f)

    # We will mock the base_dir check in registry.py to use tmp_path for resolving relative CSV paths
    with patch("os.path.dirname", return_value=str(tmp_path)):
        registry = AgentRegistry(config_dir=str(tmp_path))
        registry.load_configs()

    # Assert agents are instantiated correctly
    assert "issues_agent" in registry.agents
    assert "second_lod_agent" in registry.agents

    issues_agent = registry.agents["issues_agent"]
    second_lod_agent = registry.agents["second_lod_agent"]

    assert issues_agent.name == "issues_agent"
    assert issues_agent.model == "gemini-2.5-flash"
    assert issues_agent.description == "Queries issues."
    assert issues_agent.instruction == "Find open issues."
    
    # Verify chapter agent gets DuckDB tools
    assert len(issues_agent.tools) == 2
    tool_names = [t.__name__ for t in issues_agent.tools]
    assert "get_issues_schema" in tool_names
    assert "query_issues" in tool_names

    # Verify reviewer gets no tools
    assert len(second_lod_agent.tools) == 0

    # Verify DuckDB loader was called
    schema = registry.db.get_table_schema("issues")
    assert "id" in schema
    assert "severity" in schema

    # Verify get_all_tools generates wrapper callables
    tools = registry.get_all_tools()
    assert len(tools) == 2
    p2p_tool_names = [t.name for t in tools]
    assert "issues_agent" in p2p_tool_names
    assert "second_lod_agent" in p2p_tool_names

    # Verify docs are set correctly
    issues_tool = next(t for t in tools if t.name == "issues_agent")
    assert "Queries issues." in issues_tool._get_declaration().description
