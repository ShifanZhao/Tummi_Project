import logging
logger = logging.getLogger(__name__)
import streamlit as st
import requests
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks
import pandas as pd
import streamlit as st
from numpy.random import default_rng as rng

SideBarLinks()

st.write("# Leaderboards")


full_df1 = pd.DataFrame(
    rng(0).standard_normal(size=(10, 2)),
    columns=["Username", "# Restaurants Been To"],
    index = range(1, 11)
)

full_df1.index.name = "Rank"

full_df2 = pd.DataFrame(
    rng(0).standard_normal(size=(10, 2)),
    columns=["Username", "# Followers"],
    index = range(1, 11)
)

full_df2.index.name = "Rank"

full_df3 = pd.DataFrame(
    rng(0).standard_normal(size=(10, 2)),
    columns=["Username", "# Photos Uploaded"],
    index = range(1, 11)
)

full_df3.index.name = "Rank"

friends_list = [1, 3, 5, 7, 10]

friends_only = st.toggle("Friends Only", value=False)

if friends_only:
    filtered_df1 = full_df1.loc[friends_list].reset_index(drop=True)
    filtered_df1.index = range(1, len(filtered_df1) + 1)
    filtered_df1.index.name = "Rank"
    
    filtered_df2 = full_df1.loc[friends_list].reset_index(drop=True)
    filtered_df2.index = range(1, len(filtered_df2) + 1)
    filtered_df2.index.name = "Rank"
    
    filtered_df3 = full_df1.loc[friends_list].reset_index(drop=True)
    filtered_df3.index = range(1, len(filtered_df3) + 1)
    filtered_df3.index.name = "Rank"

else:
    filtered_df1 = full_df1
    filtered_df2 = full_df2.copy()
    filtered_df3 = full_df3.copy()

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Been To")
    st.dataframe(filtered_df1)

with col2:
    st.subheader("Followers")
    st.dataframe(filtered_df2)

with col3:
    st.subheader("Photos")
    st.dataframe(filtered_df3)




# SideBarLinks()

# st.write("# Accessing a REST API from Within Streamlit")
# """
# Simply retrieving data from a REST api running in a separate Docker Container.

# If the container isn't running, this will be very unhappy.  But the Streamlit app 
# should not totally die. 
# """

# data = {} 
# try:
#   data = requests.get('http://web-api:4000/data').json()
# except:
#   st.write("**Important**: Could not connect to sample api, so using dummy data.")
#   data = {"a":{"b": "123", "c": "hello"}, "z": {"b": "456", "c": "goodbye"}}

# st.dataframe(data)
