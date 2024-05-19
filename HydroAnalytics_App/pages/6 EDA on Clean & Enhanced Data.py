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
    <h3 style='text-align: left; color: navy;'>EDA on Clean & Enhanced Data</h3>
    """,
    unsafe_allow_html=True
)
st.subheader(" ")

try:
    # Retrieve the selected_options dictionary from session state
    selected_options = st.session_state.selected_options

    # Retrieve the value of the eda_clean_enhanced_data variable
    eda_clean_enhanced_data_value = selected_options["eda_clean_enhanced_data"]

    # Display the value of the eda_clean_enhanced_data variable
    # st.write("Value of eda_clean_enhanced_data:", eda_clean_enhanced_data_value)

    if eda_clean_enhanced_data_value == False :
        st.markdown(
        """
        <p style='text-align: center; color: red;'>You haven't checked this option, go back to Data Loading and check it for EDA on Clean & Enhanced Data.</p>
        """,
        unsafe_allow_html=True
        )
    else:
        st.subheader(" ")

except KeyError:
    st.markdown(
    """
    <p style='text-align: center; color: red;'>Go to the Data Loading section in order to upload your dataset first.</p>
    """,
    unsafe_allow_html=True
    )