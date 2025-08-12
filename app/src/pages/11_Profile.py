import logging

logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout="wide")

# Display the appropriate sidebar links for the role of the logged in user
SideBarLinks()

# st.title("Prediction with Regression")

st.markdown("""
<style>
.color-bar {
    position: fixed;
    top: 0;
    left: 0;
    width: 650px;
    height: 100vh;
    background-color: #e6a78e;
    z-index: 1000;
}
</style>
<div class="color-bar"></div>
""", unsafe_allow_html=True)

st.markdown("""
<style>
.circle {
    position: fixed;
    top: 100px;
    left: 300px;
    width: 300px;
    height: 300px;
    background-color: #ff6b6b;
    border-radius: 50%;
    z-index: 1000;
}
</style>
<div class="circle"></div>
""", unsafe_allow_html=True)


# Background content
# st.title("Main Content")
# st.write("This is the main content of the page")

# Overlay text
st.markdown("""
<style>
.overlay-text {
    position: fixed;
    top: 430px;
    left: 390px;
    font-size: 30px;
    color: black;
    background-color: rgba(0, 0, 0, 0);
    padding: 0px, 0px;
    border-radius: 10px;
    z-index: 1000;
}
</style>
<div class="overlay-text">Tiffany</div>
""", unsafe_allow_html=True)



