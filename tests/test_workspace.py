import os
import csv
import yaml

def test_issues_csv():
    path = "data/issues.csv"
    assert os.path.exists(path)
    with open(path, "r", encoding="utf-8") as f:
        reader = list(csv.DictReader(f))
        assert len(reader) == 3
        # Check header
        assert set(reader[0].keys()) == {"issue_id", "title", "severity", "status", "open_date", "due_date"}
        # Check data
        assert reader[0]["issue_id"] == "I001"
        assert reader[0]["severity"] == "High"
        assert reader[0]["status"] == "Open"

def test_risk_metrics_csv():
    path = "data/risk_metrics.csv"
    assert os.path.exists(path)
    with open(path, "r", encoding="utf-8") as f:
        reader = list(csv.DictReader(f))
        assert len(reader) == 3
        # Check header
        assert set(reader[0].keys()) == {"metric_id", "metric_name", "value", "threshold", "status", "date"}
        # Check data
        assert reader[0]["metric_id"] == "M001"
        assert reader[1]["status"] == "Red"

def test_issues_yaml():
    path = "config/agents/issues.yaml"
    assert os.path.exists(path)
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
        assert data["name"] == "issues_agent"
        assert data["model"] == "gemini-2.5-flash"
        assert "duckdb" in data["instruction"].lower()

def test_risk_metrics_yaml():
    path = "config/agents/risk_metrics.yaml"
    assert os.path.exists(path)
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
        assert data["name"] == "risk_metrics_agent"
        assert data["model"] == "gemini-2.5-flash"
        assert "risk_metrics" in data["database_table"]

def test_second_lod_yaml():
    path = "config/reviewers/second_lod.yaml"
    assert os.path.exists(path)
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
        assert data["name"] == "second_lod_agent"
        assert data["model"] == "gemini-2.5-pro"
        assert "CHALLENGE" in data["instruction"]

if __name__ == "__main__":
    test_issues_csv()
    test_risk_metrics_csv()
    test_issues_yaml()
    test_risk_metrics_yaml()
    test_second_lod_yaml()
    print("All tests passed successfully!")

