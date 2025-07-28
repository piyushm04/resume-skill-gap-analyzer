import matplotlib.pyplot as plt
import streamlit as st

def plot_skill_match_pie(matched_count, missing_count):
    """
    Plots a pie chart showing the proportion of matched vs. missing skills.
    """
    labels = ['Matched Skills', 'Missing Skills']
    sizes = [matched_count, missing_count]
    colors = ['#4CAF50', '#FF5722']
    explode = (0.05, 0.05)

    fig, ax = plt.subplots()
    ax.pie(
        sizes,
        explode=explode,
        labels=labels,
        colors=colors,
        autopct='%1.1f%%',
        shadow=True,
        startangle=140
    )
    ax.axis('equal')
    st.pyplot(fig)
