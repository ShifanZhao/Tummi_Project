import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Welcome Influencer, {st.session_state['first_name']}.")
st.write('')
st.write('')
st.write('### What would you like to do today?')

st.write('')
st.write('See your analytics')

analytics = requests.get('http://api:4000/fi/2/analytics').json()

try:
    st.dataframe(analytics)
except:
    st.write('Could not connect to database to get feed')

import streamlit as st
import requests


analytics = requests.get('http://api:4000/fi/2/analytics').json()

try:
    #follwer count
    st.write(f"**Follower Count:** {analytics.get('FollowerCount', 0)}")

    #posts analytics (data was in a list)
    posts = feed.get("Posts", [])
    if posts:
        st.write("### Posts Analytics")
        for post in posts:
            st.markdown(f"""
            **Post ID:** {post.get('PostId')}  
            ❤️ Likes: {post.get('Likes', 0)} &nbsp; | &nbsp; 🔖 Saves: {post.get('Saves', 0)} &nbsp; | &nbsp; 🔄 Shares: {post.get('Share', 0)} &nbsp; | &nbsp; 📊 Total Engagement: {post.get('TotalEngagement', 0)}
            """)
            st.markdown("---")
    else:
        st.write("No posts found.")
except:
    st.write("Could not connect to database.")



if st.button('See Followers Lists', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/33_Influencer_Follow_List.py')