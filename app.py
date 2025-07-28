import streamlit as st
from skill_extractor import extract_skills_from_resume
from jd_parser import extract_skills_from_jd
from visualization import plot_skill_comparison, display_cards
import json

st.set_page_config(page_title="Resume Skill Gap Analyzer", layout="wide")

def load_css():
    with open("assets/styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def load_questions():
    with open("company_coding_questions.json", "r") as file:
        return json.load(file)

def main():
    load_css()
    st.markdown("<h1 class='main-title'>Resume Skill Gap Analyzer</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>Upload your resume and job description to find missing skills and prepare better!</p>", unsafe_allow_html=True)

    resume_file = st.file_uploader("Upload your resume", type=["pdf", "docx"])
    jd_text = st.text_area("Paste the job description here")

    if st.button("Analyze") and resume_file and jd_text:
        with st.spinner("Analyzing..."):
            resume_skills = extract_skills_from_resume(resume_file)
            jd_skills = extract_skills_from_jd(jd_text)

            matched_skills = resume_skills & jd_skills
            missing_skills = jd_skills - resume_skills

            display_cards("Matched Skills", matched_skills, "#d4edda")
            display_cards("Missing Skills", missing_skills, "#f8d7da")
            plot_skill_comparison(resume_skills, jd_skills)

            st.markdown("### 🔍 Top 5 Most Asked Questions by the Company")
            questions_data = load_questions()
            company_name = "default"
            for key in questions_data:
                if key.lower() in jd_text.lower():
                    company_name = key
                    break
            questions = questions_data.get(company_name, [])[:5]
            for i, q in enumerate(questions, 1):
                st.markdown(f"**{i}. {q}**")

if __name__ == "__main__":
    main()