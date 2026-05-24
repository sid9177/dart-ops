import pytest
from db_helper import DuckDBHelper
from unittest.mock import patch
import pandas as pd

def test_duckdb_helper_flow(tmp_path):
    temp_csv = tmp_path / "temp_test.csv"
    temp_csv.write_text("col_a,col_b\n1,hello\n2,world\n", encoding="utf-8")

    helper = DuckDBHelper()
    helper.load_csv("test_table", str(temp_csv))

    # Test schema discovery
    schema = helper.get_table_schema("test_table")
    assert "col_a" in schema
    assert "col_b" in schema

    # Test query execution
    res = helper.run_sql_query("SELECT * FROM test_table WHERE col_a = 1")
    assert "hello" in res

def test_duckdb_helper_excel():
    helper = DuckDBHelper()
    mock_df = pd.DataFrame({"col_c": [3], "col_d": ["excel"]})
    with patch("pandas.read_excel", return_value=mock_df) as mock_read:
        helper.load_csv("excel_table", "dummy.xlsx")
        mock_read.assert_called_once_with("dummy.xlsx")
        
        schema = helper.get_table_schema("excel_table")
        assert "col_c" in schema
        assert "col_d" in schema
        
        res = helper.run_sql_query("SELECT * FROM excel_table")
        assert "excel" in res

def test_duckdb_helper_invalid_file():
    helper = DuckDBHelper()
    with pytest.raises(IOError):
        helper.load_csv("invalid_table", "non_existent_file.csv")
