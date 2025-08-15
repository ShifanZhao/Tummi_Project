import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')

SideBarLinks()

st.title('Manage Permissions')


@st.dialog("User Details")
def show_user_info(user_data):
    
    st.write(user_data)

@st.dialog("Restaurant Details")
def show_restaurant_info(restaurant_data):
    
    st.write(restaurant_data)


@st.dialog("Flagged User Details")
def show_flagged_user_info(user_data):
    
    st.write(user_data)


@st.dialog("Flagged Restaurant Details")
def show_flagged_restaurant_info(restaurant_data):
    
    st.write(restaurant_data)

@st.dialog("Flagged Post Details")
def show_flagged_post_info(post_data):

    st.write(post_data) 



# tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Pending User Verifications", 
    "Pending Restaurant Verifications", 
    "Flagged Users", 
    "Flagged Restaurants",
    "Flagged Posts"
])

def data_with_modal(tab, data, key_name, modal_type):
   
    if not data:
        tab.write("No entries to display.")
        return
    
    for i, row in enumerate(data):
        cols = tab.columns([2, 1, 1])
        
        # identifier as a button
        if cols[0].button(row[key_name], key=f"{modal_type}_{i}_name"):
            if modal_type == 'user':
                show_user_info(row)
            elif modal_type == 'restaurant':
                show_restaurant_info(row)
            elif modal_type == 'flagged_user':
                show_flagged_user_info(row)
            elif modal_type == 'flagged_restaurant':
                show_flagged_restaurant_info(row)
            elif modal_type == 'flagged_post':
                show_flagged_post_info(row)
            
        
        if cols[1].button("✅ Accept", key=f"{modal_type}_{i}_accept"):
            st.success(f"Accepted {row[key_name]}")
            # TODO: update database
        
        if cols[2].button("❌ Decline", key=f"{modal_type}_{i}_decline"):
            st.warning(f"Declined {row[key_name]}")
            # TODO: update database


# API call

try:
    pending_users = requests.get("http://api:4000/ita/pending/influencers").json()
except:
    pending_users = []
    st.error("Could not fetch pending users.")

try:
    pending_restaurants = requests.get("http://api:4000/ita/requests/pending").json()
except:
    pending_restaurants = []
    st.error("Could not fetch pending restaurants.")



all_flagged_users = []
flagged_users_routes = ["http://api:4000/ita/moderation/influencers/flagged", "http://api:4000/ita/moderation/diners/flagged", "http://api:4000/ita/moderation/owners/flagged"]

for user in flagged_users_routes:
    try:
        flagged_users = requests.get(user).json()
        all_flagged_users.extend(flagged_users)
    except:
        st.error("Could not fetch flagged users.")

try:
    flagged_restaurants = requests.get("http://api:4000/ita/moderation/restaurants/flagged").json()
except:
    flagged_restaurants = []
    st.error("Could not fetch flagged restaurants.")

try:
    flagged_posts = requests.get("http://api:4000/ita/moderation/cdposts/flagged").json()
except:
    flagged_posts = []
    st.error("Could not fetch flagged posts.")


# filling in each tab
with tab1:
    data_with_modal(tab1, pending_users, "Username", "user")

with tab2:
    data_with_modal(tab2, pending_restaurants, "RestName", "restaurant")

with tab3:
    data_with_modal(tab3, all_flagged_users, "Username", "flagged_user")

with tab4:
    data_with_modal(tab4, flagged_restaurants, "RestName", "flagged_restaurant")

with tab5:
    data_with_modal(tab5, flagged_posts, "PostId", "flagged_post")
