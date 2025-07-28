import streamlit as st
import json
from skill_extractor import extract_skills_from_resume, extract_skills_from_jd
from jd_parser import extract_job_description
from visualization import plot_skill_match_pie


def main():
    st.set_page_config(page_title="Resume Skill Gap Analyzer", layout="wide")
    st.title("Resume Skill Gap Analyzer")

    # Upload resume
    resume_file = st.file_uploader("Upload your resume (PDF or DOCX)", type=["pdf", "docx"])

    # Job description input
    job_description_text = st.text_area("Paste the Job Description")

    # Load coding question data once
    try:
        with open("company_coding_questions.json", "r") as f:
            question_data = json.load(f)
        company_list = sorted(question_data.keys())
    except:
        question_data = {}
        company_list = []

    # Dropdown to select target company
    selected_company = st.selectbox("Select Targeted Company", company_list)

    if st.button("Analyze"):
        if resume_file is not None and job_description_text.strip():
            # Extract skills
            resume_skills = extract_skills_from_resume(resume_file)
            jd_skills = extract_skills_from_jd(job_description_text)

            matched_skills = list(set(resume_skills) & set(jd_skills))
            missing_skills = list(set(jd_skills) - set(resume_skills))

            # SECTION 1 — Show Coding Questions First
            st.subheader(f"Top Coding Questions Asked in {selected_company}")
            questions = question_data.get(selected_company)
            if questions:
                for i, q in enumerate(questions[:10], 1):
                    st.markdown(f"**{i}.** {q}")
            else:
                st.info(f"No coding questions found for **{selected_company}**.")

            # SECTION 2 — Show Skill Match
            st.subheader("Skill Match Analysis")
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("**Matched Skills:**")
                if matched_skills:
                    for skill in matched_skills:
                        st.success(skill)
                else:
                    st.warning("No matched skills found.")

            with col2:
                st.markdown("**Missing Skills:**")
                if missing_skills:
                    for skill in missing_skills:
                        st.error(skill)
                else:
                    st.info("No missing skills 🎯")

            # Visualization pie chart
            plot_skill_match_pie(len(matched_skills), len(missing_skills))
        else:
            st.warning("Please upload a resume and enter a job description.")


if __name__ == "__main__":
    main()
