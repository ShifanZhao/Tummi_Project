import logging
logger = logging.getLogger(__name__)
import streamlit as st
from streamlit_extras.app_logo import add_logo
import pandas as pd
import pydeck as pdk
from urllib.error import URLError
from modules.nav import SideBarLinks
from numpy.random import default_rng as rng
import requests

SideBarLinks()

# add the logo
add_logo("assets/logo.png", height=400)

# set up the page
st.markdown("# Bookmarked")
st.sidebar.header("Bookmarked")


bookmarks = requests.get('http://api:4000/cd/Bookmark/1').json()

try:
    st.dataframe(bookmarks)
except:
    st.write('Could not connect to database to get feed')