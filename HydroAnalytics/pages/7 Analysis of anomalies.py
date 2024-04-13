import streamlit as st

st.set_page_config(
page_title="HydroAnalytics",
page_icon="💧",
layout="wide",
initial_sidebar_state="expanded")

st.sidebar.markdown('''<small>© Edith Ruiz Macià 2024</small>''', unsafe_allow_html=True)

#The title
st.markdown(
    """
    <h3 style='text-align: left; color: navy;'>Analysis of Anomalies</h3>
    """,
    unsafe_allow_html=True
)
st.subheader(" ")
st.subheader(" ")