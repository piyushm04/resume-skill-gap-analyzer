import streamlit as st
from resume_skill_gap_analyzer.skill_extractor import extract_skills_from_resume, extract_skills_from_jd

from jd_parser import get_top_missing_skills
from visualization import plot_skill_match_pie
import json
import base64

# Load CSS
def load_css():
    with open("assets/style.css") as f:  # Corrected the file name
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Load animation (optional for UI enhancement)
def load_lottie_animation():
    with open("assets/animations.json", "r") as f:
        return json.load(f)

def main():
    st.set_page_config(page_title="Resume Skill Gap Analyzer", layout="wide")
    load_css()

    st.markdown("<h1 class='title'>Resume Skill Gap Analyzer</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>Compare your resume against the job description and improve your chances.</p>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        resume_file = st.file_uploader("Upload Your Resume (PDF or DOCX)", type=["pdf", "docx"])
    with col2:
        jd_text = st.text_area("Paste Job Description Here")

    if resume_file and jd_text:
        resume_skills = extract_skills_from_resume(resume_file)
        jd_skills = extract_skills_from_jd(jd_text)

        missing_skills = list(set(jd_skills) - set(resume_skills))

        st.subheader("Skills in Resume:")
        st.write(", ".join(resume_skills) if resume_skills else "No skills found.")

        st.subheader("Skills in Job Description:")
        st.write(", ".join(jd_skills) if jd_skills else "No skills found.")

        st.subheader("Missing Skills:")
        if missing_skills:
            st.error(", ".join(missing_skills))
        else:
            st.success("Great! Your resume matches all required skills.")

        st.subheader("Skill Match Overview:")
        plot_skill_match_pie(resume_skills, jd_skills)

        st.subheader("Top 5 Coding Questions from Target Company:")
        company_name = get_company_from_jd(jd_text)
        questions = get_top_missing_skills(company_name)
        if questions:
            for i, q in enumerate(questions, 1):
                st.markdown(f"**Q{i}.** {q}")
        else:
            st.info("No questions found for this company.")

def get_company_from_jd(jd_text):
    lines = jd_text.lower().splitlines()
    for line in lines:
        if "company" in line or "organization" in line:
            words = line.strip().split()
            return words[-1].capitalize()
    return "Unknown"

if __name__ == "__main__":
    main()
