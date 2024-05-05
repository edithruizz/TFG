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

st.sidebar.markdown('''<small>© Edith Ruiz Macià - 2024</small>''', unsafe_allow_html=True)

#The title
st.markdown(
    """
    <h3 style='text-align: left; color: navy;'>Data Prediction</h3>
    """,
    unsafe_allow_html=True
)
st.subheader(" ")
st.subheader(" ")

# Retrieve the selected_options dictionary from session state
selected_options = st.session_state.selected_options

# Retrieve the value of the data_prediction variable
data_prediction_value = selected_options["data_prediction"]

# Display the value of the data_prediction variable
st.write("Value of data_prediction:", data_prediction_value)