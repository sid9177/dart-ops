import os
import duckdb
from dart_ops.duckdb_tool import execute_duckdb_query

def test_execute_duckdb_query(tmp_path):
    # Setup dummy csv
    csv_file = tmp_path / "test_data.csv"
    with open(csv_file, "w") as f:
        f.write("id,value\n1,100\n2,200\n")
        
    query = f"SELECT SUM(value) as total FROM read_csv_auto('{csv_file}')"
    result = execute_duckdb_query(query)
    
    assert "300" in result
