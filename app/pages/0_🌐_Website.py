import streamlit as st
import pathlib

st.set_page_config(
    page_title="SolarYield — AI Solar Forecasting",
    page_icon="☀️",
    layout="wide"
)

st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
[data-testid="stSidebar"] {display: none;}
.block-container {padding: 0 !important; max-width: 100% !important;}
</style>
""", unsafe_allow_html=True)

html_file = pathlib.Path("app/assets/website/index.html")
html_content = html_file.read_text(encoding="utf-8")
st.components.v1.html(html_content, height=6000, scrolling=True)
