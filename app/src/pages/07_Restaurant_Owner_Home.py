import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')

SideBarLinks()

st.title('Restaurant Owner Home')

if st.button('Restaurant Profile', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/08_Restaurant_Profile.py')

if st.button('Restaurant Analytics', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/09_Restaurant_Analytics.py')