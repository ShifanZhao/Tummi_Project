import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')

SideBarLinks()

st.title('Manage Permissions')


# tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "Pending User Verifications", 
    "Pending Restaurant Verifications", 
    "Flagged Users", 
    "Flagged Restaurants"
])

def data(tab, data, key_name):
    """
    tab: Streamlit tab object
    data: list of dicts from Tummi_db
    key_name: key to display as main identifier (username or name)
    """
    if not data:
        tab.write("No entries to display.")
        return
    
    for i, row in enumerate(data):
        cols = tab.columns(3)  # 1 for name/username, 2 for buttons
        cols[0].write(row[key_name])
        
        # accept button
        if cols[1].button("✅ Accept", key=f"{tab}_{i}_accept"):
            st.success(f"Accepted {row[key_name]}")
            # TODO: update database
        
        # decline button
        if cols[2].button("❌ Decline", key=f"{tab}_{i}_decline"):
            st.warning(f"Declined {row[key_name]}")
            # TODO: update database

# Sample data
pending_users = [{"username": "SpencerTheGuy"}]
pending_restaurants = [{"name": "Evelyn's Restaurant"}]
flagged_users = [{"username": "TiffanyInf"}]
flagged_restaurants = [{"name": "Shifan's Restaurant"}]

# filling in each tab
data(tab1, pending_users, "username")
data(tab2, pending_restaurants, "name")
data(tab3, flagged_users, "username")
data(tab4, flagged_restaurants, "name")

