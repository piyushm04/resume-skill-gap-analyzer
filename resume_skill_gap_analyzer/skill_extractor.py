import docx2txt
import PyPDF2
import io
import re

def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() or ""
    return text

def extract_text_from_docx(file):
    return docx2txt.process(file)

def clean_text(text):
    # Remove special characters, digits, extra spaces
    text = re.sub(r"[^a-zA-Z\s]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.lower()

def extract_skills_from_resume(resume_file):
    if resume_file.name.endswith(".pdf"):
        raw_text = extract_text_from_pdf(resume_file)
    elif resume_file.name.endswith(".docx"):
        raw_text = extract_text_from_docx(resume_file)
    else:
        return set()

    cleaned = clean_text(raw_text)
    return extract_skills_from_text(cleaned)

def extract_skills_from_text(text):
    # Simple predefined skill set
    predefined_skills = {
        "python", "java", "c", "c++", "html", "css", "javascript",
        "sql", "mysql", "mongodb", "react", "node.js", "git", "linux",
        "machine learning", "deep learning", "data analysis", "django", "flask"
    }

    found = set()
    for skill in predefined_skills:
        if skill in text:
            found.add(skill)
    return found

def extract_skills_from_jd(jd_text):
    cleaned = clean_text(jd_text)
    return extract_skills_from_text(cleaned)
