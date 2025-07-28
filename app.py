import streamlit as st
import json
import os
from skill_extractor import extract_skills_from_resume, extract_skills_from_jd
from jd_parser import parse_job_description
from visualization import plot_skill_comparison, display_cards, display_loading

# Load and apply custom CSS
def load_css():
    css_path = "assets/styles.css"
    if os.path.exists(css_path):
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    else:
        st.warning("⚠️ 'styles.css' not found in assets folder.")

# Load company coding questions
def load_questions():
    with open("company_coding_questions.json") as f:
        return json.load(f)

# Main logic
def main():
    st.set_page_config(page_title="Resume Skill Gap Analyzer", layout="wide")
    load_css()

    # --- Navigation Bar ---
    st.markdown("""
    <nav class="navbar">
        <div class="nav-container">
            <h2 class="nav-title">Resume Skill Gap Analyzer</h2>
        </div>
    </nav>
    """, unsafe_allow_html=True)

    st.markdown("### 📄 Upload Your Resume (in .docx format)")
    resume_file = st.file_uploader("Upload your resume", type=["docx"])

    st.markdown("### 💼 Paste Job Description")
    job_desc_input = st.text_area("Paste the job description here...", height=200)

    if st.button("Analyze"):
        if resume_file and job_desc_input:
            display_loading()

            # Extract skills
            resume_skills = extract_skills_from_resume(resume_file)
            parsed_jd = parse_job_description(job_desc_input)
            jd_skills = extract_skills_from_jd(parsed_jd)

            # Visualizations
            plot_skill_comparison(resume_skills, jd_skills)

            # Display skills
            matched = resume_skills & jd_skills
            missing = jd_skills - resume_skills

            display_cards("✅ Skills in Resume & JD", matched, "#d4edda")
            display_cards("❌ Missing Skills (Important to Learn)", missing, "#f8d7da")

            # Show most asked questions
            st.markdown("### 💡 Top Coding Questions Asked by the Company")
            questions_data = load_questions()

            for company, questions in questions_data.items():
                if company.lower() in job_desc_input.lower():
                    for q in questions[:5]:
                        st.markdown(f"• {q}")
                    break
        else:
            st.warning("Please upload a resume and enter a job description.")

# Run the app
if __name__ == "__main__":
    main()
