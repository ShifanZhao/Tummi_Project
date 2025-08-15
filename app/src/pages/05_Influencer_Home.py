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

if st.button('View Leaderboards', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/01_Leaderboard.py')

if st.button('View Profile', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/11_Profile.py')


# rest of home page
st.write("")

# search bar
search_query = st.text_input("Search", placeholder="Search restaurants, cuisines, etc.")

if search_query:
    st.write(f"You searched for: {search_query}")
    # TODO: Connect to API or DB to show real search results

st.markdown("---")

st.write("")


# Get info required to make a new post
st.write('### Create a new post')
with st.form("Create a new post"):
    rating = st.number_input("Rate this restaurant 0-10:")
    caption = st.text_input("Review of Restaurant:")
    restid = st.number_input("RestaurantID:")

    # Click post button
    submitted = st.form_submit_button("Post")

    if submitted:
        data = {}
        data["Rating"] = rating
        data["Caption"] = caption
        data["RestId"] = restid
        st.write(data)

        # Create new post with provided data
        requests.post('http://api:4000/fi/2/createpost', json=data)
        
        
        

st.write('')
st.write('### Look At Your Feed')
# feed posts
feed = requests.get('http://api:4000/fi/InfPost/2').json()

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
                <h4 style="margin: 0; color: #333;">influencer: {post.get('username')}</h4>
                <p style="font-size: 16px;">{post.get('Caption', '')}</p>
                <div style="color: gray; font-size: 12px;">
                    ❤️ {post.get('Likes', 0)} &nbsp; | &nbsp; ⭐ {post.get('rating', 0)} &nbsp; | &nbsp; 🔖 {post.get('bookmark', 0)} &nbsp; | &nbsp; 🔄 {post.get('share', 0)}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("❤️ Like", key=f"like_{post.get('PostId')}"):
                    try:
                        response = requests.put(f'http://api:4000/fi/InfPost/{post.get("PostId")}')
                        if response.status_code == 200:
                            st.success("Liked!")
                            st.rerun()  # Refresh to show updated like count
                        else:
                            st.error("Failed to like post")
                    except Exception as e:
                        st.error(f"Error: {e}")
                        
            with col2:
                with st.form(f"Comment_{post.get('PostId')}"):
                    comment = st.text_input("Create Comment:", key=f"comment_input_{post.get('PostId')}")
                    submitted = st.form_submit_button("Post Comment")
                    
                    if submitted and comment:
                        try:
                            data = {}
                            data["Comment"] = comment
                            data["InfPostId"] = post.get('PostId')
                            
                            st.write("Data being sent:", data)
                            response = requests.post('http://api:4000/fi/createcomment', json=data)
                            
                            st.write(f"Response Status: {response.status_code}")
                            st.write(f"Response Content: {response.text}")
                            
                            if response.status_code == 200:
                                st.success("Comment made!")
                                st.rerun()
                                
                        except Exception as e:
                            st.error(f"Error: {e}")
                    
                    elif submitted and not comment:
                        st.warning("Please enter a comment before submitting.")
            with col3:
                with st.form(f"Bookmark_{post.get('PostId')}"):
                    rest = st.text_input("Create bookmark:", key=f"bookmark_input_{post.get('PostId')}")
                    submitted = st.form_submit_button("Create Bookmark")
                    
                    if submitted and rest:
                        try:
                            data = {}
                            data["rest"] = rest
                            
                            st.write("Data being sent:", data)
                            response = requests.post('http://api:4000/fi/createbm/2', json=data)
                            
                            st.write(f"Response Status: {response.status_code}")
                            st.write(f"Response Content: {response.text}")
                            
                            if response.status_code == 200:
                                st.success("Bookmark made!")
                                st.rerun()
                                
                        except Exception as e:
                            st.error(f"Error: {e}")          
    else:
        st.write("No posts found.")
except Exception as e:
    st.error(f"Error displaying posts: {e}")
    
    
    

