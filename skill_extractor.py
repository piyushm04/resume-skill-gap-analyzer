import re
import fitz  # PyMuPDF

# Define some generic and technical skills to extract
GENERIC_SKILLS = [
    "communication", "teamwork", "problem-solving", "leadership", "time management",
    "adaptability", "creativity", "interpersonal skills", "critical thinking"
]

TECHNICAL_SKILLS = [
    "python", "java", "c++", "sql", "html", "css", "javascript", "react", "node.js",
    "machine learning", "deep learning", "data analysis", "excel", "power bi", "aws",
    "docker", "kubernetes", "tensorflow", "pytorch", "git", "github"
]

ALL_SKILLS = set(skill.lower() for skill in (GENERIC_SKILLS + TECHNICAL_SKILLS))


# ✅ Extract text from resume file
def extract_text_from_file(file):
    if file.name.endswith(".pdf"):
        doc = fitz.open(stream=file.read(), filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    else:
        return file.read().decode("utf-8")


# ✅ Extract skills from resume text
def extract_skills_from_resume(file):
    text = extract_text_from_file(file)
    text = text.lower()
    found_skills = [skill for skill in ALL_SKILLS if skill in text]
    return list(set(found_skills))


# ✅ Extract skills from job description
def extract_skills_from_jd(jd_text):
    jd_text = jd_text.lower()
    found_skills = [skill for skill in ALL_SKILLS if skill in jd_text]
    return list(set(found_skills))
