# Improving Water Consumption Management in Barcelona through Data Quality Enhancement and Prediction Models

Author: Edith Ruiz Macià

Tutor: Vladimir Estivill-Castro

Bachelor's final thesis on Computer Engineering

## Abstract
The project aims to improve the quality of water consumption data of Barcelona for better management of resources. Aigües de Barcelona has allowed me to continue using their data as an extension of the project done in the AB Data Challenge. I have enhanced the datasets by applying data cleaning and adding new features combining meteorological datasets. I stored all anomalies detected for analysis and classification into different categories. Anomalies can have different sources and serve as potential indicators of a water misuse, leak or errors of the data collection system. I have predicted the missing values caused by the data cleaning and tested the accuracy of five prediction models in order to select the most accurate one for each specific dataset. Finally, I designed a solution in the form of a web application, defined the necessary requirements based on a needs analysis and developed a first version prototype. The app allows users to learn about the insights of datasets with a similar structure to those of Aigües de Barcelona.

## Structure of the Repository
#### HydroAnalytics_App
Code for HydroAnalytics, an application created with the Streamlit library in Python. This application analyzes datasets of similar structure and type to those provided by Aigües de Barcelona. The user imports their csv file and can select which procedures to apply to their data, among which there are data cleaning, data enhancement, data prediction, exploratory data analysis and analysis of anomalies.

#### Python_Notebooks
Python notebooks in which I apply data transformation, data cleaning, data enhancement, data prediction, exploratory data analysis and analysis of anomalies to the datasets dataset1_v2.csv, dataset2_v2.csv and dataset1_activitat_eco_v2.csv provided by Aigües de Barcelona.