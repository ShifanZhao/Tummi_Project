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



st.write("#### Recommended for You")



restaurants = requests.get('http://api:4000/cd/get_restaurants').json()

try:
    st.dataframe(restaurants)
except:
    st.write('Could not connect to database to get feed')

st.set_page_config(layout = 'wide')



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
    with st.container(border=True):
        st.image("https://media.istockphoto.com/id/1409329028/vector/no-picture-available-placeholder-thumbnail-icon-illustration-design.jpg?s=612x612&w=0&k=20&c=_zOuJu755g2eEUioiOUdz_mHKJQJn-tDgIAhQzyeKUQ=", use_container_width=True)
        st.write("**Restaurant Name 1**")
        st.write("Location")

with col2:
    with st.container(border=True):
        st.image("https://media.istockphoto.com/id/1409329028/vector/no-picture-available-placeholder-thumbnail-icon-illustration-design.jpg?s=612x612&w=0&k=20&c=_zOuJu755g2eEUioiOUdz_mHKJQJn-tDgIAhQzyeKUQ=", use_container_width=True)
        st.write("**Restaurant Name 2**")
        st.write("Location")

with col3:
    with st.container(border=True):
        st.image("https://media.istockphoto.com/id/1409329028/vector/no-picture-available-placeholder-thumbnail-icon-illustration-design.jpg?s=612x612&w=0&k=20&c=_zOuJu755g2eEUioiOUdz_mHKJQJn-tDgIAhQzyeKUQ=", use_container_width=True)
        st.write("**Restaurant Name 3**")
        st.write("Location")

with col4:
    with st.container(border=True):
        st.image("https://media.istockphoto.com/id/1409329028/vector/no-picture-available-placeholder-thumbnail-icon-illustration-design.jpg?s=612x612&w=0&k=20&c=_zOuJu755g2eEUioiOUdz_mHKJQJn-tDgIAhQzyeKUQ=", use_container_width=True)
        st.write("**Restaurant Name 4**")
        st.write("Location")

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
    with st.container(border=True):
        st.image("https://media.istockphoto.com/id/1409329028/vector/no-picture-available-placeholder-thumbnail-icon-illustration-design.jpg?s=612x612&w=0&k=20&c=_zOuJu755g2eEUioiOUdz_mHKJQJn-tDgIAhQzyeKUQ=", use_container_width=True)
        st.write("**Restaurant Name 1**")
        st.write("Location")

with col2:
    with st.container(border=True):
        st.image("https://media.istockphoto.com/id/1409329028/vector/no-picture-available-placeholder-thumbnail-icon-illustration-design.jpg?s=612x612&w=0&k=20&c=_zOuJu755g2eEUioiOUdz_mHKJQJn-tDgIAhQzyeKUQ=", use_container_width=True)
        st.write("**Restaurant Name 2**")
        st.write("Location")

with col3:
    with st.container(border=True):
        st.image("https://media.istockphoto.com/id/1409329028/vector/no-picture-available-placeholder-thumbnail-icon-illustration-design.jpg?s=612x612&w=0&k=20&c=_zOuJu755g2eEUioiOUdz_mHKJQJn-tDgIAhQzyeKUQ=", use_container_width=True)
        st.write("**Restaurant Name 3**")
        st.write("Location")

with col4:
    with st.container(border=True):
        st.image("https://media.istockphoto.com/id/1409329028/vector/no-picture-available-placeholder-thumbnail-icon-illustration-design.jpg?s=612x612&w=0&k=20&c=_zOuJu755g2eEUioiOUdz_mHKJQJn-tDgIAhQzyeKUQ=", use_container_width=True)
        st.write("**Restaurant Name 4**")
        st.write("Location")




# for influencer user story, search influencer posts by cusine

st.title("Discover Influencer Posts by Cuisine")

# Inputs
influ_username = st.text_input("Influencer Username", "")
cuisine = st.text_input("Cuisine", "")

if st.button("Get Posts"):
    if not influ_username or not cuisine:
        st.warning("Please provide both influencer username and cuisine type.")
    else:
        # API request
        feed = requests.get(f"http://localhost:4000/fi/influ_posts/{influ_username}/{cuisine}").json()

        try:
            if feed and isinstance(feed, list):
                for post in feed:
                    st.markdown(f"""
                    <div style="
                        border: 1px solid #ddd;
                        border-radius: 10px;
                        padding: 15px;
                        margin-bottom: 20px;
                        background-color: #fff;
                        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                    ">
                        <h4 style="margin: 0; color: #333;">Influencer: {influ_username}</h4>
                        <p style="font-size: 16px;">Restaurant: {post.get('RestName')} ({post.get('Cuisine')})</p>
                        <div style="color: gray; font-size: 12px;">
                            ❤️ Likes: {post.get('Likes', 0)} &nbsp; | &nbsp; 🔖 Bookmarks: {post.get('Bookmark', 0)} &nbsp; | &nbsp; 🔄 Shares: {post.get('Share', 0)}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.write("No posts found for this influencer and cuisine.")
        except Exception as e:
            st.error(f"Error displaying posts: {e}")
