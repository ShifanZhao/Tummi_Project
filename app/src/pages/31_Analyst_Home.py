import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')

SideBarLinks()

st.title('Analyst Dashboard')
st.write(f"Welcome, {st.session_state['first_name']} — Internal Analyst")
st.write("This dashboard lets you manage pending verifications, review flagged users and restaurants, and access app analytics.")


if st.button('Manage Permissions', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/32_Manage_Permissions.py')

