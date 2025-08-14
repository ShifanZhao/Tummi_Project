import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')

SideBarLinks()

st.title('Followers List')


followers = requests.get('http://api:4000/fi/FoodManiac/followers').json()

try:
    st.dataframe(followers)
except:
    st.write('Could not connect to database to get feed')