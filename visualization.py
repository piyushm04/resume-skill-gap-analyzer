import streamlit as st
import matplotlib.pyplot as plt

def plot_skill_match_pie(matched_skills, missing_skills):
    matched_count = len(matched_skills)
    missing_count = len(missing_skills)
    total = matched_count + missing_count

    if total == 0:
        st.info("No skills detected to visualize.")
        return

    labels = ['Matched Skills', 'Missing Skills']
    sizes = [matched_count, missing_count]
    colors = ['#2ecc71', '#e74c3c']

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',
           startangle=140, textprops={'fontsize': 12})
    ax.axis('equal')

    st.pyplot(fig)
