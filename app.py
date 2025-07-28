import streamlit as st
import PyPDF2
import json
import re
from io import BytesIO
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Set up the page configuration
st.set_page_config(page_title="Resume Skill Gap Analyzer", layout="wide", initial_sidebar_state="auto")

# Apply custom CSS for dark theme and cards
st.markdown("""
    <style>
        body {
            background-color: #121212;
            color: white;
        }
        .main {
            background-color: #1E1E1E;
            padding: 2rem;
            border-radius: 10px;
        }
        .card {
            background-color: #2E2E2E;
            padding: 1.5rem;
            border-radius: 10px;
            margin-bottom: 1rem;
            box-shadow: 0 0 15px rgba(0,0,0,0.4);
        }
        h1, h2, h3 {
            font-weight: 800;
        }
    </style>
""", unsafe_allow_html=True)

# Title and Description
st.markdown("<h1 style='text-align:center;'>Resume Skill Gap Analyzer</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; font-size:18px;'>Upload your resume and paste the job description to get skill suggestions and check your job readiness.</p>", unsafe_allow_html=True)

# Load skill set
common_skills = ['python', 'java', 'c', 'c++', 'html', 'css', 'javascript', 'sql', 'mysql', 'mongodb',
                 'git', 'github', 'machine learning', 'deep learning', 'data analysis', 'numpy', 'pandas', 'react']

def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text.lower()

def extract_skills(text, skill_set):
    return {skill for skill in skill_set if skill in text.lower()}

def calculate_match_percentage(resume_skills, jd_skills):
    if not jd_skills:
        return 0
    return round((len(resume_skills & jd_skills) / len(jd_skills)) * 100, 2)

# Upload PDF
st.markdown("<div class='card'>", unsafe_allow_html=True)
resume_file = st.file_uploader("Upload your Resume (PDF)", type=['pdf'])

# Paste Job Description
job_description = st.text_area("Paste Job Description Here")

st.markdown("</div>", unsafe_allow_html=True)

# Company question selection
st.markdown("<div class='card'>", unsafe_allow_html=True)
company = st.selectbox("Select Your Dream Company", ["TCS", "Infosys", "Capgemini", "Bently", "Flipkart", "Amazon"])
st.markdown("</div>", unsafe_allow_html=True)

# Analyze Button
if st.button("Analyze Resume"):
    if resume_file and job_description:
        with st.spinner("Analyzing your resume..."):
            resume_text = extract_text_from_pdf(resume_file)
            jd_text = job_description.lower()

            resume_skills = extract_skills(resume_text, common_skills)
            jd_skills = extract_skills(jd_text, common_skills)
            missing_skills = jd_skills - resume_skills
            match_percent = calculate_match_percentage(resume_skills, jd_skills)

            # Display results
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("### Skills in Resume")
            st.write(resume_skills)
            st.markdown("### Skills Required (From JD)")
            st.write(jd_skills)
            st.markdown("### Missing Skills")
            st.write(missing_skills)
            st.markdown(f"### Match Percentage: **{match_percent}%**")
            st.markdown("</div>", unsafe_allow_html=True)

            # Load questions
            try:
                with open('company_coding_questions.json', 'r') as file:
                    company_data = json.load(file)
                top_questions = company_data.get(company.lower(), [])[:10]

                st.markdown("<div class='card'>", unsafe_allow_html=True)
                st.markdown("### Top Interview Questions")
                for i, q in enumerate(top_questions, 1):
                    st.markdown(f"**{i}. {q}**")
                st.markdown("</div>", unsafe_allow_html=True)

            except Exception as e:
                st.error("Could not load questions. Please check the JSON file.")
    else:
        st.warning("Please upload a resume and paste the job description.")

# Footer
st.markdown("""
    <hr style="margin-top: 2rem;"/>
    <p style="text-align:center; color:gray;">© 2025 Resume Skill Gap Analyzer. All rights reserved.</p>
""", unsafe_allow_html=True)
