import streamlit as st
import PyPDF2
import re
import json
import matplotlib.pyplot as plt
from streamlit_lottie import st_lottie
import requests

# ========== Custom Styling ==========
st.set_page_config(page_title="Skill Gap Analyzer", layout="wide")

# Apply clean CSS for layout polish
st.markdown("""
    <style>
    .reportview-container {
        background: linear-gradient(to right, #f9f9f9, #e0f7fa);
    }
    .block-container {
        padding: 2rem;
        border-radius: 10px;
    }
    h1, h2, h3 {
        color: #2c3e50;
    }
    </style>
""", unsafe_allow_html=True)

# Load Lottie animation (from URL)
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_resume = load_lottieurl("https://lottie.host/3a87084d-3e14-4d65-82a5-c83e14b68ac1/lijD6uXjKq.json")

# ========== Skill Set ==========
common_skills = {
    'python', 'java', 'c++', 'c', 'html', 'css', 'javascript', 'django', 'flask',
    'react', 'nodejs', 'mysql', 'mongodb', 'rest api', 'git', 'github', 'sql',
    'machine learning', 'deep learning', 'data structures', 'algorithms',
    'data analysis', 'pandas', 'numpy', 'matplotlib', 'tensorflow', 'keras',
    'linux', 'cloud', 'aws', 'azure', 'devops', 'docker', 'kubernetes'
}

# ========== Helper Functions ==========
def extract_text_from_pdf(uploaded_file):
    reader = PyPDF2.PdfReader(uploaded_file)
    text = ''
    for page in reader.pages:
        text += page.extract_text() or ''
    return text.lower()

def extract_skills(text, skill_set):
    return {skill for skill in skill_set if re.search(r'\b' + re.escape(skill) + r'\b', text)}

# ========== UI ==========
st_lottie(lottie_resume, speed=1, height=200, key="intro")

st.title("📄 Resume Skill Gap Analyzer")
st.markdown("Upload your resume, paste the job description, and get a professional skill gap report with top company questions.")

st.markdown("---")
col1, col2 = st.columns(2)

# ========== Upload Resume ==========
with col1:
    st.subheader("📤 Upload Resume (PDF)")
    uploaded_file = st.file_uploader("Choose a file", type="pdf")

# ========== Job Description ==========
with col2:
    st.subheader("📋 Paste Job Description")
    jd_text = st.text_area("Paste here...")

# ========== Process ==========
if uploaded_file and jd_text:
    resume_text = extract_text_from_pdf(uploaded_file)
    resume_skills = extract_skills(resume_text, common_skills)
    jd_text = jd_text.lower()
    jd_skills = extract_skills(jd_text, common_skills)

    missing_skills = jd_skills - resume_skills
    matched_skills = resume_skills & jd_skills
    match_percent = round((len(matched_skills) / len(jd_skills)) * 100, 2) if jd_skills else 0

    st.markdown("---")
    st.subheader("📊 Skill Match Report")

    # === Pie Chart ===
    fig, ax = plt.subplots()
    ax.pie(
        [len(matched_skills), len(missing_skills)],
        labels=["Matched", "Missing"],
        autopct="%1.1f%%",
        colors=["#00C853", "#D50000"]
    )
    st.pyplot(fig)

    # === Skill Sets ===
    st.markdown(f"🎯 **Match Percentage:** `{match_percent}%`")
    st.success(f"✅ **Matched Skills:** {', '.join(sorted(matched_skills))}")
    st.warning(f"❌ **Missing Skills:** {', '.join(sorted(missing_skills))}")
    st.info(f"📌 **All JD Skills:** {', '.join(sorted(jd_skills))}")

    # === Company Questions ===
    st.markdown("---")
    st.subheader("🏢 Top Coding Questions by Company")
    company = st.text_input("Enter Company Name (e.g. amazon, tcs, google)").lower().strip()

    if company:
        try:
            with open("company_coding_questions.json", "r") as f:
                company_data = json.load(f)

            top_questions = company_data.get(company, [])
            if top_questions:
                for i, q in enumerate(top_questions[:10], 1):
                    st.markdown(f"**{i}.** {q}")
            else:
                st.warning("⚠️ No questions found for this company.")
        except:
            st.error("❌ Couldn't load questions.")
else:
    st.info("📎 Upload resume and job description to begin.")
