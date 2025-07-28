import streamlit as st
from skill_extractor import extract_skills_from_resume, extract_skills_from_jd
from jd_parser import extract_job_description
from visualization import plot_skill_match_pie
import json
import os

# Load custom CSS
def load_css():
    css_path = os.path.join("assets", "styles.css")
    if os.path.exists(css_path):
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    else:
        st.warning("Custom CSS file not found.")

# Load top coding questions
def get_top_questions(company):
    try:
        with open("company_coding_questions.json", "r") as file:
            questions = json.load(file)
        return questions.get(company.lower(), ["No questions found for this company."])
    except Exception as e:
        return [f"Error loading questions: {str(e)}"]

# Main Streamlit app
def main():
    st.set_page_config(page_title="Resume Skill Gap Analyzer", layout="wide")
    load_css()
    
    st.title("Resume Skill Gap Analyzer")
    st.write("Upload your resume and paste a job description to analyze the skill gap.")

    resume_file = st.file_uploader("Upload Resume (PDF/Text)", type=["pdf", "txt"])
    job_description = st.text_area("Paste Job Description")

    if st.button("Analyze"):
        if resume_file and job_description:
            with st.spinner("Extracting skills..."):
                resume_skills = extract_skills_from_resume(resume_file)
                jd_skills = extract_skills_from_jd(job_description)

                missing_skills = list(set(jd_skills) - set(resume_skills))
                matched_skills = list(set(jd_skills) & set(resume_skills))

                st.success("Analysis complete!")
                col1, col2 = st.columns(2)

                with col1:
                    st.subheader("Matched Skills")
                    if matched_skills:
                        st.write(", ".join(matched_skills))
                    else:
                        st.write("No matched skills found.")

                with col2:
                    st.subheader("Missing Skills")
                    if missing_skills:
                        st.write(", ".join(missing_skills))
                    else:
                        st.write("No missing skills found.")

                st.subheader("Visual Representation")
                plot_skill_match_pie(len(matched_skills), len(missing_skills))

                st.subheader("Top Coding Questions for Target Company")
                company = st.text_input("Enter Target Company Name")
                if company:
                    top_questions = get_top_questions(company)
                    for q in top_questions:
                        st.markdown(f"- {q}")
        else:
            st.warning("Please upload a resume and paste a job description to proceed.")

if __name__ == "__main__":
    main()
