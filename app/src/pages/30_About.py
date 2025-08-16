import streamlit as st
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

SideBarLinks()

st.write("# About this App")

st.markdown(
    """
    We’re building Tummi, a data-driven food discovery app that helps users track their restaurant visits, rate dishes, and receive recommendations. It also allows users to add friends to see which restaurants their friends have visited and recommend. This app is important because it enhances users’ experience with finding new restaurants and foods. Traditional food review platforms often are cluttered, impersonal, and outdated. Users are typically overwhelmed by hundreds/thousands of anonymous reviews and generic star ratings. Tummi solves these pain points.

    """
)

# Add a button to return to home page
if st.button("Return to Home", type="primary"):
    st.switch_page("Home.py")
