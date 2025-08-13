import logging
logger = logging.getLogger(__name__)

from modules.nav import SideBarLinks

import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

st.set_page_config(layout = 'wide')

SideBarLinks()

st.title('Analyst Dashboard')
st.write(f"Welcome, {st.session_state['first_name']} — Internal Analyst")
st.write("This dashboard lets you manage pending verifications, review flagged users and restaurants, and access app analytics.")


if st.button('Manage Permissions', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/32_Manage_Permissions.py')



# sample data - need to connect to API
feature_engagement_data = pd.DataFrame({
    'Feature': ['Search', 'Reviews', 'Likes', 'Bookmarks', 'Shares'],
    'Engagement': np.random.randint(100, 1000, size=5)
})

audience_insights_data = pd.DataFrame({
    'Location': ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Miami'],
    'Users': np.random.randint(500, 5000, size=5)
})

top_influencers_data = pd.DataFrame({
    'Influencer': [f'Influencer {i}' for i in range(1, 6)],
    'Followers': np.random.randint(1000, 5000, size=5)
})

user_frequency_data = pd.DataFrame({
    'Day': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
    'ActiveUsers': np.random.randint(200, 1000, size=7)
})


# 2x2 chart layout
col1, col2 = st.columns(2)

with col1:
    st.subheader("Feature Engagement")
    chart1 = alt.Chart(feature_engagement_data).mark_bar().encode(
        x=alt.X('Feature', sort='-y'),
        y='Engagement',
        color='Feature'
    )
    st.altair_chart(chart1, use_container_width=True)

with col2:
    st.subheader("Audience Insights (by Location)")
    chart2 = alt.Chart(audience_insights_data).mark_bar().encode(
        x=alt.X('Location', sort='-y'),
        y='Users',
        color='Location'
    )
    st.altair_chart(chart2, use_container_width=True)

col3, col4 = st.columns(2)

with col3:
    st.subheader("Top Influencers")
    chart3 = alt.Chart(top_influencers_data).mark_bar().encode(
        x=alt.X('Influencer', sort='-y'),
        y='Followers',
        color='Influencer'
    )
    st.altair_chart(chart3, use_container_width=True)

with col4:
    st.subheader("User Frequency")
    chart4 = alt.Chart(user_frequency_data).mark_line(point=True).encode(
        x='Day',
        y='ActiveUsers'
    )
    st.altair_chart(chart4, use_container_width=True)


# summary stats
st.markdown("---")
st.write("**AVERAGE USER ENGAGEMENT TIME:** 15 min")
st.write("**TOTAL USERS:** 12,345")
st.write("**TOTAL RESTAURANTS:** 2,345")
st.write("**TOTAL INFLUENCERS:** 234")