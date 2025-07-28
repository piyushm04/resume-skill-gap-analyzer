import streamlit as st
import PyPDF2
import json
import re
import requests
from datetime import datetime
from streamlit_lottie import st_lottie

# Page config
st.set_page_config(page_title="Resume Skill Gap Analyzer", layout="wide")

# Load Lottie Animation
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_resume = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_jcikwtux.json")

if lottie_resume:
    st_lottie(lottie_resume, speed=1, height=250, key="resume")

# Title and Subtitle
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>📊 Resume Skill Gap Analyzer</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: gray;'>Upload your resume and enter a job description to find missing skills and top company questions</h4>", unsafe_allow_html=True)

# Extract text from PDF
def extract_text_from_pdf(uploaded_file):
    reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# Extract skills
def extract_skills(text, skill_set):
    found = set()
    text = text.lower()
    for skill in skill_set:
        pattern = r'\b' + re.escape(skill.lower()) + r'\b'
        if re.search(pattern, text):
            found.add(skill)
    return found

# Load skills and company questions
all_skills = {'python', 'java', 'c', 'c++', 'sql', 'mysql', 'html', 'css', 'javascript', 'react', 'nodejs', 'git', 'github', 'pandas', 'numpy', 'data analysis', 'machine learning', 'mongodb'}

with open("company_coding_questions.json", "r") as f:
    company_data = json.load(f)

# Upload Resume
uploaded_file = st.file_uploader("📄 Upload your Resume (PDF format)", type="pdf")

# Job Description
job_description = st.text_area("📝 Paste the Job Description")

# Company Name
company = st.text_input("🏢 Enter the Company Name (e.g., Google, Amazon)")

if uploaded_file and job_description:
    resume_text = extract_text_from_pdf(uploaded_file)
    
    skills_in_resume = extract_skills(resume_text, all_skills)
    skills_from_jd = extract_skills(job_description, all_skills)
    
    missing_skills = skills_from_jd - skills_in_resume
    match_percentage = (len(skills_in_resume & skills_from_jd) / len(skills_from_jd)) * 100 if skills_from_jd else 0

    st.markdown("### ✅ Skills in Resume")
    st.write(skills_in_resume)

    st.markdown("### 📌 Skills from Job Description")
    st.write(skills_from_jd)

    st.markdown("### ❌ Missing Skills")
    st.write(missing_skills)

    st.markdown(f"### 🎯 Match Percentage: `{match_percentage:.2f}%`")

    # Top Company Questions
    if company:
        company = company.lower().strip()
        company_questions = company_data.get(company, [])
        
        if company_questions:
            st.markdown(f"### 💻 Top Coding Questions Asked by `{company.capitalize()}`")
            for i, q in enumerate(company_questions[:10], 1):
                st.markdown(f"**{i}. {q}**")
        else:
            st.warning("🚫 No coding questions found for this company. Check the spelling or update the JSON file.")

# Footer
st.markdown("---")
st.markdown(
    f"<div style='text-align: center; color: gray;'>© {datetime.now().year} Resume Skill Gap Analyzer | Built by Piyush Molawade</div>",
    unsafe_allow_html=True
)
