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

try:
    ad_performance = requests.get(f"http://api:4000/ro/3/ad_performance").json()
    audience_insights = requests.get("http://api:4000/ro/audience_insights").json()
    feature_engagement = requests.get(f"http://api:4000/ro/2/feature_engagement").json()
    
    Analytics, Ad_Campaigns = st.tabs(["Analytics", "Ad Campaigns"])

    with Analytics:

        if audience_insights:
            audience_insights_data = pd.DataFrame(audience_insights)
        
            audience_insights_data = audience_insights_data.rename(columns={
                'NumUsers': 'Users',
                'Location': 'Location'
            })
        else:
            audience_insights_data = pd.DataFrame({'Location': [], 'Users': []})

        if feature_engagement:
            feature_engagement_df = pd.DataFrame(feature_engagement)
    
            feature_engagement_data = pd.DataFrame({
                'Feature': ['Rating', 'Saves', 'Visits', 'Posts'],
                'Engagement': [
                    feature_engagement_df['Rating'].iloc[0] if len(feature_engagement_df) > 0 else 0,
                    feature_engagement_df['NumSaves'].iloc[0] if len(feature_engagement_df) > 0 else 0,
                    feature_engagement_df['NumVisits'].iloc[0] if len(feature_engagement_df) > 0 else 0,
                    feature_engagement_df['NumInfPost'].iloc[0] if len(feature_engagement_df) > 0 else 0
                ]
            })
        else:
            feature_engagement_data = pd.DataFrame({'Feature': [], 'Engagement': []})

        # Create graphs with real data
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Feature Engagement")
            if not feature_engagement_data.empty:
                chart1 = alt.Chart(feature_engagement_data).mark_bar().encode(
                    x=alt.X('Feature', sort='-y'),
                    y='Engagement',
                    color='Feature'
                )
                st.altair_chart(chart1, use_container_width=True)
            else:
                st.write("No feature engagement data available")

        with col2:
            st.subheader("Audience Insights (by Location)")
            if not audience_insights_data.empty:
                chart2 = alt.Chart(audience_insights_data).mark_bar().encode(
                    x=alt.X('Location', sort='-y'),
                    y='Users',
                    color='Location'
                )
                st.altair_chart(chart2, use_container_width=True)
            else:
                st.write("No audience insights data available")

        col3, col4 = st.columns(2)

    with Ad_Campaigns:
        st.subheader("Ad Campaign Performance")
        
        if ad_performance and isinstance(ad_performance, list):
            for post in ad_performance:
                campaignId = post.get('CampaignId')
                AdCost = post.get('AdCost')
                Revenue = post.get('Revenue')
                Profit = post.get('Profit')
                
                st.write(f"**Campaign ID:** {campaignId}")
                st.write(f"**Ad Cost:** ${AdCost}")
                st.write(f"**Ad Revenue:** ${Revenue}")
                st.write(f"**Ad Profit:** ${Profit}")
                st.divider()
        else:
            st.write("No ad campaign data found.")

except requests.exceptions.RequestException as e:
    st.error(f"Error fetching data from API: {e}")
except Exception as e:
    st.error(f"Error processing data: {e}")