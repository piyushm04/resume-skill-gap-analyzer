import streamlit as st
import json
import time
from skill_extractor import extract_skills_from_resume
from jd_parser import extract_skills_from_jd, parse_job_description
from visualization import plot_skill_match_pie
from streamlit_lottie import st_lottie


# Load Lottie animation
def load_lottie_animation(path: str):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception:
        return None

# Custom CSS
def load_css():
    with open("assets/styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# Load animation
lottie_resume = load_lottie_animation("assets/animations.json")

# Sidebar
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Resume Skill Gap Analyzer", "About"])

if page == "Resume Skill Gap Analyzer":
    st_lottie(lottie_resume, speed=1, height=200, key="intro")

    st.title("🔍 Resume Skill Gap Analyzer")
    st.markdown("This tool compares your **resume** with a **job description** and shows missing skills.")

    uploaded_resume = st.file_uploader("Upload your Resume (PDF)", type=["pdf"])
    job_description_input = st.text_area("Paste the Job Description here")

    company_name = st.text_input("Enter Target Company Name (e.g., Google)")

    if st.button("Analyze"):
        if not uploaded_resume or not job_description_input:
            st.error("Please upload a resume and enter the job description.")
        else:
            with st.spinner("Analyzing your resume and job description..."):
                time.sleep(2)  # Simulate loading

                resume_text = extract_skills_from_resume(uploaded_resume)
                jd_text = parse_job_description(job_description_input)

                resume_skills = set(resume_text)
                jd_skills = set(extract_skills_from_jd(jd_text))

                matched = resume_skills.intersection(jd_skills)
                missing = jd_skills - resume_skills
                match_percentage = round((len(matched) / len(jd_skills)) * 100, 2) if jd_skills else 0

                # Skill Match Summary
                st.subheader("Skill Match Summary")
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**Skills in Resume:**")
                    st.write(", ".join(sorted(resume_skills)))
                with col2:
                    st.markdown("**Skills in JD:**")
                    st.write(", ".join(sorted(jd_skills)))

                st.markdown("**Missing Skills:**")
                st.error(", ".join(sorted(missing)) if missing else "None")

                st.markdown(f"**Match Percentage:** `{match_percentage}%`")

                # Visualization
                st.subheader("Visual Analysis")
                plot_skill_match_pie(len(matched), len(missing))

                # Load company-specific questions
                try:
                    with open("company_coding_questions.json") as f:
                        company_data = json.load(f)
                    top_questions = company_data.get(company_name.lower(), [])[:5]
                except Exception:
                    top_questions = []

                if top_questions:
                    st.subheader(f"Top Coding Questions at {company_name.title()}")
                    for i, q in enumerate(top_questions, 1):
                        st.markdown(f"**{i}.** {q}")
                else:
                    st.info("No coding questions found for the entered company.")

elif page == "About":
    st.title("About this Project")
    st.markdown("""
    **Resume Skill Gap Analyzer** helps job applicants identify the missing skills 
    by comparing their resume against a job description. 

    It also suggests the most frequently asked coding questions for the target company.

    💻 Built with **Streamlit** | 🎨 Designed for clarity and professionalism.
    """)

# Footer
st.markdown("""
    <hr style='border:1px solid #555;'/>
    <div style='text-align: center; color: gray; font-size: 14px;'>
        &copy; 2025 Resume Skill Gap Analyzer | Designed by Piyush M.
    </div>
""", unsafe_allow_html=True)
