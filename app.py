import streamlit as st
from skill_extractor import extract_skills_from_resume
from jd_parser import extract_skills_from_jd
from visualization import plot_skill_comparison, display_cards, display_loading
import json
import os

# Set page config
st.set_page_config(page_title="Resume Skill Gap Analyzer", layout="wide")

# Load custom CSS
def load_css():
    with open("assets/styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# ------------------ NAVBAR ------------------
st.markdown("""
<div class="navbar">
  <h1>Resume Skill Gap Analyzer</h1>
  <div>
    <a href="#upload-resume">Resume</a>
    <a href="#enter-job-description">Job Description</a>
    <a href="#analysis-results">Results</a>
  </div>
</div>
""", unsafe_allow_html=True)

# ------------------ RESUME UPLOAD ------------------
st.markdown("## 📄 <span id='upload-resume'>Upload Your Resume</span>", unsafe_allow_html=True)
resume_file = st.file_uploader("Upload your resume (.txt or .pdf)", type=["txt", "pdf"])

resume_skills = set()
if resume_file:
    with st.expander("📜 View Extracted Resume Text"):
        st.write(resume_file.read().decode("utf-8", errors="ignore"))
    with st.spinner("Extracting skills from resume..."):
        resume_file.seek(0)
        resume_skills = extract_skills_from_resume(resume_file)

# ------------------ JOB DESCRIPTION ------------------
st.markdown("## 🧾 <span id='enter-job-description'>Enter Job Description</span>", unsafe_allow_html=True)
job_description = st.text_area("Paste the job description here:", height=200)
jd_skills = set()
if job_description:
    with st.spinner("Extracting skills from job description..."):
        jd_skills = extract_skills_from_jd(job_description)

# ------------------ ANALYSIS RESULTS ------------------
st.markdown("## 📊 <span id='analysis-results'>Skill Gap Analysis Results</span>", unsafe_allow_html=True)

if resume_skills and jd_skills:
    matched = resume_skills & jd_skills
    missing = jd_skills - resume_skills

    st.success(f"✅ Skills matched: {len(matched)}")
    st.error(f"❌ Skills missing: {len(missing)}")

    col1, col2 = st.columns(2)
    with col1:
        display_cards("Your Resume Skills", resume_skills, "#1e1e1e")
    with col2:
        display_cards("JD Required Skills", jd_skills, "#1e1e1e")

    plot_skill_comparison(resume_skills, jd_skills)
else:
    st.warning("Please upload both a resume and a job description to see the analysis.")

# ------------------ COMPANY CODING QUESTIONS ------------------
st.markdown("## 💡 Company Specific Questions")

company_name = st.text_input("Enter the target company name:")
if company_name:
    try:
        with open("company_coding_questions.json", "r") as f:
            data = json.load(f)
        questions = data.get(company_name.lower(), [])
        if questions:
            st.info(f"Top {len(questions)} coding questions for {company_name.capitalize()}:")
            for i, q in enumerate(questions[:5], 1):
                st.markdown(f"**{i}.** {q}")
        else:
            st.warning(f"No questions found for {company_name}")
    except FileNotFoundError:
        st.error("Company questions data file not found.")

# ------------------ FOOTER ------------------
st.markdown("""
<div class='footer'>
  Developed with ❤️ by Piyush | Streamlit App | 2025
</div>
""", unsafe_allow_html=True)
