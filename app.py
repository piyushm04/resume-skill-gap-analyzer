import streamlit as st
import json
from skill_extractor import extract_skills_from_resume, extract_skills_from_jd
from jd_parser import parse_job_description
from visualization import plot_skill_comparison, display_cards, display_loading

# Load animation and CSS
def load_css():
    with open("assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def load_animation():
    try:
        with open("assets/animations.json", "r") as f:
            animation_data = json.load(f)
        return animation_data
    except Exception as e:
        st.error("Failed to load animation.")
        return None

# Title & Welcome Modal
def show_welcome_modal(animation_data):
    if "modal_shown" not in st.session_state:
        st.session_state.modal_shown = True
        st.markdown(
            f"""
            <div class="welcome-modal animate">
                <h2>🚀 Welcome to Resume Skill Gap Analyzer</h2>
                <p>Upload your resume and job description to discover your missing skills and prepare better!</p>
            </div>
            """,
            unsafe_allow_html=True
        )

# Main App
def main():
    st.set_page_config(page_title="Resume Skill Gap Analyzer", layout="wide")
    load_css()
    animation_data = load_animation()
    show_welcome_modal(animation_data)

    st.markdown("<h1 class='title'>Resume Skill Gap Analyzer</h1>", unsafe_allow_html=True)
    st.markdown("<p class='description'>Compare your resume with a job description and identify missing skills.</p>", unsafe_allow_html=True)

    resume_file = st.file_uploader("Upload your Resume (.pdf or .docx)", type=["pdf", "docx"])
    job_description = st.text_area("Paste Job Description Here", height=200)

    if st.button("Analyze Skills"):
        if resume_file and job_description:
            display_loading()

            # Extract skills
            resume_skills = extract_skills_from_resume(resume_file)
            jd_skills = extract_skills_from_jd(job_description)

            matched_skills = resume_skills & jd_skills
            missing_skills = jd_skills - resume_skills

            st.subheader("Skill Comparison")
            plot_skill_comparison(resume_skills, jd_skills)

            display_cards("Matched Skills", matched_skills, "#d4edda")
            display_cards("Missing Skills", missing_skills, "#f8d7da")
        else:
            st.warning("Please upload a resume and enter a job description to proceed.")

if __name__ == "__main__":
    main()
