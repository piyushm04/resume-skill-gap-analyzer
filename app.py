import streamlit as st
import PyPDF2
import json
import re
import requests
from datetime import datetime
from streamlit_lottie import st_lottie

# Page Config
st.set_page_config(page_title="Skill Gap Analyzer", layout="wide")

# Load Lottie animation
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_resume = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_jcikwtux.json")

# Custom CSS Styling
st.markdown("""
    <style>
    html, body, [class*="css"]  {
        font-family: 'Segoe UI', sans-serif;
        background-color: #f2f4f8;
    }
    .title {
        color: #0052cc;
        font-size: 45px;
        font-weight: bold;
        text-align: center;
        margin-top: 10px;
    }
    .subtitle {
        text-align: center;
        font-size: 18px;
        color: #555;
        margin-bottom: 30px;
    }
    .section {
        background-color: #ffffff;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 6px 15px rgba(0,0,0,0.05);
        margin-top: 25px;
        margin-bottom: 25px;
    }
    .skill-badge {
        display: inline-block;
        background-color: #e0ffe6;
        color: #1b5e20;
        padding: 6px 12px;
        margin: 4px;
        border-radius: 25px;
        font-size: 14px;
    }
    .footer {
        text-align: center;
        font-size: 14px;
        color: #888;
        margin-top: 50px;
        padding-bottom: 20px;
    }
    hr {
        border-top: 1px solid #ccc;
        margin-top: 50px;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown("<div class='title'>🚀 Resume Skill Gap Analyzer</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Compare your resume with the job description, identify missing skills & ace the interview!</div>", unsafe_allow_html=True)

# Animation
if lottie_resume:
    st_lottie(lottie_resume, speed=1, height=250, key="resume")

# PDF Text Extractor
def extract_text_from_pdf(uploaded_file):
    reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# Skill Extraction Logic
def extract_skills(text, skill_set):
    found = set()
    text = text.lower()
    for skill in skill_set:
        pattern = r'\b' + re.escape(skill.lower()) + r'\b'
        if re.search(pattern, text):
            found.add(skill)
    return found

# Load skills & question bank
with open("company_coding_questions.json", "r") as f:
    company_data = json.load(f)

all_skills = {
    'python', 'java', 'c', 'c++', 'sql', 'mysql', 'html', 'css', 'javascript',
    'react', 'nodejs', 'git', 'github', 'pandas', 'numpy',
    'data analysis', 'machine learning', 'mongodb'
}

# Uploads and Inputs
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        uploaded_file = st.file_uploader("📄 Upload Your Resume (PDF)", type="pdf")
    with col2:
        company = st.text_input("🏢 Target Company (e.g., Google, Infosys, Amazon)")

job_description = st.text_area("📝 Paste Job Description Here", height=200)

# Skill Analysis
if uploaded_file and job_description:
    st.markdown("<div class='section'>", unsafe_allow_html=True)

    resume_text = extract_text_from_pdf(uploaded_file)
    resume_skills = extract_skills(resume_text, all_skills)
    jd_skills = extract_skills(job_description, all_skills)
    missing_skills = jd_skills - resume_skills
    match_percent = (len(resume_skills & jd_skills) / len(jd_skills)) * 100 if jd_skills else 0

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### ✅ Skills Found in Resume")
        st.markdown("<div>" + "".join([f"<span class='skill-badge'>{skill}</span>" for skill in resume_skills]) + "</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("### 📌 Skills Required in JD")
        st.markdown("<div>" + "".join([f"<span class='skill-badge'>{skill}</span>" for skill in jd_skills]) + "</div>", unsafe_allow_html=True)

    st.markdown("### ❌ Missing Skills")
    st.markdown("<div>" + "".join([f"<span class='skill-badge'>{skill}</span>" for skill in missing_skills]) + "</div>", unsafe_allow_html=True)

    st.markdown(f"<h4 style='color: #ff9f1c;'>🎯 Match Percentage: <b>{match_percent:.2f}%</b></h4>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Coding Questions
    if company:
        company = company.lower().strip()
        questions = company_data.get(company, [])
        st.markdown("<div class='section'>", unsafe_allow_html=True)
        st.markdown(f"### 💻 Top 10 Coding Questions for `{company.capitalize()}`")
        if questions:
            for i, q in enumerate(questions[:10], 1):
                st.markdown(f"**{i}. {q}**")
        else:
            st.warning("🚫 No questions found for this company. Check spelling or update the dataset.")
        st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown(f"<div class='footer'>© {datetime.now().year} Resume Skill Gap Analyzer | Designed with 💡 by Piyush Molawade</div>", unsafe_allow_html=True)
