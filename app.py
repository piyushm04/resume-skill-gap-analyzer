import streamlit as st
from skill_extractor import extract_skills_from_resume
from jd_parser import extract_skills_from_jd
from visualization import plot_skill_match_pie
import json

# Load custom CSS
def load_css():
    with open("assets/styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Load top 5 coding questions for the selected company
def load_company_questions(company):
    try:
        with open("company_coding_questions.json", "r") as file:
            data = json.load(file)
            return data.get(company.lower(), [])
    except Exception as e:
        return []

# Streamlit App Layout
def main():
    st.set_page_config(page_title="Resume Skill Gap Analyzer", layout="wide")
    load_css()

    st.title("Resume Skill Gap Analyzer")
    st.write("Upload your resume and job description to identify missing skills and get company-specific interview questions.")

    col1, col2 = st.columns(2)

    with col1:
        resume_file = st.file_uploader("Upload Resume (.pdf or .docx)", type=["pdf", "docx"])
    with col2:
        jd_text = st.text_area("Paste Job Description Here")

    if resume_file and jd_text:
        resume_skills = extract_skills_from_resume(resume_file)
        jd_skills = extract_skills_from_jd(jd_text)

        missing_skills = list(set(jd_skills) - set(resume_skills))
        matched_skills = list(set(resume_skills) & set(jd_skills))

        st.subheader("🔍 Skill Analysis")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Skills in Resume:**")
            st.write(resume_skills)
            st.markdown("**Missing Skills:**")
            st.write(missing_skills)
        with col2:
            st.markdown("**Skills Required in JD:**")
            st.write(jd_skills)
            st.markdown("**Matched Skills:**")
            st.write(matched_skills)

        st.subheader("📊 Skill Match Visualization")
        plot_skill_match_pie(matched_skills, missing_skills)

        st.subheader("🏢 Company-Specific Interview Questions")
        company = st.text_input("Enter Target Company Name (e.g., Amazon, Google)").strip()
        if company:
            questions = load_company_questions(company)
            if questions:
                st.markdown(f"### Top 5 Interview Questions for {company.title()}:")
                for i, q in enumerate(questions, 1):
                    st.markdown(f"**Q{i}.** {q}")
            else:
                st.warning("No data available for this company.")

if __name__ == "__main__":
    main()
