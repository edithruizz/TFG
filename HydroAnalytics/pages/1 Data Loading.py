import streamlit as st
import pandas as pd

st.set_page_config(
page_title="HydroAnalytics",
page_icon="💧",
layout="wide",
initial_sidebar_state="expanded")

#The title
st.markdown("""<h3 style='text-align: left; color: navy;'>Data Loading</h3>""",unsafe_allow_html=True)
st.subheader(" ")

st.write("Begin by uploading your data file, nsure it's in CSV format to proceed with the data analysis. Our platform accepts CSV files to facilitate efficient exploration and understanding of your water consumption patterns.")

# File uploader
uploaded_file = st.file_uploader(" ", type=["csv"])

# If a file is uploaded
if uploaded_file is not None:
    # Read the CSV file into a DataFrame
    df = pd.read_csv(uploaded_file)

    # Display a preview of the DataFrame
    st.write("Preview of uploaded data:")
    st.write(df.head())

# explanation of what to do in the next section
st.write(" ")
st.write("Customize your data analysis experience by selecting the operations you wish to perform on your dataset. Check all the options that align with your objectives to tailor the analysis according to your specific needs.")

# Create checkboxes for each option
col1, col2 = st.columns(2)

# Checkboxes for first three options in the first column
with col1:
    exploratory_data_analysis = st.checkbox("Exploratory Data Analysis")
    data_cleaning = st.checkbox("Data Cleaning")
    data_processing = st.checkbox("Data Processing and Enhancement")

# Checkboxes for remaining three options in the second column
with col2:
    data_prediction = st.checkbox("Data Prediction")
    eda_clean_enhanced_data = st.checkbox("EDA on Clean and Enhanced Data")
    analysis_of_anomalies = st.checkbox("Analysis of Anomalies")


# Display the selected options
# st.write("Selected Options:")
# st.write("Exploratory Data Analysis:", exploratory_data_analysis)
# st.write("Data Cleaning:", data_cleaning)
# st.write("Data Processing and Enhancement:", data_processing)
# st.write("Data Prediction:", data_prediction)
# st.write("Analysis of Anomalies:", analysis_of_anomalies)
# st.write("EDA on Clean and Enhanced Data:", eda_clean_enhanced_data)