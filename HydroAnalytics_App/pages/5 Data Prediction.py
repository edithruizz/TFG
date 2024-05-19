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

try:
    # Retrieve the selected_options dictionary from session state
    selected_options = st.session_state.selected_options

    # Retrieve the value of the data_prediction variable
    data_prediction_value = selected_options["data_prediction"]

    # Display the value of the data_prediction variable
    # st.write("Value of data_prediction:", data_prediction_value)

    if data_prediction_value == False :
        st.markdown(
        """
        <p style='text-align: center; color: red;'>You haven't checked this option, go back to Data Loading and check it for Data Prediction.</p>
        """,
        unsafe_allow_html=True
        )
    else:
        st.subheader(" ")

        df = st.session_state.enhanced_file

        st.markdown(
            """
            <h5 style='text-align: left; color: navy;'>Download Predicted Dataset</h5>
            """,
            unsafe_allow_html=True
        )

        # Convert DataFrame to CSV
        csv = df.to_csv(index=False)

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