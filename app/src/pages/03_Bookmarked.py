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

@st.dialog("High_Ratings")
def show_High_Ratings():
    
    df = pd.DataFrame(
    rng(0).standard_normal(size=(10, 2)),
    columns=("Name", "Location"),
)
    st.dataframe(df, hide_index=True)



bookmarks = requests.get('http://api:4000/cd/Bookmark/1').json()
st.dataframe(bookmarks)


# custom spacing (gap between buttons)
col1, col2, col3, col4, col5, col6, col7 = st.columns([0.01, 0.5, 0.1, 0.5, 0.1, 0.5, 2])

with col2:
    if st.button("Mexican Food", use_container_width=True):
        show_Mexican_Food()

with col4:
    if st.button("High Ratings", use_container_width=True):
        show_High_Ratings()
    
with col6:
    if st.button("New List", use_container_width=True):
        st.session_state.new_list_text = not st.session_state.new_list_text
    
    if st.session_state.new_list_text:
        st.markdown("Feature coming soon!")

# favorited section

restaurants = requests.get('http://api:4000/cd/get_restaurants').json()

try:
    if restaurants and isinstance(restaurants, list):
        st.write("#### Favorited")
        
        # limit to 12 reccomendations on pg
        restaurants = restaurants[:12]
        
        # display in a 3x2 layout
        for i in range(0, len(restaurants), 3):
            cols = st.columns(3)
            for idx, col in enumerate(cols):
                if i + idx < len(restaurants):
                    rest = restaurants[i + idx]
                    with col:
                        st.markdown(f"""
                        <div style="
                            border: 1px solid #ddd;
                            border-radius: 10px;
                            padding: 15px;
                            margin-bottom: 20px;
                            background-color: #fff;
                            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                        ">
                            <h4 style="margin: 0; color: #333;">{rest.get('RestName', 'Unnamed Restaurant')}</h4>
                            <p style="font-size: 14px; color: gray;">Location: {rest.get('Location', 'Unknown')}</p>
                            <p style="font-size: 14px; color: gray;">Cuisine: {rest.get('Cuisine', 'N/A')}</p>
                            <p style="font-size: 14px; color: gray;">Rating: {rest.get('Rating', 0)}</p>
                        </div>
                        """, unsafe_allow_html=True)
    else:
        st.write("No restaurants found.")
except Exception as e:
    st.error(f"Could not connect to database or display restaurants: {e}")
