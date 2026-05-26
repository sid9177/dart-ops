import os
import yaml
import pytest
from dart_ops.config_reader import load_chapters_config

def test_load_chapters_config(tmp_path):
    # Create a dummy yaml file
    config_file = tmp_path / "chapters.yaml"
    config_data = {
        "chapters": {
            "Issues": {
                "data_source": "data/issues.csv",
                "instructions": "You are the Issues Chapter Agent.",
                "skills": ["regulator_perspective.md"]
            }
        }
    }
    with open(config_file, "w") as f:
        yaml.dump(config_data, f)
        
    config = load_chapters_config(str(config_file))
    assert "Issues" in config["chapters"]
    assert config["chapters"]["Issues"]["data_source"] == "data/issues.csv"
