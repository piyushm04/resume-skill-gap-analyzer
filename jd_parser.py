# jd_parser.py

import re

def clean_text(text):
    """Remove special characters and extra spaces."""
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    return re.sub(r'\s+', ' ', text).strip().lower()

def extract_skills_from_jd(jd_text, known_skills):
    """Extract matching skills from the job description."""
    jd_clean = clean_text(jd_text)
    return {skill for skill in known_skills if skill.lower() in jd_clean}
