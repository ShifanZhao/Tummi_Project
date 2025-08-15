import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Welcome Influencer, {st.session_state['first_name']}")
st.write('')


followers_count = 260
following_count = 84

col1, col2, col3, col4, col5 = st.columns([0.1, 0.5, 0.1, 0.5, 3])

with col2:
    st.metric(label="Followers", value=followers_count)

with col4:
    st.metric(label="Following", value=following_count)


st.write('')

tab1, tab2 = st.tabs(["Recent Posts", "Profile Analytics"])

with tab1:
    restaurants = requests.get('http://api:4000/fi/MyInfPost/2').json()

    try:
        if isinstance(restaurants, dict) and "Sadly" in restaurants:
            st.write("No posts available for this user.")
        elif restaurants and isinstance(restaurants, list):
            st.write("")
            st.write("#### Recent Posts")
            
            # limit to 6 posts on page
            restaurants = restaurants[:12]
            
            # display in a 3x2 layout
            for i in range(0, len(restaurants), 3):
                cols = st.columns(3)
                for idx, col in enumerate(cols):
                    if i + idx < len(restaurants):
                        post = restaurants[i + idx]
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
                                <h4 style="margin: 0; color: #333;">@{post.get('username', 'Unknown User')}</h4>
                                <p style="font-size: 14px; color: gray;">Caption: {post.get('Caption', 'No caption')}</p>
                                <p style="font-size: 14px; color: gray;">Rating: {post.get('rating', 0)}/10</p>
                                <p style="font-size: 14px; color: gray;">❤️ {post.get('Likes', 0)} likes</p>
                            </div>
                            """, unsafe_allow_html=True)
        else:
            st.write("No posts found.")
    except Exception as e:
        st.error(f"Could not connect to database or display posts: {e}")
        st.write("Debug info:", restaurants)

with tab2:
    st.write('### See your analytics:')


    analytics = requests.get('http://api:4000/fi/2/analytics').json()

    try:
        #follwer count
        st.write(f"**Follower Count:** {analytics.get('FollowerCount', 0)}")

        #posts analytics (data was in a list)
        posts = analytics.get("Posts", [])
        if posts:
            st.write("**Posts Analytics:**")
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





# restaurants = requests.get('http://api:4000/fi/MyInfPost/2').json()

# try:
#     if isinstance(restaurants, dict) and "Sadly" in restaurants:
#         st.write("No posts available for this user.")
#     elif restaurants and isinstance(restaurants, list):
#         st.write("")
#         st.write("#### Recent Posts")
        
#         # limit to 6 posts on page
#         restaurants = restaurants[:12]
        
#         # display in a 3x2 layout
#         for i in range(0, len(restaurants), 3):
#             cols = st.columns(3)
#             for idx, col in enumerate(cols):
#                 if i + idx < len(restaurants):
#                     post = restaurants[i + idx]
#                     with col:
#                         st.markdown(f"""
#                         <div style="
#                             border: 1px solid #ddd;
#                             border-radius: 10px;
#                             padding: 15px;
#                             margin-bottom: 20px;
#                             background-color: #fff;
#                             box-shadow: 0 2px 5px rgba(0,0,0,0.1);
#                         ">
#                             <h4 style="margin: 0; color: #333;">@{post.get('username', 'Unknown User')}</h4>
#                             <p style="font-size: 14px; color: gray;">Caption: {post.get('Caption', 'No caption')}</p>
#                             <p style="font-size: 14px; color: gray;">Rating: {post.get('rating', 0)}/5</p>
#                             <p style="font-size: 14px; color: gray;">❤️ {post.get('Likes', 0)} likes</p>
#                         </div>
#                         """, unsafe_allow_html=True)
#     else:
#         st.write("No posts found.")
# except Exception as e:
#     st.error(f"Could not connect to database or display posts: {e}")
#     st.write("Debug info:", restaurants)

