"""
TFG - Bachelor's degree in Computer Engineering
Author: Edith Ruiz Macià
Year: 2024
Project: Improving Water Management in Barcelona through Data Quality Enhancement and Predictive Analytics
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from io import StringIO

st.set_page_config(
page_title="HydroAnalytics",
page_icon="💧",
layout="wide",
initial_sidebar_state="expanded")

st.sidebar.markdown('''<small>© Edith Ruiz Macià - 2024</small>''', unsafe_allow_html=True)

# Title
st.markdown(
    """
    <h3 style='text-align: left; color: navy;'>Data Preprocessing</h3>
    """,
    unsafe_allow_html=True
)
st.subheader(" ")

try:
    # Retrieve the selected_options dictionary from session state
    selected_options = st.session_state.selected_options

    # Retrieve the value of the data_preprocessing variable
    data_preprocessing_value = selected_options["data_preprocessing"]

    # Display the value of the data_preprocessing variable
    #st.write("Value of data_preprocessing:", data_preprocessing_value)

    if data_preprocessing_value == False :
        st.markdown(
        """
        <p style='text-align: center; color: red;'>You haven't checked this option, go back to Data Loading and check it for Data Cleaning.</p>
        """,
        unsafe_allow_html=True
        )
    else:
        # Retrieve the uploaded_file dictionary from session state
        df = st.session_state.uploaded_file
        original = st.session_state.uploaded_file

        st.write("In this section of the application we will clean the data by normalizing it and removing erroneous values and outliers.")

        st.markdown(
            """
            <h5 style='text-align: left; color: navy;'>Rename columns</h5>
            """,
            unsafe_allow_html=True
        )

        # Rename dataset columns

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
            <h5 style='text-align: left; color: navy;'>Data Normalization</h5>
            """,
            unsafe_allow_html=True
        )

        # Normalization of Accumulated Consumption (L/day) by Number of meters
        st.write(df.head(3))

        st.write('As we can see, entries can have different number of meters. We have to take this into account as it is not the same an Accumulated Consumption per 4 meters than 3. Therefore, we can normalize the consumption to make better predictions.')

        df['Normalized Accumulated Consumption (L/day)'] = round(df['Accumulated Consumption (L/day)'] / df['Number of meters'], 3)

        st.write(df.head(3))

        st.write("Let's visualize the normalized data against the original one.")

        # Distribution of the target over time
        plt.figure(figsize=(10, 5))
        plt.scatter(df["Date"], df["Accumulated Consumption (L/day)"], color='blue',  marker='o', s=20, alpha=0.7, label='Accumulated Consumption')
        plt.scatter(df["Date"], df["Normalized Accumulated Consumption (L/day)"], color='lightskyblue',  marker='o', s=20, alpha=0.7, label='Normalized Accumulated Consumption')
        plt.title("Distribution of Accumulated Consumption vs Normalized Accumulated Consumption over Time", fontsize=12)
        plt.xlabel("Date", fontsize=10)
        plt.ylabel("Accumulated Consumption (L/day)", fontsize=10)
        plt.xticks(rotation=45, ha='right', fontsize=8)
        plt.yticks(fontsize=8)
        plt.grid(True)
        plt.legend(fontsize=7)
        tick_frequency = 100
        plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=tick_frequency))
        st.pyplot(plt)

        st.markdown(
            """
            <h5 style='text-align: left; color: navy;'>Null values count</h5>
            """,
            unsafe_allow_html=True
        )

        st.write('It is important to learn about null values in our data, as they can cause misinformation and problems when plotting or computing with our data.')

        # Null values count
        columns_dataset1 = df.columns
        for column in columns_dataset1:
            st.write("Column:", column, "- Null values: ", df[column].isnull().sum())
        
        st.markdown(
            """
            <h5 style='text-align: left; color: navy;'>Wrong values</h5>
            """,
            unsafe_allow_html=True
        )

        st.write('We consider as wrong values those accumulated consumptions that are negative as the only values that make sense for water consumption data are grater or equal to 0. We will replace those values to Null. Later we can predict them and analyze all anomalies.')

        # Wrong Values

        # We identify negative values in consumption
        num_negative_consum_rows = len(df[df['Normalized Accumulated Consumption (L/day)'] < 0])

        str = "Negative values in 'Normalized Accumulated Consumption (L/day)': " + str(num_negative_consum_rows)
        st.markdown(f"```\n{str}\n```")

        # Copy the negative values into the anomalies dataset for later analysis
        anomalies = df[df['Normalized Accumulated Consumption (L/day)'] < 0].copy()

        # Replace negative values in Normalized Accumulated Consumption (L/day) by null
        df_1 = df.copy()
        df_1.loc[df_1['Normalized Accumulated Consumption (L/day)'] < 0, 'Normalized Accumulated Consumption (L/day)'] = np.nan

        # Let's put null also the values of the Accumulated Consumption (L/day)
        df_1.loc[df_1['Accumulated Consumption (L/day)'] < 0, 'Accumulated Consumption (L/day)'] = np.nan   

        # Number of negative values in Normalized Accumulated Consumption (L/day) after removing negative values
        num_negative_consum_rows2 = len(df_1[df_1['Normalized Accumulated Consumption (L/day)'] < 0])

        st.markdown(
            """
            <h5 style='text-align: left; color: navy;'>Outliers</h5>
            """,
            unsafe_allow_html=True
        )

        st.write("We are going to clean outliers in 'Normalized Accumulated Consumption (L/day)' with the IQR method. To be more precise with the cleaning data will be separated by type of 'Use' in Industrial, Domestic or Commercial. Outliers will be replaced by Null and later we can predict them and analyze all anomalies.")

        # Outliers
        # Treatment of outliers in Normalized Accumulated Consumption (L/day) with the IQR method

        # We separate according to USE: Industrial, Domestic or Commercial
        domestic_df = df_1[df_1['Use'].str.contains('Domestic', case=False, na=False)].copy()
        industrial_df = df_1[df_1['Use'].str.contains('Industrial', case=False, na=False)].copy()
        comercial_df = df_1[df_1['Use'].str.contains('Commercial', case=False, na=False)].copy()

        def outliers_iqr(dataframe):
            global anomalies

            # We compute the IQR for the 'Normalized Accumulated Consumption (L/day)' column
            consum_col = 'Normalized Accumulated Consumption (L/day)'
            Q1 = dataframe[consum_col].quantile(0.25)
            Q3 = dataframe[consum_col].quantile(0.75)
            IQR = Q3 - Q1

            # We identify the outliers
            outlier_filter = ((dataframe[consum_col] < (Q1 - 1.5 * IQR)) | (dataframe[consum_col] > (Q3 + 1.5 * IQR)))

            # Copy the outlier value into the anomalies dataset for later analysis
            outliers = dataframe[outlier_filter].copy()
            anomalies = pd.concat([anomalies, outliers], ignore_index=True)

            # And replace them with null
            dataframe.loc[outlier_filter, consum_col] = np.nan

            return dataframe

        # We apply the function for each dataframe corresponding to each "Use"
        domestic_df = outliers_iqr(domestic_df)
        industrial_df = outliers_iqr(industrial_df)
        comercial_df = outliers_iqr(comercial_df)

        dataset1_filtered = pd.concat([domestic_df, industrial_df, comercial_df], ignore_index=True)

        # Let's put to null also the values that correspond to those outliers in 'Accumulated Consumption (L/day)'
        dataset1_filtered.loc[dataset1_filtered['Normalized Accumulated Consumption (L/day)'].isnull(), 'Accumulated Consumption (L/day)'] = np.nan

        # Save anomalies for future analysis
        clean_data = dataset1_filtered.copy()

        st.session_state.clean = clean_data
        st.session_state.anomalies = anomalies

        # Passing cleaned dataset
        st.session_state.cleaned_file = dataset1_filtered
        st.session_state.uploaded_file = original

        # Distribution of the target over time
        plt.figure(figsize=(10, 5))
        plt.scatter(df["Date"], df["Normalized Accumulated Consumption (L/day)"], color='blue',  marker='o', s=20, alpha=0.7, label='Not Clean Normalized Accumulated Consumption')
        plt.scatter(dataset1_filtered["Date"], dataset1_filtered["Normalized Accumulated Consumption (L/day)"], color='lightskyblue',  marker='o', s=20, alpha=0.7, label='Clean Normalized Accumulated Consumption')
        plt.title("Distribution of Not Clean Normalized Accumulated Consumption vs Clean over Time", fontsize=12)
        plt.xlabel("Date", fontsize=10)
        plt.ylabel("Accumulated Consumption (L/day)", fontsize=10)
        plt.xticks(rotation=45, ha='right', fontsize=8)
        plt.yticks(fontsize=8)
        plt.grid(True)
        plt.legend(fontsize=7)
        tick_frequency = 100
        plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=tick_frequency))
        st.pyplot(plt)

        st.markdown(
            """
            <h5 style='text-align: left; color: navy;'>Download Preprocessed Dataset</h5>
            """,
            unsafe_allow_html=True
        )

        # Convert DataFrame to CSV
        csv = dataset1_filtered.to_csv(index=False)

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
