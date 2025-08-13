import logging
logger = logging.getLogger(__name__)
import streamlit as st
from streamlit_extras.app_logo import add_logo
import pandas as pd
import pydeck as pdk
from urllib.error import URLError
from modules.nav import SideBarLinks
from numpy.random import default_rng as rng

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

# Create columns with custom spacing (gap between buttons)
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

# recommended for you section
st.write("#### Recommended for You")

st.markdown("""
<style>
.rounded-rect {
    background-color: #f0f2f6;
    border-radius: 15px;
    padding: 20px;
    margin: 1px 0;
    border: 2px solid #ddd;
    height: 350px;
    width: 300px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}
</style>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="rounded-rect">
        <h4>Restaurant Name 1</h4>
        <p>Location</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="rounded-rect">
        <h4>Restaurant Name 2</h4>
        <p>Location</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="rounded-rect">
        <h4>Restaurant Name 3</h4>
        <p>Location</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="rounded-rect">
        <h4>Restaurant Name 4</h4>
        <p>Location</p>
    </div>
    """, unsafe_allow_html=True)

st.write("")

    # recommended by friends and influencers section
st.write("#### Recommended By Friends and Following")

st.markdown("""
<style>
.rounded-rect {
    background-color: #f0f2f6;
    border-radius: 15px;
    padding: 20px;
    margin: 1px 0;
    border: 2px solid #ddd;
    height: 350px;
    width: 300px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}
</style>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="rounded-rect">
        <h4>Restaurant Name 1</h4>
        <p>Location</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="rounded-rect">
        <h4>Restaurant Name 2</h4>
        <p>Location</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="rounded-rect">
        <h4>Restaurant Name 3</h4>
        <p>Location</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="rounded-rect">
        <h4>Restaurant Name 4</h4>
        <p>Location</p>
    </div>
    """, unsafe_allow_html=True)