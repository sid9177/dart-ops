import os
from app.helix_agent.tools import list_skills, read_skill, get_skills_dir

def test_list_skills():
    skills = list_skills()
    assert "Available skills" in skills or "No skills" in skills
    
def test_read_skill():
    # Write a dummy skill to test reading
    test_skill_path = os.path.join(get_skills_dir(), "test_skill.md")
    with open(test_skill_path, "w", encoding="utf-8") as f:
        f.write("This is a test skill.")
        
    try:
        content = read_skill("test_skill")
        assert "This is a test skill." in content
        
        content_with_ext = read_skill("test_skill.md")
        assert "This is a test skill." in content_with_ext
    finally:
        if os.path.exists(test_skill_path):
            os.remove(test_skill_path)

def test_read_nonexistent_skill():
    content = read_skill("does_not_exist.md")
    assert "Error: Skill" in content
