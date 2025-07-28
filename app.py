import streamlit as st
from skill_extractor import extract_skills_from_resume, extract_skills_from_jd
from jd_parser import parse_company_from_jd, load_company_questions
from visualization import plot_skill_comparison, display_cards, display_loading
import base64

def load_css():
    with open("../assets/styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def main():
    st.set_page_config(page_title="Resume Skill Gap Analyzer", layout="centered")
    load_css()

    st.markdown("<h1 class='title'>Resume Skill Gap Analyzer</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>Compare your resume with the job description and find missing skills!</p>", unsafe_allow_html=True)

    resume_file = st.file_uploader("Upload your Resume (PDF or DOCX)", type=["pdf", "docx"])
    jd_text = st.text_area("Paste the Job Description here", height=250)

    if st.button("Analyze"):
        if not resume_file or not jd_text.strip():
            st.error("Please upload a resume and paste a job description.")
            return

        display_loading()

        resume_skills = extract_skills_from_resume(resume_file)
        jd_skills = extract_skills_from_jd(jd_text)

        matched_skills = resume_skills & jd_skills
        missing_skills = jd_skills - resume_skills

        # Skill Match Pie Chart
        plot_skill_comparison(resume_skills, jd_skills)

        # Cards for visual skill output
        display_cards("Skills in Resume", resume_skills, color="#dfe6e9")
        display_cards("Skills in Job Description", jd_skills, color="#b2bec3")
        display_cards("Matched Skills", matched_skills, color="#55efc4")
        display_cards("Missing Skills", missing_skills, color="#fab1a0")

        # Company-specific coding questions
        company = parse_company_from_jd(jd_text)
        if company:
            questions = load_company_questions(company)
            if questions:
                display_cards(f"Top Coding Questions Asked at {company}", questions, color="#ffeaa7")
            else:
                st.info(f"No coding questions found for company: {company}")
        else:
            st.info("Company not detected from job description.")

if __name__ == "__main__":
    main()
