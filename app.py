import streamlit as st
import PyPDF2
import re
import json

# === Common Skills List ===
common_skills = {
    'python', 'java', 'c++', 'c', 'html', 'css', 'javascript', 'django', 'flask',
    'react', 'nodejs', 'mysql', 'mongodb', 'rest api', 'git', 'github', 'sql',
    'machine learning', 'deep learning', 'data structures', 'algorithms',
    'data analysis', 'pandas', 'numpy', 'matplotlib', 'tensorflow', 'keras',
    'linux', 'cloud', 'aws', 'azure', 'devops', 'docker', 'kubernetes'
}

# === Extract Text from PDF ===
def extract_text_from_pdf(uploaded_file):
    reader = PyPDF2.PdfReader(uploaded_file)
    text = ''
    for page in reader.pages:
        text += page.extract_text() or ''
    return text.lower()

# === Skill Extraction Function ===
def extract_skills(text, skill_set):
    found = set()
    for skill in skill_set:
        if re.search(r'\b' + re.escape(skill) + r'\b', text):
            found.add(skill)
    return found

# === Streamlit App Starts ===
st.set_page_config(page_title="Skill Gap Analyzer", layout="centered")
st.title("💼 Resume Skill Gap Analyzer + Interview Q&A")

# Upload Resume
resume_file = st.file_uploader("📤 Upload your Resume (PDF)", type=["pdf"])

# Job Description Input
jd_text = st.text_area("📋 Paste the Job Description here (Text only)")

# Dream Company Input
company = st.text_input("🏢 Enter your Dream Company (e.g. tcs, amazon, infosys)").strip().lower()

if resume_file and jd_text:
    resume_text = extract_text_from_pdf(resume_file)
    resume_skills = extract_skills(resume_text, common_skills)
    jd_skills = extract_skills(jd_text.lower(), common_skills)

    # Skill Gap & Match %
    missing_skills = jd_skills - resume_skills
    match_percent = round((len(resume_skills & jd_skills) / len(jd_skills)) * 100, 2) if jd_skills else 0

    # Display Result
    st.subheader("📊 Skill Gap Report")
    st.write("✅ Skills in Resume:", resume_skills)
    st.write("📌 Skills from JD:", jd_skills)
    st.write("❌ Missing Skills:", missing_skills)
    st.success(f"🎯 Match Percentage: {match_percent}%")

    # Load Company Questions
    try:
        with open("company_coding_questions.json", "r") as f:
            company_data = json.load(f)
        top_questions = company_data.get(company, [])[:10]

        st.subheader(f"💡 Top 10 Interview Questions - {company.title()}")
        if top_questions:
            for i, q in enumerate(top_questions, 1):
                st.markdown(f"**{i}.** {q}")
        else:
            st.warning("⚠️ No questions found for this company.")
    except FileNotFoundError:
        st.error("❌ JSON file not found. Please add 'company_coding_questions.json' in the folder.")

elif resume_file:
    st.warning("📋 Please paste Job Description text.")
elif jd_text:
    st.warning("📤 Please upload your resume (PDF).")
