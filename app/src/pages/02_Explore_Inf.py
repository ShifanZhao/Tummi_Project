import logging
logger = logging.getLogger(__name__)
import streamlit as st
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks
import requests

SideBarLinks()

# add the logo
add_logo("assets/logo.png", height=400)

# set up the page
st.markdown("# Explore")
st.sidebar.header("Explore")


# recs nearby
@st.dialog("Recs Nearby")
def show_recommendations_dialog():
    try:
        location = 'LA'
        restaurant = requests.get(f'http://api:4000/fi/{location}/nearby_rest').json()
        st.dataframe(restaurant, hide_index=True)
    except:
        st.write('No nearby recommendations.')


# trending pop-up
@st.dialog("Trending Restaurants")
def show_trending_dialog():
    try:
        trending = requests.get('http://api:4000/cd/trending').json()
        st.dataframe(trending, hide_index=True)
    except:
        st.write('Could not connect to database.')


# button spacing
col1, col2, col3, col4, col5, col6, col7 = st.columns([0.01, 0.5, 0.1, 0.5, 0.1, 0.5, 2])

with col2:
    if st.button("Recs Nearby", use_container_width=True):
        show_recommendations_dialog()

with col4:
    if st.button("Trending", use_container_width=True):
        show_trending_dialog()


# search bar
search_query = st.text_input("Search", placeholder="Search cuisines")

if search_query:
    st.write(f"You searched for: {search_query}")
    data_req = (f'http://api:4000/cd/discovery_page/{search_query}')
    filtered_rest = requests.get(data_req).json()
    try:
        st.dataframe(filtered_rest)
    except:
        st.write('Could not connect to database to get feed')



# View all Restaurants

restaurants = requests.get('http://api:4000/cd/get_restaurants').json()

try:
    if restaurants and isinstance(restaurants, list):
        st.write("#### View all Restaurants")
        
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


st.write('')
st.write('')


# for influencer user story, search influencer posts by cusine

st.markdown("### Discover Influencer Posts by Cuisine")
cuisine = st.text_input("Cuisine", "")

if st.button("Get Posts"):
    if not cuisine:
        st.warning("Please provide a cuisine type.")
    else:
        try:
            response = requests.get(f"http://api:4000/fi/influ_posts/{cuisine}")
            
            if response.status_code == 200:
                feed = response.json()
                
                if isinstance(feed, dict) and "error" in feed:
                    st.error(feed["error"])
                elif isinstance(feed, dict) and "message" in feed:
                    st.info(feed["message"])
                elif feed and isinstance(feed, list):
                    st.success(f"Found {len(feed)} posts!")
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
                            <h4 style="margin: 0; color: #333;">Influencer: {post.get('Username', 'Unknown')}</h4>
                            <p style="font-size: 16px;">Restaurant: {post.get('RestName')} ({post.get('Cuisine')})</p>
                            <div style="color: gray; font-size: 12px;">
                                ❤️ Likes: {post.get('Likes', 0)} &nbsp; | &nbsp; 🔖 Bookmarks: {post.get('Bookmark', 0)} &nbsp; | &nbsp; 🔄 Shares: {post.get('Share', 0)}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.write("No posts found for this cuisine.")
                    
            elif response.status_code == 404:
                st.error("Cuisine not found in database.")
            else:
                st.error(f"API returned status {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            st.error("🚫 Cannot connect to Flask server! Make sure it's running on port 4000.")
        except requests.exceptions.JSONDecodeError:
            st.error("Invalid response from API")
        except Exception as e:
            st.error(f"Error: {e}")