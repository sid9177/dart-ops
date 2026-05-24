import duckdb
import pandas as pd

class DuckDBHelper:
    def __init__(self):
        self.conn = duckdb.connect(database=":memory:")

    def load_csv(self, table_name: str, file_path: str):
        if file_path.endswith((".xlsx", ".xls")):
            df = pd.read_excel(file_path)
            self.conn.register(table_name, df)
        else:
            # Normalize path for DuckDB on Windows
            normalized_path = file_path.replace("\\", "/")
            self.conn.execute(f"CREATE TABLE {table_name} AS SELECT * FROM read_csv_auto('{normalized_path}')")

    def get_table_schema(self, table_name: str) -> str:
        try:
            res = self.conn.execute(f"DESCRIBE {table_name}").fetchall()
            schema_lines = [f"{row[0]} ({row[1]})" for row in res]
            return f"Table '{table_name}' columns:\n" + "\n".join(schema_lines)
        except Exception as e:
            return f"Error fetching schema: {str(e)}"

    def run_sql_query(self, sql_query: str) -> str:
        try:
            df = self.conn.execute(sql_query).df()
            return df.to_string(index=False)
        except Exception as e:
            return f"SQL Error: {str(e)}"
