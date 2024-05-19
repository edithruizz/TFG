"""
TFG - Bachelor’s degree in Computer Engineering
Author: Edith Ruiz Macià
Year: 2024
Project: Improving Water Management in Barcelona through Data Quality Enhancement and Predictive Analytics
"""

import streamlit as st
import pandas as pd

st.set_page_config(
page_title="HydroAnalytics",
page_icon="💧",
layout="wide",
initial_sidebar_state="expanded")

st.sidebar.markdown('''<small>© Edith Ruiz Macià - 2024</small>''', unsafe_allow_html=True)

# Title
st.markdown("""<h3 style='text-align: left; color: navy;'>Data Loading</h3>""",unsafe_allow_html=True)
st.subheader(" ")

st.write("Begin by uploading your data file, make sure it's in CSV format to proceed with the data analysis. Our platform only accepts CSV files to facilitate efficient exploration and understanding of water consumption patterns.")

# Define a SessionState class
class SessionState:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

# Check if the 'selected_options' attribute exists in the session state
if 'selected_options' not in st.session_state:
    # If not, initialize it with empty values
    st.session_state.selected_options = {}

# Check if the 'uploaded_file' attribute exists in the session state
if 'uploaded_file' not in st.session_state:
    # If not, initialize it with empty values
    st.session_state.uploaded_file = None

# File uploader
uploaded_file = st.file_uploader(" ", type=["csv"])

# If a file is uploaded
if uploaded_file is not None:
    # Read the CSV file into a DataFrame
    df = pd.read_csv(uploaded_file)

    st.session_state.uploaded_file = df

    # Display a preview of the DataFrame
    # st.write("Preview of uploaded data:")
    # st.write(df.head(3))

# Explanation of what to do in the next section
st.write(" ")
st.write("Customize your data analysis experience by selecting the operations you wish to perform on your dataset. Check all the options that align with your objectives to tailor the analysis according to your specific needs.")

# Checkbox implications logic
def update_checkboxes():
    if st.session_state.data_prediction or st.session_state.eda_clean_enhanced_data or st.session_state.analysis_of_anomalies:
        if st.session_state.analysis_of_anomalies:
            st.session_state.data_preprocessing = True
            return
        else:
            st.session_state.data_preprocessing = True
            st.session_state.data_enhancement = True
    else:
        st.session_state.data_preprocessing = False
        st.session_state.data_enhancement = False

# Create checkboxes for each option
col1, col2 = st.columns(2)

# Checkboxes for first three options in the first column
with col1:
    exploratory_data_analysis = st.checkbox("Exploratory Data Analysis", key='exploratory_data_analysis')
    data_preprocessing = st.checkbox("Data Preprocessing", key='data_preprocessing')
    data_enhancement = st.checkbox("Data Enhancement", key='data_enhancement')

# Checkboxes for remaining three options in the second column
with col2:
    data_prediction = st.checkbox("Data Prediction", key='data_prediction', on_change=update_checkboxes)
    eda_clean_enhanced_data = st.checkbox("EDA on Clean and Enhanced Data", key='eda_clean_enhanced_data', on_change=update_checkboxes)
    analysis_of_anomalies = st.checkbox("Analysis of Anomalies", key='analysis_of_anomalies', on_change=update_checkboxes)


# Display the selected options
# st.write("Selected Options:")
# st.write("Exploratory Data Analysis:", exploratory_data_analysis)
# st.write("Data Preprocessing:", data_preprocessing)
# st.write("Data Processing and Enhancement:", data_enhancement)
# st.write("Data Prediction:", data_prediction)
# st.write("Analysis of Anomalies:", analysis_of_anomalies)
# st.write("EDA on Clean and Enhanced Data:", eda_clean_enhanced_data)

# Button to send the selected options
if st.button("Send"):
    # Store the state of the checkboxes
    st.session_state.selected_options = {
        "exploratory_data_analysis": exploratory_data_analysis,
        "data_preprocessing": data_preprocessing,
        "data_enhancement": data_enhancement,
        "data_prediction": data_prediction,
        "eda_clean_enhanced_data": eda_clean_enhanced_data,
        "analysis_of_anomalies": analysis_of_anomalies
    }

    st.markdown(
    """
    <p style='text-align: center; color: blue;'>You can now navigate thorugh the side menu to see the different sections you have selected and visualize your results.</p>
    """,
    unsafe_allow_html=True
    )