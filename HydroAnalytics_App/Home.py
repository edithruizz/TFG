"""
TFG - Bachelor's degree in Computer Engineering
Author: Edith Ruiz Macià
Year: 2024
Project: Improving Water Management in Barcelona through Data Quality Enhancement and Predictive Analytics
"""

import streamlit as st

st.set_page_config(
page_title="HydroAnalytics",
page_icon="💧",
layout="wide",
initial_sidebar_state="expanded")

st.sidebar.markdown('''<small>© Edith Ruiz Macià - 2024</small>''', unsafe_allow_html=True)

# Page background color
st.markdown("""
<style>
body {
    color: #fff;
    background-color: #111;
}
</style>
    """, unsafe_allow_html=True)

# Title
st.markdown("""<h1 style='text-align: center; color: navy;'>HydroAnalytics</h1>""", unsafe_allow_html=True)
st.subheader(" ")
st.subheader(" ")

# Text
st.markdown("""<h4 style='text-align: left;'>Welcome to HydroAnalytics</h4>""", unsafe_allow_html=True)
st.write(" ")
st.write("HydroAnalytics is a cutting-edge platform revolutionizing water data analytics, serving as a premier destination for understanding and predicting water consumption patterns. As leaders in the field, we're thrilled to introduce our latest innovation: a comprehensive suite of tools designed to empower users in making informed decisions regarding water usage and conservation.")

# Load image 1
image = open("data/water1.jpg", "rb").read()
col1, col2, col3, col4, col5 = st.columns(5)
with col1: st.write(' ')
with col2: st.image(image, caption=' ', width=500, output_format='auto')
with col3: st.write(' ')
st.markdown(
    "<style>div.Widget.row-widget.stImage>div{display: flex;justify-content: center;}</style>", 
    unsafe_allow_html=True)

st.markdown("""<h4 style='text-align: left;'>Explore Water Data Insights</h4>""", unsafe_allow_html=True)
st.write(" ")
st.write("Load your water-related datasets and uncover hidden trends, patterns, and correlations through our intuitive exploratory data analysis tools. From rainfall distribution to temperature fluctuations, gain valuable insights into the factors influencing water consumption.")

st.markdown("""<h4 style='text-align: left;'>Enhance and Predict</h4>""", unsafe_allow_html=True)
st.write(" ")
st.write("Harness the power of advanced data processing techniques to enhance the quality and relevance of your analysis. Our prediction models leverage historical data to forecast missing water consumption with remarkable accuracy. Explore various prediction scenarios and gain a deeper understanding of potential consumption trends.")

# Load image 2
image = open("data/data1.jpg", "rb").read()
col1, col2, col3, col4, col5 = st.columns(5)
with col1: st.write(' ')
with col2: st.image(image, caption=' ', width=500, output_format='auto')
with col3: st.write(' ')
st.markdown(
    "<style>div.Widget.row-widget.stImage>div{display: flex;justify-content: center;}</style>", 
    unsafe_allow_html=True)

st.markdown("""<h4 style='text-align: left;'>Analyze Anomalies</h4>""", unsafe_allow_html=True)
st.write(" ")
st.write("Detect anomalies and irregularities within your water datasets with ease. Our anomaly analysis tools help identify outliers and unusual patterns, enabling proactive intervention and mitigation strategies to ensure optimal water management.")

st.markdown("""<h4 style='text-align: left;'>Understand Model Decisions</h4>""", unsafe_allow_html=True)
# st.write(" ")
# st.write("Gain transparency into our prediction models with our explainability tab. Understand the underlying rationale behind each prediction, visualize feature importance, and interpret model decisions to enhance trust and confidence in the results.")

# Load image 3
image = open("data/data2.jpg", "rb").read()
col1, col2, col3, col4, col5 = st.columns(5)
with col1: st.write(' ')
with col2: st.image(image, caption=' ', width=500, output_format='auto')
with col3: st.write(' ')
st.markdown(
    "<style>div.Widget.row-widget.stImage>div{display: flex;justify-content: center;}</style>", 
    unsafe_allow_html=True)

st.markdown("""<h4 style='text-align: left;'>Join the HydroAnalytics Community</h4>""", unsafe_allow_html=True)
st.write(" ")
st.write("Embark on your journey towards data-driven water management and conservation. Whether you're a researcher, policymaker, or industry professional, HydroAnalytics offers the tools and resources you need to unlock the full potential of your water-related data.")
