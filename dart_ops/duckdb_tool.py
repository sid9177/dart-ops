import duckdb

def execute_duckdb_query(query: str) -> str:
    """Executes a SQL query using DuckDB and returns the result as a string."""
    try:
        # In-memory execution for speed, reading directly from CSVs via SQL
        result = duckdb.query(query).df()
        return result.to_string()
    except Exception as e:
        return f"Query Failed: {str(e)}. Please correct your SQL."
