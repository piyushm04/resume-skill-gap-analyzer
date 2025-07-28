import streamlit as st
import PyPDF2
import json
import re
import requests
from datetime import datetime
from streamlit_lottie import st_lottie

# Page config
st.set_page_config(page_title="Skill Gap Analyzer", layout="wide")

# Load Lottie animation from URL
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_resume = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_jcikwtux.json")

# CSS styling
st.markdown("""
    <style>
    body { font-family: 'Segoe UI', sans-serif; }
    .main { background-color: #f9f9f9; }
    .title {
        font-size: 45px;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-top: 10px;
    }
    .subtitle {
        text-align: center;
        color: #6c757d;
        font-size: 18px;
    }
    .section {
        background-color: #ffffff;
        padding: 25px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        margin-bottom: 30px;
    }
    .footer {
        text-align: center;
        color: #888;
        font-size: 14px;
        margin-top: 40px;
    }
    .skill-badge {
        display: inline-block;
        background-color: #e0f7fa;
        color: #00796b;
        padding: 6px 12px;
        margin: 4px;
        border-radius: 15px;
        font-size: 14px;
    }
    </style>
""", unsafe_allow_html=True)

# Page Header
st.markdown("<div class='title'>📊 Resume Skill Gap Analyzer</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Upload your resume and job description to find missing skills and prepare smartly!</div>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

if lottie_resume:
    st_lottie(lottie_resume, speed=1, height=250, key="resume")

# Function to extract text from PDF
def extract_text_from_pdf(uploaded_file):
    reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# Function to extract skills
def extract_skills(text, skill_set):
    found = set()
    text = text.lower()
    for skill in skill_set:
        pattern = r'\b' + re.escape(skill.lower()) + r'\b'
        if re.search(pattern, text):
            found.add(skill)
    return found

# Load skill and question data
all_skills = {
    'python', 'java', 'c', 'c++', 'sql', 'mysql', 'html', 'css', 'javascript',
    'react', 'nodejs', 'git', 'github', 'pandas', 'numpy',
    'data analysis', 'machine learning', 'mongodb'
}

with open("company_coding_questions.json", "r") as f:
    company_data = json.load(f)

# Input Section
with st.container():
    col1, col2 = st.columns(2)

    with col1:
        uploaded_file = st.file_uploader("📄 Upload your Resume (PDF format)", type="pdf")

    with col2:
        company = st.text_input("🏢 Enter the Company Name (e.g., Google, Amazon)")

    job_description = st.text_area("📝 Paste the Job Description", height=200)

# Skill Analysis
if uploaded_file and job_description:
    st.markdown("<div class='section'>", unsafe_allow_html=True)

    resume_text = extract_text_from_pdf(uploaded_file)
    skills_in_resume = extract_skills(resume_text, all_skills)
    skills_from_jd = extract_skills(job_description, all_skills)

    missing_skills = skills_from_jd - skills_in_resume
    match_percentage = (len(skills_in_resume & skills_from_jd) / len(skills_from_jd)) * 100 if skills_from_jd else 0

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### ✅ Skills in Resume")
        st.markdown("<div>" + "".join([f"<span class='skill-badge'>{skill}</span>" for skill in skills_in_resume]) + "</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("### 📌 Skills from JD")
        st.markdown("<div>" + "".join([f"<span class='skill-badge'>{skill}</span>" for skill in skills_from_jd]) + "</div>", unsafe_allow_html=True)

    st.markdown("### ❌ Missing Skills")
    st.markdown("<div>" + "".join([f"<span class='skill-badge'>{skill}</span>" for skill in missing_skills]) + "</div>", unsafe_allow_html=True)

    st.markdown(f"<h4 style='color: #673ab7;'>🎯 Match Percentage: <b>{match_percentage:.2f}%</b></h4>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # Top Company Questions
    if company:
        company = company.lower().strip()
        company_questions = company_data.get(company, [])

        st.markdown("<div class='section'>", unsafe_allow_html=True)
        st.markdown(f"### 💻 Top 10 Coding Questions Asked by `{company.capitalize()}`")

        if company_questions:
            for i, q in enumerate(company_questions[:10], 1):
                st.markdown(f"**{i}. {q}**")
        else:
            st.warning("🚫 No questions found for this company. Check spelling or update JSON.")

        st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown(f"<div class='footer'>© {datetime.now().year} Resume Skill Gap Analyzer | Built by Piyush Molawade</div>", unsafe_allow_html=True)
