import streamlit as st
from skill_extractor import extract_skills_from_resume
from jd_parser import extract_skills_from_jd
from visualization import plot_skill_comparison, display_cards, display_loading
import json
import os

st.set_page_config(page_title="Resume Skill Gap Analyzer", layout="wide")

# Load CSS styling
def load_css():
    css_path = os.path.join("assets", "styles.css")
    if os.path.exists(css_path):
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    else:
        st.warning("CSS file not found at 'assets/styles.css'")

# Load coding questions for selected company
def load_company_questions(company_name):
    with open("company_coding_questions.json", "r") as file:
        data = json.load(file)
    return data.get(company_name.lower(), [])

def main():
    load_css()
    st.markdown("<h1 class='header'>Resume Skill Gap Analyzer</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subheader'>Upload your resume and job description to compare your skills and see what's missing.</p>", unsafe_allow_html=True)

    resume_file = st.file_uploader("Upload Resume (PDF or DOCX)", type=["pdf", "docx"])
    jd_text = st.text_area("Paste Job Description")

    if st.button("Analyze") and resume_file and jd_text:
        display_loading()

        resume_skills = extract_skills_from_resume(resume_file)
        jd_skills = extract_skills_from_jd(jd_text)

        matched_skills = resume_skills & jd_skills
        missing_skills = jd_skills - resume_skills

        # Display visual and textual output
        plot_skill_comparison(resume_skills, jd_skills)
        display_cards("Matched Skills", matched_skills, "#d4edda")
        display_cards("Missing Skills", missing_skills, "#f8d7da")

        company = st.text_input("Enter Target Company (Optional):")
        if company:
            questions = load_company_questions(company)
            display_cards(f"Top Interview Questions for {company.title()}", questions[:5], "#e2e3ff")

if __name__ == "__main__":
    main()
