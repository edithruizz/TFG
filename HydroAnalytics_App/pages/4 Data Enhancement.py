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
from io import StringIO

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
    data_preprocessing_value = selected_options["data_preprocessing"]

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
        st.write("In this section of the application we will enhance our data by adding relevant information from the data we already have and from additional geotemporal datasets that can affect water consumption.")

        if data_preprocessing_value == True:
            # Retrieve the cleaned_file dictionary from session state
            df = st.session_state.cleaned_file
            original = st.session_state.uploaded_file
        else:
            # Retrieve the uploaded_file dictionary from session state
            df = st.session_state.uploaded_file
            original = st.session_state.uploaded_file

            st.markdown(
            """
            <h5 style='text-align: left; color: navy;'>Rename columns</h5>
            """,
            unsafe_allow_html=True
            )
            
            # Initial information of the dataset
            string_buffer = StringIO()
            df.info(buf=string_buffer)
            info_str = string_buffer.getvalue()
            st.markdown(f"```\n{info_str}\n```")

            st.write("Let's simplify the naming of the dataset so from this point onwards we have cleaner plots and outputs.")

            new_column_names = {
            'Secció Censal/Sección censal/Census section': 'Census section',
            'Districte/Distrito/District': 'District',
            'Codi postal/Código postal/Postcode': 'Postcode',
            'Municipi/Municipio/Municipality': 'Municipality',
            'Data/Fecha/Date': 'Date',
            'Ús/Uso/Use': 'Use',
            'Nombre de comptadors/Número de contadores/Number of meters': 'Number of meters',
            'Consum acumulat (L/dia)/Consumo acumulado(L/día)/Accumulated Consumption (L/day)': 'Accumulated Consumption (L/day)'
            }

            df.rename(columns=new_column_names, inplace=True)

            # Renamed information of the dataset
            string_buffer = StringIO()
            df.info(buf=string_buffer)
            info_str = string_buffer.getvalue()
            st.markdown(f"```\n{info_str}\n```")
        
        st.markdown(
            """
            <h5 style='text-align: left; color: navy;'>Additional information</h5>
            """,
            unsafe_allow_html=True
        )

        st.write("Adding new columns from the ones that we already have can help see data in different prespectives and give us more informative plots.")

        # Convert "Date" column to datetime
        df['Date'] = pd.to_datetime(df['Date'])

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

        # Distribution of consumption by seasons
        season_consumption = df.groupby('Season')['Normalized Accumulated Consumption (L/day)'].sum()
        plt.figure(figsize=(10, 5))
        season_consumption.plot(kind='bar', color=['skyblue', 'dodgerblue', 'royalblue', 'navy'])
        plt.xlabel('Season', fontsize=10)
        plt.ylabel('Accumulated Consumption (L/day)', fontsize=10)
        plt.xticks(fontsize=8)
        plt.yticks(fontsize=8)
        plt.title('Accumulated Consumption by Season', fontsize=12)
        st.pyplot(plt)


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

        # Precipitation Over Time
        df_sorted = df.sort_values(by='Date')
        plt.figure(figsize=(10, 5))
        plt.plot(df_sorted['Date'], df_sorted['Precipitations'], color='blue', linewidth=2)
        plt.xlabel('Date', fontsize=10)
        plt.ylabel('Precipitations (mm)', fontsize=10)
        plt.title('Precipitations Over Time', fontsize=12)
        plt.xticks(fontsize=8)
        plt.yticks(fontsize=8)
        st.pyplot(plt)

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

        # Temperature Over Time
        df_sorted = df.sort_values(by='Date')
        plt.figure(figsize=(10, 5))
        plt.plot(df_sorted['Date'], df_sorted['Temperature'], color='blue', linewidth=2)
        plt.xlabel('Date', fontsize=10)
        plt.ylabel('Temperature (ºC)', fontsize=10)
        plt.title('Temperature Over Time', fontsize=12)
        plt.xticks(fontsize=8)
        plt.yticks(fontsize=8)
        st.pyplot(plt)

        # Passing enhanced dataset
        st.session_state.enhanced_file = df
        st.session_state.uploaded_file = original

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
            file_name='dataset_enhanced.csv',
            mime='text/csv'
        )

except KeyError:
    st.markdown(
    """
    <p style='text-align: center; color: red;'>Go to the Data Loading section in order to upload your dataset first.</p>
    """,
    unsafe_allow_html=True
    )