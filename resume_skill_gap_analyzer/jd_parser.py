import re

def parse_job_description(jd_text):
    """Basic cleanup and standardization of JD text."""
    jd_text = jd_text.lower()
    jd_text = re.sub(r'[^\w\s]', '', jd_text)  # Remove punctuation
    return jd_text

def extract_skills_from_jd(jd_text):
    # A simple static list of possible skills (for demonstration)
    skill_keywords = [
        'python', 'java', 'c++', 'html', 'css', 'javascript',
        'sql', 'machine learning', 'deep learning', 'nlp',
        'react', 'nodejs', 'mongodb', 'git', 'docker', 'kubernetes',
        'data analysis', 'excel', 'pandas', 'numpy', 'tensorflow',
        'pytorch', 'flask', 'django', 'api', 'linux', 'cloud', 'aws',
        'azure', 'problem solving', 'oop'
    ]
    
    jd_text = parse_job_description(jd_text)
    extracted_skills = {skill for skill in skill_keywords if skill in jd_text}
    return extracted_skills
