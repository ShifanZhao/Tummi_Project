import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')

SideBarLinks()


# Get info required to make a new post
st.write('### Delete a menu item')
with st.form("Delete a menu item"):
    dishid = st.number_input("DishId to be removed:", step=1)

    # Click remove button to confirm
    submitted = st.form_submit_button("Remove")

    if submitted:
        # delete
        resp = requests.delete(f'http://api:4000/ro/delete_menuitem/{dishid}')
        


rest_data = requests.get('http://api:4000/ro/restaurant/3').json()
for inst in rest_data:
    rating = inst.get('Rating')
    RestName = inst.get('RestName')
    cuisine = inst.get('Cuisine')
    Location = inst.get('Location')
    rest_id = inst.get('RestId')
    
    col1, col2, col3 = st.columns(3)
    
    st.title(f'{RestName}')
    header_left, header_right = st.columns([3, 1])
    with header_left:
        st.markdown(f"### 𖡡 Location: {Location}")
        st.markdown(f"### ★ {rating}")
        st.write("")
        st.markdown(f"#### Cuisine: {cuisine}")
        st.write("")
        Customer_Posts, = st.tabs(["Customer Posts"])
        
        with Customer_Posts:
            restaurants = requests.get(f'http://api:4000/ro/restaurant_posts/{rest_id}').json()
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
                                        <p style="font-size: 14px; color: gray;">Rating: {post.get('Rating', 0)}/10</p>
                                        <p style="font-size: 14px; color: gray;">❤️ {post.get('Likes', 0)} likes</p>
                                    </div>
                                    """, unsafe_allow_html=True)
                else:
                    st.write("No posts found.")
            except Exception as e:
                st.error(f"Could not connect to database or display posts: {e}")
                st.write("Debug info:", restaurants)
    
    with col3:
        # Create unique session state key for each restaurant
        menu_key = f'see_menu_{rest_id}'
        
        if menu_key not in st.session_state:
            st.session_state[menu_key] = False
        
        if st.button("See Menu", use_container_width=True, key=f"see_menu_btn_{rest_id}"):
            st.session_state[menu_key] = not st.session_state[menu_key]
    
        if st.session_state[menu_key]:
            try:
                response = requests.get(f'http://api:4000/ro/menuitem/{rest_id}')
                if response.status_code == 200:
                    menu_data = response.json()
                    st.dataframe(menu_data)
                else:
                    st.error("Failed to retrieve menu")
            except Exception as e:
                st.error(f"Error: {e}")