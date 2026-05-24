import os
import yaml
from google.adk.agents import Agent
from db_helper import DuckDBHelper

class AgentRegistry:
    def __init__(self, db_helper: DuckDBHelper):
        self.db_helper = db_helper
        self.agents: dict[str, Agent] = {}

    def load_chapter_agents(self, config_dir: str):
        if not os.path.exists(config_dir):
            return

        for filename in os.listdir(config_dir):
            if filename.endswith(".yaml") or filename.endswith(".yml"):
                filepath = os.path.join(config_dir, filename)
                with open(filepath, "r") as f:
                    config = yaml.safe_load(f)

                # 1. Load data into DuckDB if specified
                table_name = config.get("database_table")
                file_path = config.get("file_path")
                if table_name and file_path and os.path.exists(file_path):
                    try:
                        self.db_helper.load_csv(table_name, file_path)
                    except Exception as e:
                        print(f"Warning: Failed to load data for {config['name']}: {e}")

                # 2. Create tools bounded to this table
                tools = []
                if table_name:
                    def get_schema() -> str:
                        """Get the schema of the assigned database table."""
                        return self.db_helper.get_table_schema(table_name)
                    get_schema.__name__ = f"get_{table_name}_schema"
                    
                    def run_sql(sql_query: str) -> str:
                        """Run a SQL query against the database."""
                        return self.db_helper.run_sql_query(sql_query)
                    run_sql.__name__ = f"query_{table_name}_table"

                    tools = [
                        get_schema,
                        run_sql
                    ]

                # 3. Instantiate ADK Agent
                agent = Agent(
                    name=config["name"],
                    model=config.get("model", "gemini-2.5-flash"),
                    instruction=config.get("instruction", ""),
                    tools=tools
                )
                self.agents[config["name"]] = agent
