import os
import yaml
import re
from google.adk.agents.llm_agent import Agent
from db_helper import DuckDBHelper

class AgentRegistry:
    def __init__(self, config_dir: str = "config"):
        self.config_dir = config_dir
        self.agents = {}
        self.db = DuckDBHelper()

    def load_configs(self):
        # Load chapter agents
        agents_path = os.path.join(self.config_dir, "agents")
        if os.path.exists(agents_path):
            for f in os.listdir(agents_path):
                if f.endswith(".yaml") or f.endswith(".yml"):
                    with open(os.path.join(agents_path, f), "r") as stream:
                        config = yaml.safe_load(stream)
                        self._register_agent(config, is_reviewer=False)
                        
        # Load reviewer agents
        reviewers_path = os.path.join(self.config_dir, "reviewers")
        if os.path.exists(reviewers_path):
            for f in os.listdir(reviewers_path):
                if f.endswith(".yaml") or f.endswith(".yml"):
                    with open(os.path.join(reviewers_path, f), "r") as stream:
                        config = yaml.safe_load(stream)
                        self._register_agent(config, is_reviewer=True)

    def _register_agent(self, config: dict, is_reviewer: bool):
        name = config.get("name")
        model = config.get("model", "gemini-2.5-flash")
        instruction = config.get("instruction", "")
        description = config.get("description", "")
        
        file_path = config.get("file_path")
        table_name = config.get("database_table")
        
        agent_tools = []
        if not is_reviewer and file_path and table_name:
            # Load file into DuckDB
            # Resolve relative file path relative to project root
            base_dir = os.path.dirname(os.path.abspath(__file__))
            full_path = os.path.join(base_dir, file_path) if not os.path.isabs(file_path) else file_path
            
            # Ensure path exists, if not log warning and skip
            if os.path.exists(full_path):
                self.db.load_csv(table_name, full_path)
                
                # Define schema discovery and query tools
                def get_schema(table=table_name):
                    return self.db.get_table_schema(table)
                
                def run_query(sql: str):
                    return self.db.run_sql_query(sql)
                    
                get_schema.__name__ = f"get_{table_name}_schema"
                get_schema.__doc__ = f"Get column names and schema for table '{table_name}'."
                run_query.__name__ = f"query_{table_name}"
                run_query.__doc__ = f"Run read-only SQL queries on table '{table_name}'."
                
                agent_tools = [get_schema, run_query]

        agent = Agent(
            name=name,
            model=model,
            instruction=instruction,
            description=description,
            tools=agent_tools
        )
        self.agents[name] = agent

    def get_all_tools(self) -> list:
        # Wrap each agent as an ADK tool
        tools = []
        for name, agent in self.agents.items():
            def make_agent_tool(a_name=name, a_agent=agent):
                def call_agent(query: str) -> str:
                    return a_agent.run(query)
                call_agent.__name__ = f"call_{a_name}"
                call_agent.__doc__ = f"Query {a_name} agent to analyze: {a_agent.description}"
                return call_agent
            tools.append(make_agent_tool())
        return tools
