import re

def extract_skills_from_resume(text, skill_set):
    text = text.lower()
    found_skills = set()
    for skill in skill_set:
        pattern = r'\b' + re.escape(skill.lower()) + r'\b'
        if re.search(pattern, text):
            found_skills.add(skill.lower())
    return found_skills
