import streamlit as st
import json
import os

from resume_skill_gap_analyzer.skill_extractor import extract_skills_from_resume, extract_skills_from_jd
from resume_skill_gap_analyzer.jd_parser import get_top_missing_skills
from resume_skill_gap_analyzer.visualization import plot_skill_match_pie

def load_css():
    css_path = os.path.join("assets", "styles.css")
    if os.path.exists(css_path):
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    else:
        st.warning("⚠️ styles.css not found in assets/ folder!")

def load_company_questions():
    file_path = "company_coding_questions.json"
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return json.load(f)
    else:
        st.error("company_coding_questions.json not found.")
        return {}

def main():
    st.set_page_config(page_title="Resume Skill Gap Analyzer", layout="wide", page_icon="🧠")
    load_css()

    st.title("🧠 Resume Skill Gap Analyzer")
    st.markdown("Compare your resume with a job description and find skill gaps.")

    resume_text = st.text_area("Paste your Resume Text here:", height=250)
    jd_text = st.text_area("Paste the Job Description here:", height=250)

    company_questions = load_company_questions()
    selected_company = st.selectbox("Select a Company (for top 5 coding questions):", ["None"] + list(company_questions.keys()))

    if st.button("Analyze Skill Gap"):
        if not resume_text.strip() or not jd_text.strip():
            st.error("Please enter both resume and job description text.")
            return

        resume_skills = extract_skills_from_resume(resume_text)
        jd_skills = extract_skills_from_jd(jd_text)

        matched_skills = list(set(resume_skills) & set(jd_skills))
        missing_skills = list(set(jd_skills) - set(resume_skills))

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("✅ Skills in your Resume")
            st.write(matched_skills if matched_skills else "No matched skills found.")

        with col2:
            st.subheader("❌ Missing Skills")
            st.write(missing_skills if missing_skills else "No missing skills.")

        st.subheader("📊 Skill Match Visualization")
        st.pyplot(plot_skill_match_pie(len(matched_skills), len(missing_skills)))

        if selected_company != "None":
            st.subheader(f"💡 Top 5 Coding Questions Asked by {selected_company}")
            questions = company_questions.get(selected_company, [])
            if questions:
                for idx, q in enumerate(questions[:5], 1):
                    st.markdown(f"**{idx}.** {q}")
            else:
                st.info("No questions found for this company.")

if __name__ == "__main__":
    main()
