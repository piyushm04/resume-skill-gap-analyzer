import streamlit as st
from skill_extractor import extract_skills_from_resume
from jd_parser import extract_skills_from_jd
from visualization import plot_skill_comparison, display_cards
import json
import base64

# Load external CSS
def load_css():
    try:
        with open("assets/styles.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("⚠️ styles.css not found in assets/ folder")

# Load company-wise coding questions
def load_questions():
    with open("company_coding_questions.json", "r") as file:
        return json.load(file)

# App main function
def main():
    st.set_page_config(page_title="Resume Skill Gap Analyzer", layout="wide")
    load_css()

    st.markdown("<h2 class='title'>Resume Skill Gap Analyzer</h2>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>Upload your resume and a job description to analyze the skill gap.</p>", unsafe_allow_html=True)

    resume_file = st.file_uploader("Upload your Resume (PDF or DOCX)", type=["pdf", "docx"])
    job_desc = st.text_area("Paste Job Description")

    if resume_file and job_desc:
        resume_skills = extract_skills_from_resume(resume_file)
        jd_skills = extract_skills_from_jd(job_desc)

        matched_skills = resume_skills & jd_skills
        missing_skills = jd_skills - resume_skills

        # Display results
        plot_skill_comparison(resume_skills, jd_skills)
        display_cards("Matched Skills", matched_skills, "#d4edda")
        display_cards("Missing Skills", missing_skills, "#f8d7da")

        # Top 5 coding questions
        st.markdown("### Top Coding Questions from Target Company")
        company_questions = load_questions()

        for company in company_questions:
            if company.lower() in job_desc.lower():
                questions = company_questions[company][:5]
                for q in questions:
                    st.markdown(f"- {q}")
                break
        else:
            st.info("No matching company found for coding questions.")

if __name__ == "__main__":
    main()
