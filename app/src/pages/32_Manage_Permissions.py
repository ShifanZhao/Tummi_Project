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

                
        if cols[1].button("✅ Accept", key=f"{modal_type}_{i}_accept"):
            st.success(f"Accepted {row[key_name]}")
            infid = row.get("UserId")
            st.write(infid)
            requests.put(f'http://api:4000/ita/influencers/verify/{row["UserId"]}')
            # TODO: update database
        
        if cols[2].button("❌ Decline", key=f"{modal_type}_{i}_decline"):
            st.warning(f"Declined {row[key_name]}")
            requests.delete(f'http://api:4000/ita/influencers/remove/{row["UserId"]}')
            # TODO: update database



# API call

try:
    pending_users = requests.get("http://api:4000/ita/pending/influencers").json()
except:
    pending_users = []
    st.error("Could not fetch pending users.")




# filling in each tab
(tab1,) = st.tabs(["Pending User Verifications"])
with tab1:
    data_with_modal(tab1, pending_users, "Username", "user")
