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
import numpy as np

st.set_page_config(
page_title="HydroAnalytics",
page_icon="💧",
layout="wide",
initial_sidebar_state="expanded")

st.sidebar.markdown('''<small>© Edith Ruiz Macià - 2024</small>''', unsafe_allow_html=True)

#The title
st.markdown(
    """
    <h3 style='text-align: left; color: navy;'>Data Enhancement</h3>
    """,
    unsafe_allow_html=True
)
st.subheader(" ")

try:
    # Retrieve the selected_options dictionary from session state
    selected_options = st.session_state.selected_options

    # Retrieve the value of the data_enhancement variable
    data_enhancement_value = selected_options["data_enhancement"]

    # Display the value of the data_enhancement variable
    # st.write("Value of data_enhancement:", data_enhancement_value)

    if data_enhancement_value == False :
        st.markdown(
        """
        <p style='text-align: center; color: red;'>You haven't checked this option, go back to Data Loading and check it for Data Enhancement.</p>
        """,
        unsafe_allow_html=True
        )
    else:
        # Retrieve the cleaned_file dictionary from session state
        df = st.session_state.cleaned_file

        st.write("In this section of the application we will enhance our data by adding relevant information from the data we already have and from additional datasets of geotemporal data that can affect water consumption.")

        st.markdown(
            """
            <h5 style='text-align: left; color: navy;'>Additional information</h5>
            """,
            unsafe_allow_html=True
        )

        st.write("Adding new columns from the ones that we already have can help see data in different prespectives and give us more informative plots.")

        # Convert "Date" column to datetime
        df['Date'] = pd.to_datetime(df['Date'])
        # df.info()

        # We create a new "Season" column based on the "Date" column
        def map_to_season(month):
            if 3 <= month <= 5:
                return 'Spring'
            elif 6 <= month <= 8:
                return 'Summer'
            elif 9 <= month <= 11:
                return 'Autumn'
            else:
                return 'Winter'

        df['Season'] = df['Date'].dt.month.map(map_to_season)

        # We create a new column "Day_of_Week" based on the column "Date"
        df['Day of Week'] = df['Date'].dt.day_name()

        # We create a new column "Month" based on the column "Date"
        df['Month'] = df['Date'].dt.month

        # We create a new column "Year" based on the column "Date"
        df['Year'] = df['Date'].dt.year

        st.write("This is how the dataset looks after adding new information:")
        st.write(df.head(3))

        st.write("Data is from the following years:")
        str = 'Year/s: ' + str(df['Year'].unique())
        st.markdown(f"```\n{str}\n```")

        st.markdown(
            """
            <h5 style='text-align: left; color: navy;'>Precipitations</h5>
            """,
            unsafe_allow_html=True
        )

        # Change your path of the data if necessary
        dataset_rain = 'C:/Users/edith/Desktop/TFG/TFG/HydroAnalytics_App/datasets/geotemporal/precipitacionsbcndesde1786_2023_long.csv'
        dataset_rain = pd.read_csv(dataset_rain)

        # Filter the dataset to keep only the desired years
        years_to_keep = [2019, 2020, 2021, 2022]
        dataset_rain = dataset_rain[dataset_rain['Any'].isin(years_to_keep)]

        # Display the first few rows of the filtered dataset
        #dataset_rain.head()
        st.write(dataset_rain.head(3))

        def map_to_precipitation(dataset_filtered, dataset_rain):

            # Merge datasets on 'Year' and 'Month'
            merged_data = pd.merge(dataset_filtered, dataset_rain, left_on=['Year', 'Month'], right_on=['Any', 'Mes'], how='left')

            # Drop unnecessary columns from the merged dataset
            merged_data.drop(['Any', 'Mes', 'Desc_Mes'], axis=1, inplace=True)

            return merged_data

        df = map_to_precipitation(df, dataset_rain)
        df.rename(columns = {'Precipitacions': 'Precipitations'}, inplace=True)
        st.write(df.head(3))

        # plt.figure(figsize=(10, 5))
        # # plt.scatter(df["Date"], df["Normalized Accumulated Consumption (L/day)"], color='lightskyblue',  marker='o', s=20, alpha=0.7, label='Normalized Accumulated Consumption')
        # #plt.scatter(df["Date"], df["Precipitations"], color='blue',  marker='o', s=20, alpha=0.7, label='Precipitations')
        # plt.plot(df["Date"], df["Precipitations"], color='red', label='Precipitations')
        # plt.title("Distribution of Accumulated Consumption vs Normalized Accumulated Consumption over Time", fontsize=12)
        # plt.xlabel("Date", fontsize=10)
        # plt.ylabel("Accumulated Consumption (L/day)", fontsize=10)
        # plt.xticks(rotation=45, ha='right', fontsize=8)
        # plt.yticks(fontsize=8)
        # plt.grid(True)
        # plt.legend(fontsize=7)
        # tick_frequency = 100
        # plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=tick_frequency))
        # st.pyplot(plt)

        st.markdown(
            """
            <h5 style='text-align: left; color: navy;'>Temperature</h5>
            """,
            unsafe_allow_html=True
        )

        # Change your path of the data if necessary
        dataset_temp = 'C:/Users/edith/Desktop/TFG/TFG/HydroAnalytics_App/datasets/geotemporal/temperaturesbcndesde1780_2023_long.csv'
        dataset_temp = pd.read_csv(dataset_temp)

        # Filter the dataset to keep only the desired years
        years_to_keep = [2019, 2020, 2021, 2022]
        dataset_temp = dataset_temp[dataset_temp['Any'].isin(years_to_keep)]

        # Display the first few rows of the filtered dataset
        st.write(dataset_temp.head(3))

        def map_to_temperature(dataset_filtered, dataset_temp):

            # Merge datasets on 'Year' and 'Month'
            merged_data = pd.merge(dataset_filtered, dataset_temp, left_on=['Year', 'Month'], right_on=['Any', 'Mes'], how='left')

            # Drop unnecessary columns from the merged dataset
            merged_data.drop(['Any', 'Mes', 'Desc_Mes'], axis=1, inplace=True)

            return merged_data

        df = map_to_temperature(df, dataset_temp)
        df.rename(columns = {'Temperatura': 'Temperature'}, inplace=True)
        st.write(df.head(3))

        # Passing enhanced dataset
        st.session_state.enhanced_file = df

        st.markdown(
            """
            <h5 style='text-align: left; color: navy;'>Download Enhanced Dataset</h5>
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