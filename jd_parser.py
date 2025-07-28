import re

def parse_job_description(text):
    return text.lower()

def extract_skills_from_jd(text, skill_set):
    jd_text = parse_job_description(text)
    found_skills = set()
    for skill in skill_set:
        pattern = r'\b' + re.escape(skill.lower()) + r'\b'
        if re.search(pattern, jd_text):
            found_skills.add(skill.lower())
    return found_skills
