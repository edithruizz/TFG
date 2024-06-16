"""
TFG - Bachelor's degree in Computer Engineering
Author: Edith Ruiz Macià
Year: 2024
Project: Improving Water Management in Barcelona through Data Quality Enhancement and Predictive Analytics
"""

import streamlit as st
import matplotlib.pyplot as plt

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
        anomalies = st.session_state.anomalies
        clean_data = st.session_state.clean
        
        st.write('We are now going to state a classification criteria in order to classify said anomalies into 3 categories: leak or waste, system error or correct but misclassified.')
        st.write("This classification is based on the average of the correct real data, I'm not using the predicted one by the models but it might not be very accurate. This should be done with specific data portraying leaks, waste and system errors.")

        st.markdown(
            """
            <h5 style='text-align: left; color: navy;'>Classification Criteria</h5>
            """,
            unsafe_allow_html=True
        )

        # Count of Outliers and Negative values
        outliers_count = (anomalies['Normalized Accumulated Consumption (L/day)'] > 0).sum()
        negative_count = (anomalies['Normalized Accumulated Consumption (L/day)'] < 0).sum()

        total_count = len(anomalies)
        outliers_percentage = (outliers_count / total_count) * 100
        negative_percentage = (negative_count / total_count) * 100

        labels = ['Outliers', 'Negative Consumption']
        sizes = [outliers_percentage, negative_percentage]
        colors = ['cornflowerblue', 'lightskyblue']

        # Pie chart
        plt.figure(figsize=(10, 6))
        plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
        plt.title('Percentage of Outliers and Negative Consumption', fontsize=12)
        plt.ylabel(None)
        plt.axis('equal')
        plt.tight_layout()
        st.pyplot(plt)

        st.write('For each type of Use we can compute the min, average and max values.')
        grouped_data = clean_data.groupby('Use')['Normalized Accumulated Consumption (L/day)'].agg(['min', 'mean', 'max'])

        # Accessing min, average, and max values for a specific 'Use' type
        use_type = 'Domèstic/Doméstico/Domestic'
        domestic_min = grouped_data.loc[use_type, 'min']
        domestic_average = grouped_data.loc[use_type, 'mean']
        domestic_max = grouped_data.loc[use_type, 'max']

        use_type = 'Comercial/Comercial/Commercial'
        commercial_min = grouped_data.loc[use_type, 'min']
        commercial_average = grouped_data.loc[use_type, 'mean']
        commercial_max = grouped_data.loc[use_type, 'max']

        use_type = 'Industrial/Industrial/Industrial'
        industrial_min = grouped_data.loc[use_type, 'min']
        industrial_average = grouped_data.loc[use_type, 'mean']
        industrial_max = grouped_data.loc[use_type, 'max']

        grouped_data

        st.markdown(
            """
            <h5 style='text-align: left; color: navy;'>Anomalies Classification</h5>
            """,
            unsafe_allow_html=True
        )

        def anomalies_classification(dataset_anomalies):
            if dataset_anomalies['Use'] == 'Domèstic/Doméstico/Domestic':
                if dataset_anomalies['Normalized Accumulated Consumption (L/day)'] > domestic_max:
                    return 'Leak or Waste'
                elif dataset_anomalies['Normalized Accumulated Consumption (L/day)'] < 0:
                    return 'Data Collection System Error'
                else:
                    return 'Correct but Misclassified'
                
            elif dataset_anomalies['Use'] == 'Comercial/Comercial/Commercial':
                if dataset_anomalies['Normalized Accumulated Consumption (L/day)'] > commercial_max:
                    return 'Leak or Waste'
                elif dataset_anomalies['Normalized Accumulated Consumption (L/day)'] < 0:
                    return 'Data Collection System Error'
                else:
                    return 'Correct but Misclassified'
                
            elif dataset_anomalies['Use'] == 'Industrial/Industrial/Industrial':
                if dataset_anomalies['Normalized Accumulated Consumption (L/day)'] > industrial_max:
                    return 'Leak or Waste'
                elif dataset_anomalies['Normalized Accumulated Consumption (L/day)'] < 0:
                    return 'Data Collection System Error'
                else:
                    return 'Correct but Misclassified'
 
        anomalies['Classification'] = anomalies.apply(anomalies_classification, axis=1)
        st.dataframe(anomalies.head(3))  
        
        st.write('Now we can visualize the new classification in total and per type of Use.')

        # Count entries of each classification
        classification_counts = anomalies['Classification'].value_counts()
        labels = classification_counts.index
        sizes = classification_counts.values
        colors = ['lightskyblue', 'blue', 'cornflowerblue']

        # Pie chart
        plt.figure(figsize=(10, 6))
        plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
        plt.title('Total Percentage of Each Anomaly Classification', fontsize=12)
        plt.ylabel(None)
        plt.axis('equal')
        plt.tight_layout()
        st.pyplot(plt)


        # Select a Use
        selected_use = st.selectbox("Select the type of Use to visualize its Consumption", anomalies['Use'].unique())

        # Filtered dataset
        domestic_anomalies = anomalies[anomalies['Use'] == selected_use]

        # Count entries of each classification
        classification_counts = domestic_anomalies['Classification'].value_counts()
        labels = classification_counts.index
        sizes = classification_counts.values
        colors = ['lightskyblue', 'blue', 'cornflowerblue'] 

        # Pie chart
        plt.figure(figsize=(10, 6))
        plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
        plt.title(f'Percentage of Each Anomaly Classification for {selected_use} Use', fontsize=12)
        plt.ylabel(None)
        plt.axis('equal')
        plt.tight_layout()
        st.pyplot(plt)

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
            file_name='anomalies.csv',
            mime='text/csv'
        )


except KeyError:
    st.markdown(
    """
    <p style='text-align: center; color: red;'>Go to the Data Loading section in order to upload your dataset first.</p>
    """,
    unsafe_allow_html=True
    )