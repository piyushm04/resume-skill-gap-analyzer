import docx2txt
import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_file):
    text = ""
    with fitz.open(stream=pdf_file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

def extract_skills_from_resume(resume_file):
    filename = resume_file.name.lower()

    if filename.endswith(".pdf"):
        text = extract_text_from_pdf(resume_file)
    elif filename.endswith(".docx"):
        text = docx2txt.process(resume_file)
    else:
        return set()

    keywords = {"python", "java", "c++", "sql", "html", "css", "javascript", "aws", "react", "node.js"}
    found_skills = {word for word in keywords if word.lower() in text.lower()}
    return found_skills