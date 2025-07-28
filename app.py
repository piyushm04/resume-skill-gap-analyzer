import streamlit as st
import json
import time
from streamlit_lottie import st_lottie
from skill_extractor import extract_skills_from_resume, extract_skills_from_jd
from jd_parser import parse_company_from_jd
from visualization import display_skill_match_chart, display_missing_skills_card, display_top_questions_card

# Set page config
st.set_page_config(page_title="Resume Skill Gap Analyzer", layout="wide", initial_sidebar_state="expanded")

# Load custom CSS
with open("assets/styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Load animation
def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

lottie_resume = load_lottiefile("assets/animations.json")

# Header Section
with st.container():
    left, right = st.columns([2, 1])
    with left:
        st.markdown("<h1 class='main-title'>Resume Skill Gap Analyzer</h1>", unsafe_allow_html=True)
        st.markdown("<p class='subtitle'>Compare your resume with any job description and find missing skills instantly.</p>", unsafe_allow_html=True)
    with right:
        st_lottie(lottie_resume, speed=1, height=200, key="intro")

st.markdown("<hr>", unsafe_allow_html=True)

# Upload resume
with st.container():
    st.markdown("<h3 class='section-title'>Upload Your Resume</h3>", unsafe_allow_html=True)
    resume_text = st.text_area("Paste your resume content here:", height=200)

# Enter Job Description
with st.container():
    st.markdown("<h3 class='section-title'>Paste the Job Description</h3>", unsafe_allow_html=True)
    jd_text = st.text_area("Paste the job description here:", height=200)

# Analyze Button
if st.button("Analyze Skill Gap"):
    if not resume_text.strip() or not jd_text.strip():
        st.warning("Please fill in both the resume and job description.")
    else:
        with st.spinner("Analyzing..."):
            time.sleep(2)
            resume_skills = extract_skills_from_resume(resume_text)
            jd_skills = extract_skills_from_jd(jd_text)
            missing_skills = jd_skills - resume_skills
            match_percentage = round(len(resume_skills & jd_skills) / len(jd_skills) * 100, 2) if jd_skills else 0

            # Display results
            display_skill_match_chart(resume_skills, jd_skills)
            display_missing_skills_card(missing_skills, match_percentage)

            # Show top questions
            company = parse_company_from_jd(jd_text)
            try:
                with open("company_coding_questions.json", "r") as f:
                    company_data = json.load(f)
                top_questions = company_data.get(company.lower(), [])[:5]
                if top_questions:
                    display_top_questions_card(top_questions, company)
                else:
                    st.info(f"No coding questions found for company: **{company}**")
            except Exception:
                st.error("Error loading company questions. Please check the JSON file.")

# Footer
st.markdown("""
    <hr>
    <div class='footer'>
        &copy; 2025 Resume Skill Gap Analyzer. All rights reserved.
    </div>
""", unsafe_allow_html=True)
