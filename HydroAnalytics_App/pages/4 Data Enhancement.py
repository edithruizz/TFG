"""
TFG - Bachelor's degree in Computer Engineering
Author: Edith Ruiz Macià
Year: 2024
Project: Improving Water Management in Barcelona through Data Quality Enhancement and Predictive Analytics
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
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
        st.write("In this section of the application we will enhance our data by adding relevant information from the data we already have and from additional meteorological datasets that can affect water consumption.")

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

        st.write("Adding new columns from the ones that we already have can help see data in different perspectives and give us more informative plots.")

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

        if data_preprocessing_value == True :
            # Distribution of consumption by seasons
            season_consumption = df.groupby('Season')['Normalized Accumulated Consumption (L/day)'].sum()
            plt.figure(figsize=(15, 7))
            season_consumption.plot(kind='bar', color=['tomato', 'lightgreen', 'gold', 'skyblue'])
            plt.xlabel('Season', fontsize=10)
            plt.ylabel('Accumulated Consumption (L/day)', fontsize=10)
            plt.xticks(fontsize=8)
            plt.yticks(fontsize=8)
            plt.title('Accumulated Consumption by Season', fontsize=12)
            st.pyplot(plt)

        st.write("Data is from the following years:")
        str = 'Year/s: ' + str(df['Year'].unique())
        st.markdown(f"```\n{str}\n```")
        st.write(" ")

        st.markdown(
            """
            <h5 style='text-align: left; color: navy;'>Meteorological Data</h5>
            """,
            unsafe_allow_html=True
        )

        # Importing the datasets
        # Temperature
        temperature = 'C:/Users/edith/Desktop/TFG\Datasets/Dades meteorològiques de la XEMA/Temperature_Dades_Meteorologiques_XEMA.csv'
        temperature = pd.read_csv(temperature)
        temperature['DATA_LECTURA'] = pd.to_datetime(temperature['DATA_LECTURA'])
        temperature['DATA_LECTURA'] = temperature['DATA_LECTURA'].dt.date
        temperature['DATA_LECTURA'] = pd.to_datetime(temperature['DATA_LECTURA'])
        temperature = temperature.groupby(['CODI_ESTACIO', 'DATA_LECTURA'])['VALOR_LECTURA'].mean().reset_index()

        # Relative Humidity
        rel_humidity = 'C:/Users/edith/Desktop/TFG\Datasets/Dades meteorològiques de la XEMA/Relative_Humidity_Dades_Meteorologiques_XEMA.csv'
        rel_humidity = pd.read_csv(rel_humidity)
        rel_humidity['DATA_LECTURA'] = pd.to_datetime(rel_humidity['DATA_LECTURA'])
        rel_humidity['DATA_LECTURA'] = rel_humidity['DATA_LECTURA'].dt.date
        rel_humidity['DATA_LECTURA'] = pd.to_datetime(rel_humidity['DATA_LECTURA'])
        rel_humidity = rel_humidity.groupby(['CODI_ESTACIO', 'DATA_LECTURA'])['VALOR_LECTURA'].mean().reset_index()
        
        # Atmospheric Pressure
        atm_pressure = 'C:/Users/edith/Desktop/TFG\Datasets/Dades meteorològiques de la XEMA/Atmospheric_Pressure_Dades_Meteorologiques_XEMA.csv'
        atm_pressure = pd.read_csv(atm_pressure)
        atm_pressure['DATA_LECTURA'] = pd.to_datetime(atm_pressure['DATA_LECTURA'])
        atm_pressure['DATA_LECTURA'] = atm_pressure['DATA_LECTURA'].dt.date
        atm_pressure['DATA_LECTURA'] = pd.to_datetime(atm_pressure['DATA_LECTURA'])
        atm_pressure = atm_pressure.groupby(['CODI_ESTACIO', 'DATA_LECTURA'])['VALOR_LECTURA'].mean().reset_index()

        # Precipitation
        precipitation = 'C:/Users/edith/Desktop/TFG\Datasets/Dades meteorològiques de la XEMA/Precipitation_Dades_Meteorologiques_XEMA.csv'
        precipitation = pd.read_csv(precipitation)
        precipitation['DATA_LECTURA'] = pd.to_datetime(precipitation['DATA_LECTURA'])
        precipitation['DATA_LECTURA'] = precipitation['DATA_LECTURA'].dt.date
        precipitation['DATA_LECTURA'] = pd.to_datetime(precipitation['DATA_LECTURA'])
        precipitation = precipitation.groupby(['CODI_ESTACIO', 'DATA_LECTURA'])['VALOR_LECTURA'].mean().reset_index()

        # Global Solar Radiation
        solar_rad = 'C:/Users/edith/Desktop/TFG\Datasets/Dades meteorològiques de la XEMA/Solar_Radation_global_Dades_Meteorologiques_XEMA.csv'
        solar_rad = pd.read_csv(solar_rad)
        solar_rad['DATA_LECTURA'] = pd.to_datetime(solar_rad['DATA_LECTURA'])
        solar_rad['DATA_LECTURA'] = solar_rad['DATA_LECTURA'].dt.date
        solar_rad['DATA_LECTURA'] = pd.to_datetime(solar_rad['DATA_LECTURA'])
        solar_rad = solar_rad.groupby(['CODI_ESTACIO', 'DATA_LECTURA'])['VALOR_LECTURA'].mean().reset_index()

        # Availability of Weather station information
        st.write("Availability of Weather Station information:")

        st.write('Temperature available station info:', " ".join(temperature['CODI_ESTACIO'].unique()))
        st.write('Relative Humidity available station info:', " ".join(rel_humidity['CODI_ESTACIO'].unique()))
        st.write('Atmospheric Pressure available station info:', " ".join(atm_pressure['CODI_ESTACIO'].unique()))
        st.write('Precipitation available station info:', " ".join(precipitation['CODI_ESTACIO'].unique()))
        st.write('Solar Radiation available station info:', " ".join(solar_rad['CODI_ESTACIO'].unique()))

        # Mapping of Municipalities and CP to stations
        st.write("The mapping is done by proximity of the data location to its closest weather station. When it comes to the municipalities of Gavà, Viladecans, Sant Adrià, l'Hospitalet de Llobregat the mapping is direct as follows:")

        municipality_to_station_temp_relh_prec_sol = { "GAVA": "UG", "VILADECANS": "UG", "SANT ADRIA": "WU", "L'HOSPITALET LLOBR.": "XL", "SANT FELIU LL.": "X8" }
        municipality_to_station_atmp = { "GAVA": "D5", "VILADECANS": "D5", "SANT ADRIA": "WU", "L'HOSPITALET LLOBR.": "XL", "SANT FELIU LL.": "X8" }

        postalcode_to_station_temp_relh = {
            8001: 'X4', 8002: 'X4', 8003: 'X2', 8004: 'X4', 8005: 'X2', 8006: 'D5', 8007: 'X4', 8008: 'X4', 8009: 'X4', 8010: 'X4',
            8011: 'X4', 8012: 'D5', 8013: 'X2', 8014: 'XL', 8015: 'X4', 8016: 'D5', 8017: 'X8', 8018: 'X2', 8019: 'X2', 8020: 'X2',
            8021: 'X8', 8022: 'D5', 8023: 'D5', 8024: 'D5', 8025: 'D5', 8026: 'X2', 8027: 'D5', 8028: 'XL', 8029: 'X8', 8030: 'D5',
            8031: 'D5', 8032: 'D5', 8033: 'D5', 8034: 'X8', 8035: 'D5', 8036: 'X4', 8037: 'X4', 8038: 'X4', 8039: 'X4', 8040: 'XL',
            8041: 'D5', 8042: 'D5'
        }

        postalcode_to_station_atmp = {
            8001: 'X4', 8002: 'X4', 8003: 'X4', 8004: 'X4', 8005: 'X4', 8006: 'D5', 8007: 'X4', 8008: 'X4', 8009: 'X4', 8010: 'X4',
            8011: 'X4', 8012: 'D5', 8013: 'X4', 8014: 'D5', 8015: 'X4', 8016: 'D5', 8017: 'X8', 8018: 'X4', 8019: 'X4', 8020: 'X4',
            8021: 'X8', 8022: 'D5', 8023: 'D5', 8024: 'D5', 8025: 'D5', 8026: 'X4', 8027: 'D5', 8028: 'D5', 8029: 'X8', 8030: 'D5',
            8031: 'D5', 8032: 'D5', 8033: 'D5', 8034: 'X8', 8035: 'D5', 8036: 'X4', 8037: 'X4', 8038: 'X4', 8039: 'X4', 8040: 'D5',
            8041: 'D5', 8042: 'D5'
        }

        postalcode_to_station_prec_sol = {
            8001: 'X4', 8002: 'X4', 8003: 'X4', 8004: 'X4', 8005: 'X4', 8006: 'D5', 8007: 'X4', 8008: 'X4', 8009: 'X4', 8010: 'X4',
            8011: 'X4', 8012: 'D5', 8013: 'X4', 8014: 'XL', 8015: 'X4', 8016: 'D5', 8017: 'X8', 8018: 'X4', 8019: 'X4', 8020: 'X4',
            8021: 'X8', 8022: 'D5', 8023: 'D5', 8024: 'D5', 8025: 'D5', 8026: 'X4', 8027: 'D5', 8028: 'XL', 8029: 'X8', 8030: 'D5',
            8031: 'D5', 8032: 'D5', 8033: 'D5', 8034: 'X8', 8035: 'D5', 8036: 'X4', 8037: 'X4', 8038: 'X4', 8039: 'X4', 8040: 'XL',
            8041: 'D5', 8042: 'D5'
        }

        def mapping_geotemporal(dataset, geotemporal, attribute, municipality_to_station, postalcode_to_station):
    
            # Split in two different datasets for CODI_ESTACIO mapping
            dataset_filtered = dataset[dataset['Municipality'].isin(municipality_to_station.keys())]
            dataset_barcelona = dataset[dataset['Municipality'] == "BARCELONA"]

            dataset_filtered['CODI_ESTACIO'] = dataset_filtered['Municipality'].map(municipality_to_station)
            dataset_barcelona['CODI_ESTACIO'] = dataset_barcelona['Postcode'].map(postalcode_to_station)

            # Combine datasets back together
            dataset_combined = pd.concat([dataset_filtered, dataset_barcelona])

            # Merge dataset with geotemporal on 'CODI_ESTACIO' and 'Date'
            dataset = pd.merge(
                dataset_combined, 
                geotemporal, 
                left_on=['CODI_ESTACIO', 'Date'], 
                right_on=['CODI_ESTACIO', 'DATA_LECTURA'],
                how='left'
            )

            # Drop 'CODI_ESTACIO' and 'DATA_LECTURA' and rename 'VALOR_LECTURA'
            dataset.drop(columns=['CODI_ESTACIO', 'DATA_LECTURA'], inplace=True)
            dataset.rename(columns = {'VALOR_LECTURA': attribute}, inplace=True)

            return dataset

        df = mapping_geotemporal(df, temperature, "Temperature", municipality_to_station_temp_relh_prec_sol, postalcode_to_station_temp_relh)
        df = mapping_geotemporal(df, rel_humidity, "Relative Humidity", municipality_to_station_temp_relh_prec_sol, postalcode_to_station_temp_relh)
        df = mapping_geotemporal(df, atm_pressure, "Atmospheric Pressure", municipality_to_station_atmp, postalcode_to_station_atmp)
        df = mapping_geotemporal(df, precipitation, "Precipitation", municipality_to_station_temp_relh_prec_sol, postalcode_to_station_prec_sol)
        df = mapping_geotemporal(df, solar_rad, "Solar Radiation global", municipality_to_station_temp_relh_prec_sol, postalcode_to_station_prec_sol)

        # Final Dataset
        st.write(" ")
        st.write("Final dataset: ")
        st.write(df.head(3))

        # Visualizations
        st.write("Now we can visualize the distributions of the new meteorological datasets we have just added:")
        
        col1, col2 = st.columns(2)

        with col1:
            # Temperature Over Time
            df_sorted = df.sort_values(by='Date')
            plt.figure(figsize=(10, 5))
            plt.plot(df_sorted['Date'], df_sorted['Temperature'], color='orangered', linewidth=1)
            plt.xlabel('Date', fontsize=10)
            plt.ylabel('Temperature (°C)', fontsize=10)
            plt.title('Temperature Over Time', fontsize=12)
            plt.xticks(fontsize=8)
            plt.yticks(fontsize=8)
            st.pyplot(plt)

            # Relative Humidity Over Time
            df_sorted = df.sort_values(by='Date')
            plt.figure(figsize=(10, 5))
            plt.plot(df_sorted['Date'], df_sorted['Relative Humidity'], color='turquoise', linewidth=1)
            plt.xlabel('Date', fontsize=10)
            plt.ylabel('Relative Humidity (%)', fontsize=10)
            plt.title('Relative Humidity Over Time', fontsize=12)
            plt.xticks(fontsize=8)
            plt.yticks(fontsize=8)
            st.pyplot(plt)

            # Atmospheric Pressure Over Time
            df_sorted = df.sort_values(by='Date')
            plt.rcParams['agg.path.chunksize'] = 10000
            plt.figure(figsize=(10, 5))
            plt.plot(df_sorted['Date'], df_sorted['Atmospheric Pressure'], color='mediumorchid', linewidth=1)
            plt.xlabel('Date', fontsize=10)
            plt.ylabel('Atmospheric Pressure (hPa)', fontsize=10)
            plt.title('Atmospheric Pressure Over Time', fontsize=12)
            plt.xticks(fontsize=8)
            plt.yticks(fontsize=8)
            st.pyplot(plt)

        with col2:
            # Precipitation Over Time
            df_sorted = df.sort_values(by='Date')
            plt.figure(figsize=(10, 5))
            plt.plot(df_sorted['Date'], df_sorted['Precipitation'], color='deepskyblue', linewidth=1)
            plt.xlabel('Date', fontsize=10)
            plt.ylabel('Precipitation (mm)', fontsize=10)
            plt.title('Precipitation Over Time', fontsize=12)
            plt.xticks(fontsize=8)
            plt.yticks(fontsize=8)
            st.pyplot(plt)

            # Solar Radation global Over Time
            df_sorted = df.sort_values(by='Date')
            plt.figure(figsize=(10, 5))
            plt.plot(df_sorted['Date'], df_sorted['Solar Radiation global'], color='orange', linewidth=1)
            plt.xlabel('Date', fontsize=10)
            plt.ylabel('Solar Radiation global (W/m2)', fontsize=10)
            plt.title('Solar Radiation global Over Time', fontsize=12)
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