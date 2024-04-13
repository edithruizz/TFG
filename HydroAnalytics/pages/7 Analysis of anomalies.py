"""
TFG - Bachelor’s degree in Computer Engineering
Author: Edith Ruiz Macià
Year: 2024
Project: Improving Water Management in Barcelona through Data Quality Enhancement and Predictive Analytics
"""

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

# Retrieve the selected_options dictionary from session state
selected_options = st.session_state.selected_options

# Retrieve the value of the analysis_of_anomalies variable
analysis_of_anomalies_value = selected_options["analysis_of_anomalies"]

# Display the value of the analysis_of_anomalies variable
st.write("Value of analysis_of_anomalies:", analysis_of_anomalies_value)