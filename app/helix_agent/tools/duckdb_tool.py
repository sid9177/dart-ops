import os
import glob
import duckdb

# Initialize persistent in-memory connection
conn = duckdb.connect(':memory:')

# Pre-load CSVs from the data directory into DuckDB tables
def _preload_data():
    # Find the data directory.
    # This file is in app/helix_agent/tools/, so project root is 3 levels up
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    data_dir = os.path.join(project_root, "data")
    
    # Fallback to local 'data' directory if running directly from the root
    if not os.path.exists(data_dir):
        data_dir = "data"
        
    if os.path.exists(data_dir):
        csv_files = glob.glob(os.path.join(data_dir, "*.csv"))
        for csv_path in csv_files:
            table_name = os.path.splitext(os.path.basename(csv_path))[0]
            try:
                # Convert backslashes to forward slashes for DuckDB
                safe_path = csv_path.replace('\\', '/')
                # Load the CSV into a table of the same name
                conn.execute(f"CREATE OR REPLACE TABLE {table_name} AS SELECT * FROM read_csv_auto('{safe_path}')")
            except Exception as e:
                print(f"Warning: Failed to load {csv_path} into DuckDB: {e}")

# Run preload immediately when this module is imported
_preload_data()

def execute_duckdb_query(query: str) -> str:
    """Executes a SQL query using DuckDB and returns the result as a string."""
    try:
        # Query against the persistent connection instead of the default duckdb.query()
        result = conn.query(query).df()
        return result.to_string()
    except Exception as e:
        return f"Query Failed: {str(e)}. Please correct your SQL."
