import os
import glob

def get_skills_dir() -> str:
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_dir, "skills")

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
