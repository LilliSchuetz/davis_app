import streamlit as st

st.set_page_config(layout="wide", page_title="DAVIS 2.0", page_icon=":chart_with_upwards_trend:")  # sets layout

# local imports

import app.about as about
import app.exp_data_analysis as exp_data_analysis
import app.fetch_data as fetch_data

st.sidebar.title("Page Navigator")

hide_streamlit_style = """
<style>#MainMenu {visibility: hidden;}footer {visibility: hidden;}</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
options = st.sidebar.radio("Choose:", ["About app", "Experiment data analysis", "Previous experiments"])

if options == "About app":
    about.about()
elif options == "Experiment data analysis":
    exp_data_analysis.exp_data_analysis()
elif options == "Previous experiments":
    fetch_data.fetch_data()
