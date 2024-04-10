import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import shap
import pickle
import seaborn as sns

st.set_page_config(
page_title="Explaniability",
page_icon="💡",
layout="centered",
initial_sidebar_state="expanded")

# Load the data
def load_model():
    with open('model.pkl', 'rb') as file:
        data = pickle.load(file)
    return data
data = load_model()
model = data["model"]

df = pd.read_csv("data_lab11.csv").drop(columns='Unnamed: 0')
X_test = pd.read_csv("xtest_lab11.csv").drop(columns='Unnamed: 0')

# Title & text
st.title("Model Explainability 💡")
st.write(" ")
st.write("Explore our explainability tab, powered by SHAP values, to uncover the rationale behind each recommended car price. Understand the key factors influencing our pricing recommendations for a more transparent and informed car-shopping experience.")
st.write(" ")

# Shap init
shap.initjs()
explainer = shap.Explainer(model)
shap_values = explainer(X_test)

# 0. Correlation Matrix
st.subheader("Correlation Matrix")
corr = df.corr()
plt.figure(figsize=(6, 5))
heatmap = sns.heatmap(corr, vmin=-1, vmax=1, annot=True, cmap='magma', annot_kws={"size": 8})
sns.set(font_scale=1)
heatmap.set_xticklabels(heatmap.get_xticklabels(), fontsize=10)
heatmap.set_yticklabels(heatmap.get_yticklabels(), fontsize=10)
st.pyplot()

# Model Explainability
# 1. Summary plot for global explainability
st.subheader("Summary Plot for Global Explainability")
st.pyplot(shap.summary_plot(shap_values, X_test, show=False))

# 2. Bar plot for global explainability
st.subheader("Bar Plot for Global explainability")
st.pyplot(shap.plots.bar(shap_values))

# 3. Shap values for Mileage, EngV, Year
st.subheader("Scatter Plot for Shap Values")
selected_feature = st.selectbox("Select a feature for the scatter plot:", ["mileage", "year", "engV"])
st.subheader(f"Scatter Plot for Shap Values of {selected_feature}:")
st.pyplot(shap.plots.scatter(shap_values[:,selected_feature]))

# 4. Relationship of the variables EngV vs Price
st.subheader("Relationship of the variables EngV vs Price")
st.pyplot(shap.dependence_plot("engV", shap_values.values, X_test, interaction_index= "mileage"))

# 5. Relationship of the variables Year vs Price
st.subheader("Relationship of the variables Year vs Price")
st.pyplot(shap.dependence_plot("year", shap_values.values, X_test, interaction_index= "mileage"))

# Local Explainability
# 6. Waterfall plot
st.subheader("Waterfall plot")
st.pyplot(shap.plots.waterfall(shap_values[0]))

# 7. Decision plot
st.subheader("Decision plot")
st.pyplot(shap.decision_plot(shap_values[0].base_values,shap_values[0].values, X_test.iloc[0]))