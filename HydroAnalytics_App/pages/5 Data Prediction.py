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
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.preprocessing import LabelEncoder
from io import StringIO
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
        df = st.session_state.enhanced_file
        original = st.session_state.uploaded_file

        st.write('In order to do the projection of incorrect values (negative and outliers) that right now happen to be null values in the dataset, several prediction models have been tested and the most promising one has been shown to be K-Nearest Neighbors.')
        st.write("We will now encode the variables that aren't numerical in order to work with them and plot a correlation matrix to see which features explain best our target variable, Accumulated Consumption (L/day). ")
        
        st.markdown(
            """
            <h5 style='text-align: left; color: navy;'>Correlation Matrix</h5>
            """,
            unsafe_allow_html=True
            )

        # Convert "Date" column to object for label encoding
        df['Date'] = df['Date'].astype(object) 

        # Label Encoder
        # Initialize LabelEncoder
        label_encoder = LabelEncoder()

        # Apply LabelEncoder to each column containing categorical data
        for column in df.columns:
            if df[column].dtype == 'object':
                df[column] = label_encoder.fit_transform(df[column])  

        # We remove the null values in to see the correct correlation of the data
        df = df.dropna(subset = ['District'])
        df = df.dropna(subset = ['Census section'])

        # Correlation matrix
        df_not_null = df[~df['Accumulated Consumption (L/day)'].isnull()]
        corr = df_not_null.corr()
        plt.figure(figsize=(15,6))
        heatmap = sns.heatmap(corr, vmin=-1, vmax=1, annot=True, cmap='coolwarm')
        heatmap.set_title('Correlation Heatmap', fontdict={'fontsize': 15})
        st.pyplot(plt)

        st.markdown(
            """
            <h5 style='text-align: left; color: navy;'>Model Training</h5>
            """,
            unsafe_allow_html=True
            )
        
        st.write('We are making a prediction with Accumulated Consumption (L/day) instead of the normalized data because it was the original one and shows more promising results. At the end we just have to divide by the Number of Meters.')

        # Model Training
        string_buffer = StringIO()
        df.info(buf=string_buffer)
        info_str = string_buffer.getvalue()
        st.markdown(f"```\n{'Independent variables: Use, Number of meters, Date, Postcode, Census section'}\n```")

        string_buffer = StringIO()
        df.info(buf=string_buffer)
        info_str = string_buffer.getvalue()
        st.markdown(f"```\n{'Dependent variable: Accumulated Consumption (L/day)'}\n```")

        # We remove the null values in the consumption column to train the model
        df2 = df.dropna(subset=['Accumulated Consumption (L/day)'])

        # Independent variables 
        features = ['Use', 'Number of meters', 'Date', 'Postcode', 'Census section']
        X = df2[features]

        # Target variable (dependent variable)
        y = df2['Accumulated Consumption (L/day)']

        # 80% training and 20% testing
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # We make sure that X and Y have the same length for both train and test
        # st.write('We make sure that X and Y have the same length for both train and test')
        # st.write("Lenght X_train:", len(X_train))
        # st.write("Length y_train:", len(y_train))
        # st.write("Lenght X_test:", len(X_test))
        # st.write("Length y_test:", len(y_test))

        # K-Nearest Neighbors
        knn_model = KNeighborsRegressor()
        knn_model.fit(X_train, y_train)
        y_pred_knn = knn_model.predict(X_test)

        # Evaluate the model
        mse_knn = mean_squared_error(y_test, y_pred_knn)
        mae_knn = mean_absolute_error(y_test, y_pred_knn)
        r2_knn = r2_score(y_test, y_pred_knn)

        code = '''
        # K-Nearest Neighbors
        knn_model = KNeighborsRegressor()
        knn_model.fit(X_train, y_train)
        y_pred_knn = knn_model.predict(X_test)

        # Evaluate the model
        mse_knn = mean_squared_error(y_test, y_pred_knn)
        mae_knn = mean_absolute_error(y_test, y_pred_knn)
        r2_knn = r2_score(y_test, y_pred_knn)
        '''
        st.code(code, language='python')

        st.write(f"K-Nearest Neighbors Mean Squared Error (MSE):", round(np.sqrt(mse_knn), 4))
        st.write(f"K-Nearest Neighbors Mean Absolute Error (MAE):", round(mae_knn, 4))
        st.write(f"K-Nearest Neighbors R-squared (R2):", round(r2_knn, 4))

        st.write('It is considered a good model if the R-squared value is higher than 0.9. Therefore now we will replace the missing values with the predictions of this model. We have already trained model so now we replace all null values.')

        # Identify the rows that have a NUll values in 'Accumulated Consumption (L/day)'
        missing_rows = df[df['Accumulated Consumption (L/day)'].isnull()]

        features2 = ['Use', 'Number of meters', 'Date', 'Postcode', 'Census section']
        X_ = missing_rows[features2]

        # Predict the values with the model
        predicted_values = knn_model.predict(X_)

        df.loc[missing_rows.index, 'Accumulated Consumption (L/day)'] = predicted_values

        # We now check that no null values nor negatives are in the dataset
        # Number of null values in Accumulated Consumption (L/day)
        st.write("Number of Nulls in 'Accumulated Consumption (L/day)':", df['Accumulated Consumption (L/day)'].isnull().sum())
        # Number of negatives values in Accumulated Consumption (L/day)
        st.write("Number of Negatives in 'Accumulated Consumption (L/day)':", len(df[df['Accumulated Consumption (L/day)'] < 0]))
        
        st.write('In order to keep working with our normalized values lets once again put all null values in Normalized Accumulated Consumption (L/day) by diving the consumption by the number of meters.')

        predicted_values = df['Accumulated Consumption (L/day)'] / df['Number of meters']

        df.loc[df['Normalized Accumulated Consumption (L/day)'].isnull(), 'Normalized Accumulated Consumption (L/day)'] = predicted_values

        # Number of null values in Normalized Accumulated Consumption (L/day)
        st.write("Number of Nulls in 'Normalized Accumulated Consumption (L/day)':", df['Normalized Accumulated Consumption (L/day)'].isnull().sum())

        # Number of negatives values in Normalized Accumulated Consumption (L/day)
        st.write("Number of Negatives in 'Normalized Accumulated Consumption (L/day)':", len(df[df['Normalized Accumulated Consumption (L/day)'] < 0]))

        # Plot Original vs Predicted Data        
        # plt.figure(figsize=(10, 5))
        # plt.scatter(original["Data/Fecha/Date"], original["Consum acumulat (L/dia)/Consumo acumulado(L/día)/Accumulated Consumption (L/day)"], color='blue',  marker='o', s=20, alpha=0.7, label='Original Accumulated Consumption')
        # plt.scatter(df["Date"], df["Normalized Accumulated Consumption (L/day)"], color='lightskyblue',  marker='o', s=20, alpha=0.7, label='Predicted Normalized Accumulated Consumption')
        # plt.title("Distribution of Accumulated Consumption vs Normalized Accumulated Consumption over Time", fontsize=12)
        # plt.xlabel("Date", fontsize=10)
        # plt.ylabel("Normalized Accumulated Consumption (L/day)", fontsize=10)
        # plt.xticks(rotation=45, ha='right', fontsize=8)
        # plt.yticks(fontsize=8)
        # plt.grid(True)
        # plt.legend(fontsize=7)
        # tick_frequency = 100
        # plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=tick_frequency))
        # st.pyplot(plt)

        # Passing predicted dataset
        st.session_state.predicted_file = df
        st.session_state.uploaded_file = original

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
            file_name='dataset_predicted.csv',
            mime='text/csv'
        )

except KeyError:
    st.markdown(
    """
    <p style='text-align: center; color: red;'>Go to the Data Loading section in order to upload your dataset first.</p>
    """,
    unsafe_allow_html=True
    )