import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
import requests
import altair as alt
import numpy as np
import pandas as pd

st.set_page_config(layout = 'wide')

SideBarLinks()




st.title('Restaurant Analytics')
feed = requests.get("http://api:4000/ro/3/ad_performance").json()
try:
    if feed and isinstance(feed, list):
        for post in feed:
            Analytics, Ad_Campaigns = st.tabs(["Analytics", "Ad Campaigns"])

        with Analytics:
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

            # graphs
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

            
        with Ad_Campaigns:
            campaignId = post.get('CampaignId')
            AdCost = post.get('AdCost')
            Revenue = post.get('Revenue')
            Profit = post.get('Profit')
            st.write("##### Campaign Id:", campaignId)

            st.write("###### Ad Cost: $", AdCost)
            st.write("###### Ad Revenue: $", Revenue)
            st.write("###### Ad Profit: $", Profit)
            st.divider()
            
    else:
        st.write("No posts found.")

except Exception as e:
    st.error(f"Error displaying posts: {e}")