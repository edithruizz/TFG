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
    <h3 style='text-align: left; color: navy;'>Analysis of Anomalies</h3>
    """,
    unsafe_allow_html=True
)
st.subheader(" ")

try:
    # Retrieve the selected_options dictionary from session state
    selected_options = st.session_state.selected_options

    # Retrieve the value of the analysis_of_anomalies variable
    analysis_of_anomalies_value = selected_options["analysis_of_anomalies"]

    # Display the value of the analysis_of_anomalies variable
    # st.write("Value of analysis_of_anomalies:", analysis_of_anomalies_value)

    if analysis_of_anomalies_value == False :
        st.markdown(
        """
        <p style='text-align: center; color: red;'>You haven't checked this option, go back to Data Loading and check it for Analysis of Anomalies.</p>
        """,
        unsafe_allow_html=True
        )
    else:
        st.subheader(" ")

        anomalies = st.session_state.anomalies
        clean_data = st.session_state.clean_data

        st.markdown(
            """
            <h5 style='text-align: left; color: navy;'>Download Anomalies Dataset</h5>
            """,
            unsafe_allow_html=True
        )

        # Convert DataFrame to CSV
        csv = anomalies.to_csv(index=False)

        # Create a download button
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name='dataset_preprocessed.csv',
            mime='text/csv'
        )


except KeyError:
    st.markdown(
    """
    <p style='text-align: center; color: red;'>Go to the Data Loading section in order to upload your dataset first.</p>
    """,
    unsafe_allow_html=True
    )