import streamlit as st
import PyPDF2
import re
import json
import matplotlib.pyplot as plt
from io import BytesIO

# === Load skills ===
common_skills = {
    'python', 'java', 'c++', 'c', 'html', 'css', 'javascript', 'django', 'flask',
    'react', 'nodejs', 'mysql', 'mongodb', 'rest api', 'git', 'github', 'sql',
    'machine learning', 'deep learning', 'data structures', 'algorithms',
    'data analysis', 'pandas', 'numpy', 'matplotlib', 'tensorflow', 'keras',
    'linux', 'cloud', 'aws', 'azure', 'devops', 'docker', 'kubernetes'
}

# === Skill extraction ===
def extract_text_from_pdf(uploaded_file):
    reader = PyPDF2.PdfReader(uploaded_file)
    text = ''
    for page in reader.pages:
        text += page.extract_text() or ''
    return text.lower()

def extract_skills(text, skill_set):
    return {skill for skill in skill_set if re.search(r'\b' + re.escape(skill) + r'\b', text)}

# === Streamlit UI ===
st.set_page_config(page_title="Resume Skill Gap Analyzer", layout="wide")
st.title("📄 Resume Skill Gap Analyzer")
st.markdown("Upload your resume PDF and paste the job description to find missing skills and top company questions.")

# === Upload resume ===
st.subheader("📤 Upload Your Resume (PDF)")
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file:
    resume_text = extract_text_from_pdf(uploaded_file)
    resume_skills = extract_skills(resume_text, common_skills)

    st.success("✅ Resume uploaded and processed successfully!")
    st.markdown("---")

    # === JD input ===
    st.subheader("📋 Paste the Job Description")
    jd_text = st.text_area("Enter the job description here")
    if jd_text:
        jd_text = jd_text.lower()
        jd_skills = extract_skills(jd_text, common_skills)

        missing_skills = jd_skills - resume_skills
        match_percent = round((len(resume_skills & jd_skills) / len(jd_skills)) * 100, 2) if jd_skills else 0

        # === Visualization ===
        st.subheader("📊 Skill Match Visualization")
        fig, ax = plt.subplots()
        ax.pie([len(resume_skills & jd_skills), len(missing_skills)],
               labels=["Matched Skills", "Missing Skills"],
               autopct='%1.1f%%',
               colors=['#4CAF50', '#FF5722'],
               startangle=90)
        st.pyplot(fig)

        st.bar_chart({
            "Skills": ["Matched", "Missing"],
            "Count": [len(resume_skills & jd_skills), len(missing_skills)]
        })

        # === Report ===
        st.markdown("---")
        st.subheader("📑 Skill Gap Report")
        st.markdown(f"🎯 **Match Percentage**: `{match_percent}%`")
        st.markdown(f"✅ **Resume Skills:** `{', '.join(sorted(resume_skills))}`")
        st.markdown(f"📌 **JD Required Skills:** `{', '.join(sorted(jd_skills))}`")
        st.markdown(f"❌ **Missing Skills:** `{', '.join(sorted(missing_skills))}`")

        # === Company Questions ===
        st.markdown("---")
        st.subheader("🏢 Top Coding Questions by Company")
        company = st.text_input("Enter your dream company (e.g., amazon, tcs, google)").strip().lower()

        if company:
            try:
                with open("company_coding_questions.json", "r") as f:
                    company_data = json.load(f)

                top_questions = company_data.get(company, [])
                if top_questions:
                    st.success(f"💡 Top {len(top_questions)} Questions Asked at {company.title()}:")
                    for i, q in enumerate(top_questions[:10], 1):
                        st.markdown(f"**{i}.** {q}")
                else:
                    st.warning("⚠️ No questions available for this company.")
            except Exception as e:
                st.error("❌ Error loading company questions JSON.")
    else:
        st.info("ℹ️ Please enter the job description above.")

else:
    st.info("📎 Please upload a PDF resume file to continue.")
