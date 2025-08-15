import logging
logger = logging.getLogger(__name__)

from modules.nav import SideBarLinks

import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import requests

st.set_page_config(layout = 'wide')

SideBarLinks()

st.title('Analyst Dashboard')
st.write(f"Welcome, {st.session_state['first_name']} — Internal Analyst")
st.write("This dashboard lets you manage pending verifications, review flagged users and restaurants, and access app analytics.")


if st.button('Manage Permissions', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/32_Manage_Permissions.py')

st.write('')
st.write('')


# feature engagement
feature_engagement = requests.get('http://api:4000/ita/features/usage').json()

try:
    feature_engagement = pd.DataFrame(feature_engagement)
    feature_engagement.columns = ["Feature", "Engagement"]
except:
    feature_engagement = pd.DataFrame(columns=["Feature", "Engagement"])
    st.error("Could not fetch feature usage data")


# returning users
returning_users = requests.get("http://api:4000/ita/returning").json()

try:
    audience_insights_data = pd.DataFrame(returning_users)
    audience_insights_data.columns = ["UserId", "Sessions", "FirstVisit", "LastVisit"]
except:
    audience_insights_data = pd.DataFrame(columns=["UserId", "Sessions", "FirstVisit", "LastVisit"])
    st.error("Could not fetch returning users data")


# daily active
daily_active = requests.get("http://api:4000/ita/dau").json()

try:
    user_frequency_data = pd.DataFrame(daily_active)
    user_frequency_data.columns = ["ActiveUsers", "Day"]
except:
    user_frequency_data = pd.DataFrame(columns=["ActiveUsers", "Day"])
    st.error("Could not fetch daily active users data")



# 2x2 chart layout
col1, col2 = st.columns(2)

with col1:
    st.subheader("Feature Engagement")
    chart1 = alt.Chart(feature_engagement).mark_bar().encode(
        x=alt.X('Feature', sort='-y'),
        y='Engagement',
        color='Feature'
    )
    st.altair_chart(chart1, use_container_width=True)

with col2:
    st.subheader("Latest 15 Returning Users (by Session Count)")
    chart2 = alt.Chart(audience_insights_data).mark_bar().encode(
        x=alt.X('UserId', sort='-y'),
        y='Sessions',
        color='UserId'
    )
    st.altair_chart(chart2, use_container_width=True)


col3, = st.columns(1)

with col3:
    st.subheader("User Frequency")
    chart3 = alt.Chart(user_frequency_data).mark_line(point=True).encode(
        x='Day',
        y='ActiveUsers'
    )
    st.altair_chart(chart3, use_container_width=True)


# # summary stats
# st.markdown("---")
# st.write("**AVERAGE USER ENGAGEMENT TIME:** 15 min")
# st.write("**TOTAL USERS:** 12,345")
# st.write("**TOTAL RESTAURANTS:** 2,345")
# st.write("**TOTAL INFLUENCERS:** 234")