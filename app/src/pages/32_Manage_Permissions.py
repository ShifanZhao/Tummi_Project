import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')

SideBarLinks()

st.title('Manage Permissions')


# # tabs
# tab1, tab2, tab3, tab4 = st.tabs([
#     "Pending User Verifications", 
#     "Pending Restaurant Verifications", 
#     "Flagged Users", 
#     "Flagged Restaurants"
# ])

# def data(tab, data, key_name):
#     """
#     tab: Streamlit tab object
#     data: list of dicts from Tummi_db
#     key_name: key to display as main identifier (username or name)
#     """
#     if not data:
#         tab.write("No entries to display.")
#         return
    
#     for i, row in enumerate(data):
#         cols = tab.columns(3)  # 1 for name/username, 2 for buttons
#         cols[0].write(row[key_name])
        
#         # accept button
#         if cols[1].button("✅ Accept", key=f"{tab}_{i}_accept"):
#             st.success(f"Accepted {row[key_name]}")
#             # TODO: update database
        
#         # decline button
#         if cols[2].button("❌ Decline", key=f"{tab}_{i}_decline"):
#             st.warning(f"Declined {row[key_name]}")
#             # TODO: update database

# # Sample data
# pending_users = [{"username": "SpencerTheGuy"}]
# pending_restaurants = [{"name": "Evelyn's Restaurant"}]
# flagged_users = [{"username": "TiffanyInf"}]
# flagged_restaurants = [{"name": "Shifan's Restaurant"}]

# # filling in each tab
# data(tab1, pending_users, "username")
# data(tab2, pending_restaurants, "name")
# data(tab3, flagged_users, "username")
# data(tab4, flagged_restaurants, "name")







# # recs nearby pop up
# @st.dialog("Username")
# def show_pending_user():
    
#     st.write("add stuff here")
    
# # trending pop up
# @st.dialog("Trending Restaurants")
# def show_trending_dialog():
    
#     df = pd.DataFrame(
#     rng(0).standard_normal(size=(10, 2)),
#     columns=("Name", "Rating"),
# )

#     st.dataframe(df, hide_index=True)

# # friend recs pop up
# @st.dialog("Friend Recommendations")
# def show_friendrecs_diaglog():

#     df = pd.DataFrame(
#         rng(0).standard_normal(size=(10,3)),
#         columns=("Friend", "Restaurant", "Rating")
#     )

#     st.dataframe(df, hide_index=True)




# # create columns
# col1, col2, col3, col4, col5, col6, col7 = st.columns([0.01, 0.5, 0.1, 0.5, 0.1, 0.5, 2])

# with col2:
#     if st.button("Username", use_container_width=True):
#         show_pending_user
        

# with col4:
#     if st.button("Trending", use_container_width=True):
#         show_trending_dialog()

# with col6:
#     if st.button("Friend Recs", use_container_width=True):
#         show_friendrecs_diaglog()











@st.dialog("User Details")
def show_user_info(user_data):
    
    st.write("add stuff here")

@st.dialog("Restaurant Details")
def show_restaurant_info(restaurant_data):
    
    st.write("add stuff here")


@st.dialog("Flagged User Details")
def show_flagged_user_info(user_data):
    
    st.write("add stuff here")


@st.dialog("Flagged Restaurant Details")
def show_flagged_restaurant_info(restaurant_data):
    
    st.write("add stuff here")


# tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "Pending User Verifications", 
    "Pending Restaurant Verifications", 
    "Flagged Users", 
    "Flagged Restaurants"
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
        
        if cols[1].button("✅ Accept", key=f"{modal_type}_{i}_accept"):
            st.success(f"Accepted {row[key_name]}")
            # TODO: update database
        
        if cols[2].button("❌ Decline", key=f"{modal_type}_{i}_decline"):
            st.warning(f"Declined {row[key_name]}")
            # TODO: update database

# sample data
pending_users = [{"username": "SpencerTheGuy", "email": "spencer@example.com", "registration_date": "2024-01-15"}]
pending_restaurants = [{"name": "Evelyn's Restaurant", "address": "123 Main St", "cuisine_type": "Italian", "owner": "Evelyn Smith"}]
flagged_users = [{"username": "TiffanyInf", "flag_reason": "Inappropriate content", "flag_date": "2024-01-20", "reported_by": "User123"}]
flagged_restaurants = [{"name": "Shifan's Restaurant", "flag_reason": "False information", "flag_date": "2024-01-18", "reported_by": "FoodCritic"}]

# filling in each tab
with tab1:
    data_with_modal(tab1, pending_users, "username", "user")

with tab2:
    data_with_modal(tab2, pending_restaurants, "name", "restaurant")

with tab3:
    data_with_modal(tab3, flagged_users, "username", "flagged_user")

with tab4:
    data_with_modal(tab4, flagged_restaurants, "name", "flagged_restaurant")