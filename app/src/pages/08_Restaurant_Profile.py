import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')

SideBarLinks()

st.title('Restaurant Name')

header_left, header_right = st.columns([3, 1])
with header_left:
    st.markdown("### 𖡡 Location")
with header_right:
    if 'see_menu' not in st.session_state:
        st.session_state.see_menu = False
    
    if st.button("See Menu", use_container_width=True):
        st.session_state.see_menu = not st.session_state.see_menu
    
    if st.session_state.see_menu:
        st.markdown("Feature coming soon!")


st.markdown("### ★ 4.8")
st.markdown("#### Hours: ")
st.write("")
st.markdown("#### About")
st.write("Description")
st.write("")


Popular_Dishes, Customer_Posts = st.tabs(["Popular Dishes", "Customer Posts"])

with Popular_Dishes:
    st.markdown("### Popular Dishes")
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
            st.write("**Dish Name 1**")
            st.write("Rating")

    with col2:
        with st.container(border=True):
            st.image("https://media.istockphoto.com/id/1409329028/vector/no-picture-available-placeholder-thumbnail-icon-illustration-design.jpg?s=612x612&w=0&k=20&c=_zOuJu755g2eEUioiOUdz_mHKJQJn-tDgIAhQzyeKUQ=", use_container_width=True)
            st.write("**Dish Name 2**")
            st.write("Rating")

    with col3:
        with st.container(border=True):
            st.image("https://media.istockphoto.com/id/1409329028/vector/no-picture-available-placeholder-thumbnail-icon-illustration-design.jpg?s=612x612&w=0&k=20&c=_zOuJu755g2eEUioiOUdz_mHKJQJn-tDgIAhQzyeKUQ=", use_container_width=True)
            st.write("**Dish Name 3**")
            st.write("Rating")

    with col4:
        with st.container(border=True):
            st.image("https://media.istockphoto.com/id/1409329028/vector/no-picture-available-placeholder-thumbnail-icon-illustration-design.jpg?s=612x612&w=0&k=20&c=_zOuJu755g2eEUioiOUdz_mHKJQJn-tDgIAhQzyeKUQ=", use_container_width=True)
            st.write("**Dish Name 4**")
            st.write("Rating")

    if 'see_all_text' not in st.session_state:
        st.session_state.see_all_text = False
    
    with col1:
        if st.button("See All", use_container_width=True):
            st.session_state.see_all_text = not st.session_state.see_all_text
    
        if st.session_state.see_all_text:
            st.markdown("Feature coming soon!")
    
with Customer_Posts:
    header_left, header_right = st.columns([3, 1])
    with header_left:
        st.markdown("### Customer Posts")
    with header_right:
        st.caption("SEE ANALYTICS")

    st.write("")

    # Customer posts
    post1, post2 = st.columns(2)

    with post1:
        with st.container(border=True):
            user_info, post_images = st.columns([1, 2])
        
            with user_info:
                st.write("**USERNAME**")
                st.caption("CAPTION")
                st.write("")
                st.write("")
                st.caption("♥︎ 4.2k 🗨️ 1.6k ᯓ➤ 751")

            with post_images:
                img_a, img_b = st.columns(2)
                with img_a:
                    st.image("https://media.istockphoto.com/id/1409329028/vector/no-picture-available-placeholder-thumbnail-icon-illustration-design.jpg?s=612x612&w=0&k=20&c=_zOuJu755g2eEUioiOUdz_mHKJQJn-tDgIAhQzyeKUQ=", use_container_width=True)
                with img_b:
                    st.image("https://media.istockphoto.com/id/1409329028/vector/no-picture-available-placeholder-thumbnail-icon-illustration-design.jpg?s=612x612&w=0&k=20&c=_zOuJu755g2eEUioiOUdz_mHKJQJn-tDgIAhQzyeKUQ=", use_container_width=True)

    with post2:
        with st.container(border=True):
            user_info, post_images = st.columns([1, 2])
        
            with user_info:
                st.write("**USERNAME**")
                st.caption("CAPTION")
                st.write("")
                st.write("")
                st.caption("♥︎ 4.2k 🗨️ 1.6k ᯓ➤ 751")
        
            with post_images:
                img_a, img_b = st.columns(2)
                with img_a:
                    st.image("https://media.istockphoto.com/id/1409329028/vector/no-picture-available-placeholder-thumbnail-icon-illustration-design.jpg?s=612x612&w=0&k=20&c=_zOuJu755g2eEUioiOUdz_mHKJQJn-tDgIAhQzyeKUQ=", use_container_width=True)
                with img_b:
                    st.image("https://media.istockphoto.com/id/1409329028/vector/no-picture-available-placeholder-thumbnail-icon-illustration-design.jpg?s=612x612&w=0&k=20&c=_zOuJu755g2eEUioiOUdz_mHKJQJn-tDgIAhQzyeKUQ=", use_container_width=True)

    if 'see_analytics_text' not in st.session_state:
        st.session_state.see_analytics_text = False
    
    analytics_col1, analytics_col2, analytics_col3, analytics_col4 = st.columns(4)
    
    with analytics_col1:
        if st.button("See Analytics", use_container_width=True):
            st.session_state.see_analytics_text = not st.session_state.see_analytics_text
    
        if st.session_state.see_analytics_text:
            st.markdown("Feature coming soon!")