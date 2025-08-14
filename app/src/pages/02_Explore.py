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
st.markdown("# Explore")
st.sidebar.header("Explore")

# recs nearby pop up
@st.dialog("Recommendations Nearby")
def show_recommendations_dialog():
    
    df = pd.DataFrame({
    'Name': ["Test"],
    'lat': [42.361145],
    'lon': [-71.057083],
    })

    st.map(df)

    st.write("Restaurants:")
    st.dataframe(df, hide_index=True)
    
# trending pop up
@st.dialog("Trending Restaurants")
def show_trending_dialog():
    
    df = pd.DataFrame(
    rng(0).standard_normal(size=(10, 2)),
    columns=("Name", "Rating"),
)

    st.dataframe(df, hide_index=True)

# friend recs pop up
@st.dialog("Friend Recommendations")
def show_friendrecs_diaglog():

    df = pd.DataFrame(
        rng(0).standard_normal(size=(10,3)),
        columns=("Friend", "Restaurant", "Rating")
    )

    st.dataframe(df, hide_index=True)

# custom spacing (gap between buttons)
col1, col2, col3, col4, col5, col6, col7 = st.columns([0.01, 0.5, 0.1, 0.5, 0.1, 0.5, 2])

with col2:
    if st.button("Recs Nearby", use_container_width=True):
        show_recommendations_dialog()

with col4:
    if st.button("Trending", use_container_width=True):
        show_trending_dialog()

with col6:
    if st.button("Friend Recs", use_container_width=True):
        show_friendrecs_diaglog()


# search bar
search_query = st.text_input("Search", placeholder="Search restaurants, cuisines, etc.")

if search_query:
    st.write(f"You searched for: {search_query}")

feed = requests.get('http://api:4000/cd/get_restaurants').json()


restaurants = requests.get('http://api:4000/cd/get_restaurants').json()

try:
    if restaurants and isinstance(restaurants, list):
        st.write("#### Recommended For You")
        
        # limit to 6 reccomendations on pg
        restaurants = restaurants[:6]
        
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


# View all Restaurants

restaurants = requests.get('http://api:4000/cd/get_restaurants').json()

try:
    if restaurants and isinstance(restaurants, list):
        st.write("#### View all Restaurants")
        
        # limit to 6 reccomendations on pg
        restaurants = restaurants[:6]
        
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


restaurants = requests.get('http://api:4000/cd/get_restaurants').json()

try:
    if restaurants and isinstance(restaurants, list):
        st.write("#### Recommended by Friends and Following")
        
        # limit to 6 reccomendations on pg
        restaurants = restaurants[:6]
        
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
