"""
TFG - Bachelor's degree in Computer Engineering
Author: Edith Ruiz Macià
Year: 2024
Project: Improving Water Management in Barcelona through Data Quality Enhancement and Predictive Analytics
"""

import streamlit as st
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
    <h3 style='text-align: left; color: navy;'>EDA on Clean Data</h3>
    """,
    unsafe_allow_html=True
)
st.subheader(" ")

try:
    # Retrieve the selected_options dictionary from session state
    selected_options = st.session_state.selected_options

    # Retrieve the value of the eda_clean_enhanced_data variable
    eda_clean_enhanced_data_value = selected_options["eda_clean_enhanced_data"]
    data_prediction_value = selected_options["data_prediction"]

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

        st.write("In this section of the application we can visualize the final clean data. The analysis is divided in 3 sections: Seasonal, Weekly and Geografical.")
        
        if data_prediction_value == True:
            # Retrieve the predicted_file dictionary from session state
            df = st.session_state.predicted_file
            original = st.session_state.uploaded_file
        else:
            # Retrieve the enhanced_file dictionary from session state
            df = st.session_state.enhanced_file
            original = st.session_state.uploaded_file
        
        st.write("Let's start by plotting the categorical attributes of your dataset.")

        # Categorical Plots
        plot_types = {}

        columns = [x for x in df.columns]

        for col in columns:
            if df[col].dtype == 'object':  # Categorical columns
                plot_types[col] = 'bar'
            else:
                unique_values = df[col].nunique()
                if unique_values < 10:  # Discrete columns
                    plot_types[col] = 'bar'
                else:  # Continuous columns
                    plot_types[col] = 'kde'

        n_cols = 3
        n_rows = (len(columns) + 2) // n_cols

        fig, axes = plt.subplots(n_rows, n_cols, figsize=(n_cols * 5, n_rows * 4))
        axes = axes.flatten()

        # Plot each column in the dataframe
        for i, col in enumerate(columns):
            ax = axes[i]
            if plot_types[col] == 'bar':
                # For categorical and discrete data, use a count plot (bar chart)
                sns.countplot(x=col, data=df, ax=ax)
                ax.set_title(f'Count Plot of {col}')
                ax.set_xlabel('')
                ax.set_ylabel('Counts')
                plt.setp(ax.get_xticklabels(), rotation=45, horizontalalignment='right')
            else:
                # For continuous data, use a density plot
                sns.kdeplot(df[col], ax=ax, fill=True)
                ax.set_title(f'Density Plot of {col}')
                ax.set_xlabel(col)
                ax.set_ylabel('Density')

        # Hide any unused subplots
        for j in range(i + 1, n_rows * n_cols):
            fig.delaxes(axes[j])

        fig.tight_layout()
        st.pyplot(plt)


        st.write("Now let's take a look at the water consumption.")

        # Plot consumption in time
        # Select a Use
        selected_consum = st.selectbox("Select the type of Consumption", ["Normalized Accumulated Consumption (L/day)", "Accumulated Consumption (L/day)", "Normalized & Accumulated Consumption (L/day)"])
        
        df_sorted = df.sort_values(by='Date')
        plt.figure(figsize=(10, 5))
            
        if selected_consum == "Accumulated Consumption (L/day)":
            plt.scatter(df_sorted["Date"], df_sorted["Accumulated Consumption (L/day)"], color='blue',  marker='o', s=20, alpha=0.7, label='Accumulated Consumption')
        
        elif selected_consum == "Normalized & Accumulated Consumption (L/day)":
            plt.scatter(df_sorted["Date"], df_sorted["Accumulated Consumption (L/day)"], color='blue',  marker='o', s=20, alpha=0.7, label='Accumulated Consumption')
            plt.scatter(df_sorted["Date"], df_sorted["Normalized Accumulated Consumption (L/day)"], color='lightskyblue',  marker='o', s=20, alpha=0.7, label='Normalized Accumulated Consumption')
        
        else:
            plt.scatter(df_sorted["Date"], df_sorted["Normalized Accumulated Consumption (L/day)"], color='lightskyblue',  marker='o', s=20, alpha=0.7, label='Normalized Accumulated Consumption')
        
        plt.title(f"Distribution of {selected_consum} over Time", fontsize=12)
        plt.xlabel("Date", fontsize=10)
        plt.ylabel(f"{selected_consum}", fontsize=10)
        plt.xticks(rotation=45, ha='right', fontsize=8)
        plt.yticks(fontsize=8)
        plt.grid(True)
        plt.legend(fontsize=7)
        tick_frequency = 100
        plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=tick_frequency))
        st.pyplot(plt)

        st.markdown(
            """
            <h5 style='text-align: left; color: navy;'>Seasonal Analysis</h5>
            """,
            unsafe_allow_html=True
        )

        # Violin plot of seasons by type of use
        # Select a Use
        selected_use = st.selectbox("Select the type of Use to visualize its seasonality", df['Use'].unique())
        df_selected_use = df[df['Use'] == selected_use]

        fig, ax = plt.subplots(figsize=(10, 6))
        sns.violinplot(data=df_selected_use, x='Season', y='Normalized Accumulated Consumption (L/day)', hue='Season', ax=ax, palette={'Spring': '#2ca02c', 'Summer': '#ff7f0e', 'Autumn': '#d62728', 'Winter': '#1f77b4'}, legend=False)
        ax.set_title(f'Seasonal Variations in Normalized Consumption for {selected_use}', fontsize=12)
        ax.set_xlabel('Season', fontsize=10)
        ax.set_ylabel('Normalized Accumulated Consumption (L/day)', fontsize=10)
        ax.tick_params(axis='x', labelsize=8)
        ax.tick_params(axis='y', labelsize=8)
        st.pyplot(fig)

        # Plot consumption for meteo variable
        # Select a meteo factor
        selected_meteo = st.selectbox("Select the meteorological fator", ["Temperature (°C)", "Relative Humidity (%)", "Atmospheric Pressure (hPa)", "Precipitation (mm)", "Solar Radiation global (W/m2)"])

        # Filter the dataset for the specified use cases
        use_cases = ['Domèstic/Doméstico/Domestic', 'Comercial/Comercial/Commercial', 'Industrial/Industrial/Industrial']
        df_sorted = df.sort_values(by='Date')
        filtered_data = df_sorted[df_sorted['Use'].isin(use_cases)]

        # Create the plot
        plt.figure(figsize=(10, 5))

        if selected_meteo == "Relative Humidity (%)":
            sns.lineplot(data=filtered_data, x='Relative Humidity', y='Normalized Accumulated Consumption (L/day)', hue='Use', linewidth=1)

        elif selected_meteo == "Atmospheric Pressure (hPa)":
            sns.lineplot(data=filtered_data, x='Atmospheric Pressure', y='Normalized Accumulated Consumption (L/day)', hue='Use', linewidth=1)

        elif selected_meteo == "Precipitation (mm)":
            sns.lineplot(data=filtered_data, x='Precipitation', y='Normalized Accumulated Consumption (L/day)', hue='Use', linewidth=1)

        elif selected_meteo == "Solar Radiation global (W/m2)":
            sns.lineplot(data=filtered_data, x='Solar Radiation global', y='Normalized Accumulated Consumption (L/day)', hue='Use', linewidth=1)

        else:
            sns.lineplot(data=filtered_data, x='Temperature', y='Normalized Accumulated Consumption (L/day)', hue='Use', linewidth=1)

        # Set titles and labels
        plt.title(f'Water consumption by {selected_meteo}', fontsize=14)
        plt.xlabel(f'{selected_meteo}', fontsize=12)
        plt.ylabel('Normalized Accumulated Consumption (L/day)', fontsize=12)
        plt.legend(title='Use Case', fontsize=10)
        plt.xticks(fontsize=8)
        plt.yticks(fontsize=8)
        plt.grid(True)
        st.pyplot(plt)


        # Normalized Consumption Per Year Scatter Plot
        # Select a Use
        selected_use_2 = st.selectbox("Select the type of Use", ['Domèstic/Doméstico/Domestic', 'Comercial/Comercial/Commercial', 'Industrial/Industrial/Industrial'])
        df_selected_use_2 = df[df['Use'] == selected_use_2]

        df_2019 = df_selected_use_2[df_selected_use_2['Year'] == 2019].groupby(['Date', 'Use'])['Normalized Accumulated Consumption (L/day)'].mean().reset_index()
        df_2020 = df_selected_use_2[df_selected_use_2['Year'] == 2020].groupby(['Date', 'Use'])['Normalized Accumulated Consumption (L/day)'].mean().reset_index()
        df_2021 = df_selected_use_2[df_selected_use_2['Year'] == 2021].groupby(['Date', 'Use'])['Normalized Accumulated Consumption (L/day)'].mean().reset_index()
        df_2022 = df_selected_use_2[df_selected_use_2['Year'] == 2022].groupby(['Date', 'Use'])['Normalized Accumulated Consumption (L/day)'].mean().reset_index()

        fig, ax = plt.subplots(figsize=(12, 6))

        ax.scatter(df_2019["Date"], df_2019["Normalized Accumulated Consumption (L/day)"], color='limegreen',  marker='o', s=20, alpha=0.7, label='2019')
        ax.scatter(df_2020["Date"], df_2020["Normalized Accumulated Consumption (L/day)"], color='cornflowerblue',  marker='o', s=20, alpha=0.7, label='2020')
        ax.scatter(df_2021["Date"], df_2021["Normalized Accumulated Consumption (L/day)"], color='orange',  marker='o', s=20, alpha=0.7, label='2021')
        ax.scatter(df_2022["Date"], df_2022["Normalized Accumulated Consumption (L/day)"], color='tomato',  marker='o', s=20, alpha=0.7, label='2022')

        ax.set_title(f'Distribution of Normalized Accumulated Consumption over Time per Years for {selected_use}', fontsize=12)
        ax.set_xlabel("Date", fontsize=10)
        ax.set_ylabel("Normalized Accumulated Consumption (L/day)", fontsize=10)
        ax.tick_params(axis='x', labelsize=8)
        ax.tick_params(axis='y', labelsize=8)
        ax.legend(fontsize=10)
        tick_frequency = 100
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=tick_frequency))
        st.pyplot(fig)


        st.markdown(
            """
            <h5 style='text-align: left; color: navy;'>Weekly Analysis</h5>
            """,
            unsafe_allow_html=True
        )

        # Weekly Normalized Consumption
        days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

        selected_use_3 = st.selectbox("Select the type of Use to visualize its weekly consumption", ['Domèstic/Doméstico/Domestic', 'Comercial/Comercial/Commercial', 'Industrial/Industrial/Industrial'])

        # Checkboxes for days of the week
        cols = st.columns(3)
        selected_days = []
        for i, day in enumerate(days_of_week):
            selected_days.append(cols[i % 3].checkbox(day, True))

        df_selected_use_3 = df[df['Use'] == selected_use]

        fig, ax = plt.subplots(figsize=(12, 6))
        colors = {'Monday': '#F9DC5C', 'Tuesday': '#FF8360', 'Wednesday': '#FE5F55', 'Thursday': '#EE85B5', 'Friday': '#A663CC', 'Saturday': '#87F1FF', 'Sunday': '#A1C084'}

        for day, selected in zip(days_of_week, selected_days):
            if selected:
                day_data = df_selected_use_3[df_selected_use_3['Day of Week'] == day]
                sns.kdeplot(day_data['Normalized Accumulated Consumption (L/day)'], label=day, ax=ax, fill=True, color=colors[day])

        ax.set_title(f'Weekly Normalized Consumption for {selected_use}', fontsize=12)
        ax.tick_params(axis='x', labelsize=8)
        ax.tick_params(axis='y', labelsize=8)
        ax.legend(loc='upper right', fontsize=10)
        st.pyplot(fig)


        st.markdown(
            """
            <h5 style='text-align: left; color: navy;'>Geographycal Analysis</h5>
            """,
            unsafe_allow_html=True
        )

        # District names dictionary
        district_names = {
            1.0: "Ciutat Vella",
            2.0: "Eixample",
            3.0: "Sants-Montjuïc",
            4.0: "Les Corts",
            5.0: "Sarrià-Sant Gervasi",
            6.0: "Gràcia",
            7.0: "Horta-Guinardó",
            8.0: "Nou Barris",
            9.0: "Sant Andreu",
            10.0: "Sant Martí"
        }

        # Total Normalized Consumption Per District and Year
        # Selector for year
        selected_year = st.selectbox("Select the year to visualize", [2019, 2020, 2021, 2022])

        # Add a column for district names
        df['District Name'] = df['District'].map(district_names)

        # Filter data for the selected year
        df_selected_year = df[df['Year'] == selected_year]

        # Total consumption per district for the selected year
        total_consumption_per_district = df_selected_year.groupby('District Name')['Normalized Accumulated Consumption (L/day)'].sum()
        palette = sns.color_palette("tab10", len(district_names))
        
        # Plot
        plt.figure(figsize=(10, 6))
        sns.barplot(x=total_consumption_per_district.index, y=total_consumption_per_district.values, palette="tab10")
        plt.title(f"Total Normalized Consumption Per District in {selected_year}", fontsize=12)
        plt.xlabel('District', fontsize=10)
        plt.ylabel('Total Normalized Accumulated Consumption (L/day)', fontsize=10)
        plt.xticks(rotation=45, fontsize=8)
        plt.yticks(fontsize=8)
        plt.tight_layout()
        st.pyplot(plt)


        # Total Normalized Consumption Per District and Type of Use
        # Selector for type of use
        selected_use_4 = st.selectbox("Select the type of Use to visualize", ['Domèstic/Doméstico/Domestic', 'Comercial/Comercial/Commercial', 'Industrial/Industrial/Industrial'])

        # Filter data for the selected use case
        df_selected_use_4 = df[df['Use'] == selected_use_4]

        # Total consumption per district for the selected use case
        total_consumption_per_district = df_selected_use_4.groupby('District Name')['Normalized Accumulated Consumption (L/day)'].sum()

        # Plot
        plt.figure(figsize=(10, 6))
        sns.barplot(x=total_consumption_per_district.index, y=total_consumption_per_district.values, palette="tab10")
        plt.title(f"Total Normalized Consumption Per District for {selected_use}", fontsize=12)
        plt.xlabel('District', fontsize=10)
        plt.ylabel('Total Normalized Accumulated Consumption (L/day)', fontsize=10)
        plt.xticks(rotation=45, fontsize=8)
        plt.yticks(fontsize=8)
        plt.tight_layout()
        st.pyplot(plt)
        

except KeyError:
    st.markdown(
    """
    <p style='text-align: center; color: red;'>Go to the Data Loading section in order to upload your dataset first.</p>
    """,
    unsafe_allow_html=True
    )