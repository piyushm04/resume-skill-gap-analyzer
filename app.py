import streamlit as st
from skill_extractor import extract_skills_from_resume, extract_skills_from_jd
from jd_parser import get_top_missing_skills
from visualization import plot_skill_match_pie
import json
import base64
import os

# Load custom CSS
def load_css():
    css_path = os.path.join("assets", "styles.css")
    if os.path.exists(css_path):
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    else:
        st.warning("Custom CSS file not found.")

# Load company questions JSON
def load_company_questions():
    try:
        with open("company_coding_questions.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        st.error("company_coding_questions.json file not found.")
        return {}

# Download button helper
def get_binary_file_downloader_html(bin_file, file_label='File'):
    with open(bin_file, 'rb') as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">Download {file_label}</a>'
    return href

def main():
    st.set_page_config(page_title="Resume Skill Gap Analyzer", layout="wide", page_icon="📄")
    load_css()

    st.title("🎯 Resume Skill Gap Analyzer")
    st.markdown("Compare your resume with job descriptions and get top missing skills + interview questions.")

    uploaded_resume = st.file_uploader("Upload your Resume (PDF or DOCX)", type=["pdf", "docx"])
    jd_text = st.text_area("Paste Job Description here")

    if st.button("Analyze"):
        if uploaded_resume and jd_text.strip():
            with st.spinner("Extracting skills..."):
                resume_skills = extract_skills_from_resume(uploaded_resume)
                jd_skills = extract_skills_from_jd(jd_text)

            missing_skills = get_top_missing_skills(resume_skills, jd_skills)

            st.subheader("🧠 Skill Comparison")
            col1, col2 = st.columns(2)
            col1.markdown("**Skills in Resume**")
            col1.write(", ".join(resume_skills) or "None Found")

            col2.markdown("**Skills in Job Description**")
            col2.write(", ".join(jd_skills) or "None Found")

            st.subheader("❌ Missing Skills")
            if missing_skills:
                st.write(", ".join(missing_skills))
            else:
                st.success("Great! Your resume covers all major JD skills.")

            st.subheader("📊 Visualization")
            plot_skill_match_pie(resume_skills, jd_skills)

            # Company-based question suggestion
            st.subheader("💡 Most Asked Interview Questions")
            company_questions = load_company_questions()
            for company, questions in company_questions.items():
                if any(skill.lower() in company.lower() for skill in jd_skills):
                    st.markdown(f"**{company}**")
                    for q in questions[:5]:
                        st.markdown(f"- {q}")
        else:
            st.warning("Please upload a resume and paste a job description.")

if __name__ == "__main__":
    main()
