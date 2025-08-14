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

st.markdown("#### Lists:")

@st.dialog("Mexican Food")
def show_Mexican_Food():
    
    df = pd.DataFrame(
    rng(0).standard_normal(size=(10, 2)),
    columns=("Name", "Location"),
)
    st.dataframe(df, hide_index=True)

@st.dialog("New Places")
def show_New_Places():
    
    df = pd.DataFrame(
    rng(0).standard_normal(size=(10, 2)),
    columns=("Name", "Location"),
)
    st.dataframe(df, hide_index=True)

@st.dialog("Cheap")
def show_Chaep():
    
    df = pd.DataFrame(
    rng(0).standard_normal(size=(10, 2)),
    columns=("Name", "Location"),
)
    st.dataframe(df, hide_index=True)

@st.dialog("High_Ratings")
def show_High_Ratings():
    
    df = pd.DataFrame(
    rng(0).standard_normal(size=(10, 2)),
    columns=("Name", "Location"),
)
    st.dataframe(df, hide_index=True)

@st.dialog("Vegetarian")
def show_Vegetarian():
    
    df = pd.DataFrame(
    rng(0).standard_normal(size=(10, 2)),
    columns=("Name", "Location"),
)
    st.dataframe(df, hide_index=True)

@st.dialog("Open Late")
def show_Open_Late():
    
    df = pd.DataFrame(
    rng(0).standard_normal(size=(10, 2)),
    columns=("Name", "Location"),
)
    st.dataframe(df, hide_index=True)

# custom spacing (gap between buttons)
col1, col2, col3, col4, col5, col6, col7 = st.columns([0.01, 0.5, 0.1, 0.5, 0.1, 0.5, 2])

with col2:
    if st.button("Mexican Food", use_container_width=True):
        show_Mexican_Food()

with col4:
    if st.button("New Places", use_container_width=True):
        show_New_Places()

with col6:
    if st.button("Cheap", use_container_width=True):
        show_Chaep()

col1, col2, col3, col4, col5, col6, col7 = st.columns([0.01, 0.5, 0.1, 0.5, 0.1, 0.5, 2])

with col2:
    if st.button("High Ratings", use_container_width=True):
        show_High_Ratings()

with col4:
    if st.button("Vegetarian", use_container_width=True):
        show_Vegetarian()

with col6:
    if st.button("Open Late", use_container_width=True):
        show_Open_Late()

# Row 3
col1, col2, col3, col4, col5, col6, col7 = st.columns([0.01, 0.5, 0.1, 0.5, 0.1, 0.5, 2])

if 'new_list_text' not in st.session_state:
    st.session_state.new_list_text = False
    
with col2:
    if st.button("New List", use_container_width=True):
        st.session_state.new_list_text = not st.session_state.new_list_text
    
    if st.session_state.new_list_text:
        st.markdown("Feature coming soon!")

# favorited section
st.markdown("#### Favorited")
col1, col2, col3, col4 = st.columns(4)

with col1:
    with st.container(border=True):
        st.image("https://cdn10.bostonmagazine.com/wp-content/uploads/sites/2/2023/10/beacon_restaurants-2.jpg", use_container_width=True)
        st.write("**Restaurant Name 1**")
        st.write("Location")

with col2:
    with st.container(border=True):
        st.image("https://cdn10.bostonmagazine.com/wp-content/uploads/sites/2/2023/10/beacon_restaurants-2.jpg", use_container_width=True)
        st.write("**Restaurant Name 2**")
        st.write("Location")

with col3:
    with st.container(border=True):
        st.image("https://cdn10.bostonmagazine.com/wp-content/uploads/sites/2/2023/10/beacon_restaurants-2.jpg", use_container_width=True)
        st.write("**Restaurant Name 3**")
        st.write("Location")

with col4:
    with st.container(border=True):
        st.image("https://cdn10.bostonmagazine.com/wp-content/uploads/sites/2/2023/10/beacon_restaurants-2.jpg", use_container_width=True)
        st.write("**Restaurant Name 4**")
        st.write("Location")


bookmarks = requests.get('http://api:4000/cd/Bookmark/1').json()

try:
    st.dataframe(bookmarks)
except:
    st.write('Could not connect to database to get feed')