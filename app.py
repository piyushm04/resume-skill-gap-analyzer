import streamlit as st
import PyPDF2
import re
import json

# === Define standard skills ===
common_skills = {
    'python', 'java', 'c++', 'c', 'html', 'css', 'javascript', 'django', 'flask',
    'react', 'nodejs', 'mysql', 'mongodb', 'rest api', 'git', 'github', 'sql',
    'machine learning', 'deep learning', 'data structures', 'algorithms',
    'data analysis', 'pandas', 'numpy', 'matplotlib', 'tensorflow', 'keras',
    'linux', 'cloud', 'aws', 'azure', 'devops', 'docker', 'kubernetes'
}

# === Extract text from PDF ===
def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ''
    for page in reader.pages:
        text += page.extract_text() or ''
    return text.lower()

# === Extract relevant skills from text ===
def extract_skills(text, skill_set):
    found = set()
    for skill in skill_set:
        if re.search(r'\b' + re.escape(skill) + r'\b', text):
            found.add(skill)
    return found

# === Streamlit UI ===
st.title("📄 Resume Skill Gap Analyzer")
st.write("Upload your resume and paste a job description to find missing skills and view company questions.")

# === Upload Resume ===
resume_pdf = st.file_uploader("📤 Upload Resume (PDF)", type="pdf")

if resume_pdf:
    resume_text = extract_text_from_pdf(resume_pdf)
    resume_skills = extract_skills(resume_text, common_skills)

    # === Job Description input ===
    jd_text = st.text_area("📋 Paste Job Description Here:")
    if jd_text:
        jd_text = jd_text.lower()
        jd_skills = extract_skills(jd_text, common_skills)

        # === Calculate gap ===
        missing_skills = jd_skills - resume_skills
        match_percent = round((len(resume_skills & jd_skills) / len(jd_skills)) * 100, 2) if jd_skills else 0

        # === Select company ===
        company = st.text_input("🏢 Enter Target Company (e.g., amazon, tcs)").strip().lower()

        if company:
            try:
                with open("company_coding_questions.json", "r") as f:
                    company_data = json.load(f)

                st.write("📁 Available companies:", list(company_data.keys()))

                top_questions = company_data.get(company, [])

                # === Show Report ===
                st.subheader("📊 Skill Gap Report")
                st.markdown(f"✅ **Skills in Resume**: {', '.join(sorted(resume_skills)) or 'None'}")
                st.markdown(f"📌 **Skills from JD**: {', '.join(sorted(jd_skills)) or 'None'}")
                st.markdown(f"❌ **Missing Skills**: {', '.join(sorted(missing_skills)) or 'None'}")
                st.markdown(f"🎯 **Match Percentage**: `{match_percent}%`")

                st.subheader(f"💡 Top Questions Asked in {company.title()}")
                if top_questions:
                    for i, q in enumerate(top_questions[:10], 1):
                        st.markdown(f"**{i}.** {q}")
                else:
                    st.warning(f"No questions found for '{company}'. Please check the spelling.")
            except FileNotFoundError:
                st.error("company_coding_questions.json file not found. Please upload it.")
