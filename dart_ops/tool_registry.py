from dart_ops.duckdb_tool import execute_duckdb_query
from dart_ops.skill_tool import list_skills, read_skill

REGISTRY = {
    "execute_duckdb_query": execute_duckdb_query,
    "list_skills": list_skills,
    "read_skill": read_skill,
}
