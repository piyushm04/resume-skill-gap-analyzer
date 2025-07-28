import docx2txt
from PyPDF2 import PdfReader
import re

# Sample skill keywords – you can replace or expand this list as needed
COMMON_SKILLS = {
    'python', 'java', 'c++', 'html', 'css', 'javascript', 'sql',
    'machine learning', 'deep learning', 'data analysis', 'tensorflow',
    'pandas', 'numpy', 'react', 'node.js', 'django', 'flask',
    'git', 'linux', 'docker', 'kubernetes', 'aws', 'azure',
    'communication', 'teamwork', 'problem-solving'
}


def extract_text_from_pdf(file):
    text = ""
    try:
        reader = PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() or ""
    except Exception as e:
        print("Error reading PDF:", e)
    return text


def extract_text_from_docx(file):
    try:
        return docx2txt.process(file)
    except Exception as e:
        print("Error reading DOCX:", e)
        return ""


def clean_and_tokenize(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    tokens = set(text.split())
    return tokens


def extract_skills_from_resume(file):
    if file.name.endswith(".pdf"):
        text = extract_text_from_pdf(file)
    elif file.name.endswith(".docx"):
        text = extract_text_from_docx(file)
    else:
        return set()

    tokens = clean_and_tokenize(text)
    matched_skills = {skill for skill in COMMON_SKILLS if any(word in tokens for word in skill.split())}
    return matched_skills


def extract_skills_from_jd(jd_text):
    jd_text = jd_text.lower()
    jd_text = re.sub(r'[^a-zA-Z\s]', '', jd_text)
    tokens = set(jd_text.split())
    matched_skills = {skill for skill in COMMON_SKILLS if any(word in tokens for word in skill.split())}
    return matched_skills
