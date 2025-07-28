from skill_extractor import extract_skills_from_jd

def parse_job_description(jd_text):
    skills = extract_skills_from_jd(jd_text)
    return skills
