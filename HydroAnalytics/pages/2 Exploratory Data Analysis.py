"""
TFG - Bachelor’s degree in Computer Engineering
Author: Edith Ruiz Macià
Year: 2024
Project: Improving Water Management in Barcelona through Data Quality Enhancement and Predictive Analytics
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates

st.set_page_config(
page_title="HydroAnalytics",
page_icon="💧",
layout="wide",
initial_sidebar_state="expanded")

st.sidebar.markdown('''<small>© Edith Ruiz Macià - 2024</small>''', unsafe_allow_html=True)

#Title
st.markdown(
    """
    <h3 style='text-align: left; color: navy;'>Exploratory Data Analysis</h3>
    """,
    unsafe_allow_html=True
)
st.subheader(" ")

# Retrieve the selected_options dictionary from session state
selected_options = st.session_state.selected_options

# Retrieve the value of the exploratory_data_analysis variable
exploratory_data_analysis_value = selected_options["exploratory_data_analysis"]

# Display the value of the exploratory_data_analysis variable
# st.write("Value of exploratory_data_analysis:", exploratory_data_analysis_value)

# Retrieve the uploaded_file dictionary from session state
df = st.session_state.uploaded_file

# EDA
st.write("In this section of the application we will look at the insights of the uploaded data by means of interactive plots and tables so we can learn more about the inital state of the data provided.")

# Basic info
st.markdown(
    """
    <h5 style='text-align: left; color: navy;'>How does the data look like?</h5>
    """,
    unsafe_allow_html=True
)
rows = len(df)
columns =len(df.columns)
st.write("We have:")
st.write(str(rows)+" rows")
st.write(str(columns)+" columns")
st.dataframe(df.head(4))

# Setting plot variables
sns.set(font_scale=0.4)
sns.set_palette("plasma")

st.markdown(
    """
    <h5 style='text-align: left; color: navy;'>Visual representation of the dataset</h5>
    """,
    unsafe_allow_html=True
)

# Distribution of the target over time
plt.figure(figsize=(4, 2))
sns.lineplot(data=df, x="Data/Fecha/Date", y="Consum acumulat (L/dia)/Consumo acumulado(L/día)/Accumulated Consumption (L/day)")
plt.title("Distribution of Accumulated Consumption over Time")
plt.xlabel("Date")
plt.ylabel("Accumulated Consumption (L/day)")
plt.xticks(rotation=45)
tick_frequency = 100
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=tick_frequency))
st.pyplot(plt)

# Types of Use
plt.figure(figsize=(2, 2))
df['Ús/Uso/Use'].value_counts().plot(kind='pie', autopct='%1.1f%%', colors=sns.color_palette("plasma", len(df['Ús/Uso/Use'].unique())))
plt.title("Types of Use")
plt.axis('equal')
st.pyplot(plt)

# Select a Use
# st.subheader(f"!!!")
selected_use = st.selectbox("Select a Use of Consumption", df['Ús/Uso/Use'].unique())
df_selected_use = df[df['Ús/Uso/Use'] == selected_use]

# Distribution of the target over time and use1
plt.figure(figsize=(4, 2))
sns.lineplot(data=df_selected_use, x="Data/Fecha/Date", y="Consum acumulat (L/dia)/Consumo acumulado(L/día)/Accumulated Consumption (L/day)")
plt.title(f"Distribution of Accumulated Consumption of {selected_use} Use over Time")
plt.xlabel("Date")
plt.ylabel("Accumulated Consumption (L/day)")
plt.xticks(rotation=45)
tick_frequency = 100
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=tick_frequency))
st.pyplot(plt)