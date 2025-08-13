import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Welcome Influencer, {st.session_state['first_name']}.")
st.write('')
st.write('')
st.write('### What would you like to do today?')

if st.button('View Leaderboards', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/01_Leaderboard.py')

if st.button("Explore",
             type='primary',
             use_container_width=True):
  st.switch_page('pages/02_Explore.py')
  
if st.button("Bookmarked",
             type='primary',
             use_container_width=True):
  st.switch_page('pages/03_Bookmarked.py')

if st.button('View Profile', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/11_Profile.py')


#if st.button("Profile")