import streamlit as st
import PyPDF2
import json
import re

# === Define common skills ===
common_skills = {
    'python', 'java', 'c++', 'c', 'html', 'css', 'javascript', 'django', 'flask',
    'react', 'nodejs', 'mysql', 'mongodb', 'rest api', 'git', 'github', 'sql',
    'machine learning', 'deep learning', 'data structures', 'algorithms',
    'data analysis', 'pandas', 'numpy', 'matplotlib', 'tensorflow', 'keras',
    'linux', 'cloud', 'aws', 'azure', 'devops', 'docker', 'kubernetes'
}

# === Function to extract text from uploaded PDF ===
def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ''
    for page in reader.pages:
        text += page.extract_text() or ''
    return text.lower()

# === Function to extract skills from text ===
def extract_skills(text, skill_set):
    found = set()
    for skill in skill_set:
        if re.search(r'\b' + re.escape(skill) + r'\b', text):
            found.add(skill)
    return found

# === Streamlit UI ===
st.set_page_config(page_title="Resume Skill Gap Analyzer", layout="centered")
st.title("🧠 Resume Skill Gap Analyzer")

# === Resume Upload ===
st.subheader("📤 Upload Your Resume (PDF)")
resume_file = st.file_uploader("Choose a PDF file", type=["pdf"])

if resume_file:
    resume_text = extract_text_from_pdf(resume_file)
    resume_skills = extract_skills(resume_text, common_skills)

    # === Job Description Input ===
    st.subheader("📋 Paste the Job Description")
    jd_text = st.text_area("Enter job description here:")

    if jd_text:
        jd_text = jd_text.lower()
        jd_skills = extract_skills(jd_text, common_skills)

        # === Skill Analysis ===
        missing_skills = jd_skills - resume_skills
        match_percent = round((len(resume_skills & jd_skills) / len(jd_skills)) * 100, 2) if jd_skills else 0

        st.markdown("### 📊 Skill Gap Report")
        st.write("✅ Skills in Resume:", resume_skills)
        st.write("📌 Skills from JD:", jd_skills)
        st.write("❌ Missing Skills:", missing_skills)
        st.write(f"🎯 Match Percentage: **{match_percent}%**")

        # === Ask for dream company ===
        st.subheader("🏢 Enter Your Dream Company")
        company = st.text_input("E.g., amazon, tcs, infosys").strip().lower()

        if company:
            try:
                with open("company_coding_questions.json", "r") as f:
                    company_data = json.load(f)

                if company in company_data:
                    top_questions = company_data[company]
                    st.subheader(f"💡 Top Questions Asked in {company.title()}")
                    for i, q in enumerate(top_questions[:10], 1):
                        st.markdown(f"**{i}.** {q}")
                else:
                    st.warning(f"No questions found for '{company}'. Try one of: {', '.join(company_data.keys())}")

            except FileNotFoundError:
                st.error("📁 JSON file with company questions not found.")
