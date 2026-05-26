import os
import glob
import duckdb

# --- DUCKDB TOOL ---
def execute_duckdb_query(query: str) -> str:
    """Executes a SQL query using DuckDB and returns the result as a string."""
    try:
        result = duckdb.query(query).df()
        return result.to_string()
    except Exception as e:
        return f"Query Failed: {str(e)}. Please correct your SQL."

# --- SKILL TOOLS ---
def get_skills_dir() -> str:
    # Look for the 'skills' folder in the same directory as this file
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "skills")

def list_skills() -> str:
    """Lists all available markdown skills in the skills directory."""
    skills_dir = get_skills_dir()
    if not os.path.exists(skills_dir):
        return "No skills directory found."
    
    skills = []
    for filepath in glob.glob(os.path.join(skills_dir, "*.md")):
        skills.append(os.path.basename(filepath))
    
    if not skills:
        return "No skills found."
        
    return "Available skills: " + ", ".join(skills)

def read_skill(skill_name: str) -> str:
    """Reads and returns the contents of a specific skill markdown file. Ensure you pass the correct filename (e.g. 'regulator_perspective.md')."""
    skills_dir = get_skills_dir()
    safe_name = os.path.basename(skill_name)
    if not safe_name.endswith('.md'):
        safe_name += '.md'
        
    skill_path = os.path.join(skills_dir, safe_name)
    if not os.path.exists(skill_path):
        return f"Error: Skill '{safe_name}' not found. Please use list_skills to see available skills."
        
    try:
        with open(skill_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Error reading skill: {str(e)}"

# --- REGISTRY ---
REGISTRY = {
    "execute_duckdb_query": execute_duckdb_query,
    "list_skills": list_skills,
    "read_skill": read_skill,
}
