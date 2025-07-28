# utils/skill_extractor.py
import re

def extract_skills(text, skill_set):
    text = text.lower()
    extracted = set()
    for skill in skill_set:
        pattern = r'\b' + re.escape(skill.lower()) + r'\b'
        if re.search(pattern, text):
            extracted.add(skill)
    return extracted
