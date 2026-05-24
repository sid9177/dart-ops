import os
from pathlib import Path
import pytest
from db_helper import DuckDBHelper

def test_duckdb_helper_flow():
    base_dir = Path(__file__).parent
    temp_csv = base_dir / "temp_test.csv"
    
    with open(temp_csv, "w") as f:
        f.write("col_a,col_b\n1,hello\n2,world\n")

    try:
        helper = DuckDBHelper()
        helper.load_csv("test_table", str(temp_csv))

        # Test schema discovery
        schema = helper.get_table_schema("test_table")
        assert "col_a" in schema
        assert "col_b" in schema

        # Test query execution
        res = helper.run_sql_query("SELECT * FROM test_table WHERE col_a = 1")
        assert "hello" in res
    finally:
        # Clean up
        if temp_csv.exists():
            os.remove(temp_csv)
