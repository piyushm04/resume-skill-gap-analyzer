import streamlit as st
import base64
import json
from PyPDF2 import PdfReader
from skill_extractor import extract_skills_from_resume, extract_skills_from_jd
from jd_parser import get_top_missing_skills
from visualization import plot_skill_match_pie

# Load custom CSS
def load_css():
    with open("assets/styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Load company coding questions
def load_company_questions():
    try:
        with open("company_coding_questions.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def get_pdf_text(uploaded_file):
    try:
        reader = PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    except:
        return ""

# Streamlit App
def main():
    load_css()
    st.title("Resume Skill Gap Analyzer")

    st.markdown("Upload your **Resume (PDF)** and paste the **Job Description** below:")

    resume_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
    jd_text = st.text_area("Paste Job Description")

    company_name = st.text_input("Target Company (Optional)")

    if st.button("Analyze") and resume_file and jd_text:
        resume_text = get_pdf_text(resume_file)

        resume_skills = extract_skills_from_resume(resume_text)
        jd_skills = extract_skills_from_jd(jd_text)

        matched_skills = list(set(resume_skills) & set(jd_skills))
        missing_skills = list(set(jd_skills) - set(resume_skills))

        st.subheader("Skill Match Summary")
        st.markdown(f"✅ **Matched Skills ({len(matched_skills)}):** {', '.join(matched_skills)}")
        st.markdown(f"❌ **Missing Skills ({len(missing_skills)}):** {', '.join(missing_skills)}")

        # Plot
        plot_skill_match_pie(len(matched_skills), len(missing_skills))

        # Show top coding questions
        if company_name:
            company_questions = load_company_questions()
            questions = company_questions.get(company_name.strip().lower())
            if questions:
                st.subheader(f"Top Coding Questions Asked by {company_name.title()}")
                for i, q in enumerate(questions[:5], 1):
                    st.markdown(f"**Q{i}:** {q}")
            else:
                st.info("No coding question data available for this company.")
    elif st.button("Analyze"):
        st.error("Please upload a resume and paste a job description.")

if __name__ == "__main__":
    main()
