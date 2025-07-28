import matplotlib.pyplot as plt
import streamlit as st

def plot_skill_comparison(resume_skills, jd_skills):
    labels = ['Matched', 'Missing']
    matched = len(resume_skills & jd_skills)
    missing = len(jd_skills - resume_skills)
    sizes = [matched, missing]

    colors = ['#2ecc71', '#e74c3c']
    explode = (0.1, 0)

    fig, ax = plt.subplots()
    ax.pie(sizes, explode=explode, labels=labels, colors=colors,
           autopct='%1.1f%%', shadow=True, startangle=140)
    ax.axis('equal')
    st.pyplot(fig)

def display_cards(title, content_set, color="#f0f0f0"):
    st.markdown(f"""
    <div style='background-color: {color}; padding: 1rem; border-radius: 10px; margin-bottom: 1rem'>
        <h4 style='color: #333'>{title}</h4>
        <p style='color: #000'>{", ".join(content_set) if content_set else "None"}</p>
    </div>
    """, unsafe_allow_html=True)