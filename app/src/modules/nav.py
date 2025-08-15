# Idea borrowed from https://github.com/fsmosca/sample-streamlit-authenticator

# This file has function to add certain functionality to the left side bar of the app

import streamlit as st


#### ------------------------ General ------------------------
def HomeNav():
    st.sidebar.page_link("Home.py", label="Home", icon="🏠")


def AboutPageNav():
    st.sidebar.page_link("pages/30_About.py", label="About", icon="🧠")


#### ------------------------ Casual Diner Persona ------------------------
def CasualDinerHomeNav():
    st.sidebar.page_link(
        "pages/00_Casual_Diner_Home.py", label="Home", icon="👤"
    )


def Leaderboard():
    st.sidebar.page_link(
        "pages/01_Leaderboard.py", label="Leaderboard", icon="🏦"
    )

def Explore():
    st.sidebar.page_link("pages/02_Explore.py", label="Explore", icon="🗺️")


def Bookmarked_CD():
    st.sidebar.page_link("pages/03_Bookmarked_CD.py", label="Bookmarked", icon="🗺️")


def CasualDinerProfile():
    st.sidebar.page_link("pages/04_Casual_Diner_Profile.py", label="Profile", icon="🗺️")


## ------------------------ Influencer Persona ------------------------
def InfluencerHomeNav():
    st.sidebar.page_link(
        "pages/05_Influencer_Home.py", label="Home", icon="👤"
    )


def Leaderboard():
    st.sidebar.page_link(
        "pages/01_Leaderboard.py", label="Leaderboard", icon="🏦"
    )

def Explore():
    st.sidebar.page_link("pages/02_Explore.py", label="Explore", icon="🗺️")


def Bookmarked_Inf():
    st.sidebar.page_link("pages/03_Bookmarked_Inf.py", label="Bookmarked", icon="🗺️")


def InfluencerProfile():
    st.sidebar.page_link("pages/06_Influencer_Profile.py", label="Profile", icon="🗺️")



#### ------------------------ Restaurant Owner Persona ------------------------
def RestaurantOwnerPageNav():
    st.sidebar.page_link("pages/07_Restaurant_Owner_Home.py", label="Home", icon="🖥️")
    st.sidebar.page_link(
        "pages/08_Restaurant_Profile.py", label="Restaurant Profile", icon="🏢")
    st.sidebar.page_link(
        "pages/09_Restaurant_Analytics.py", label="Restaurant Analytics", icon="🏢"
    )


#### ------------------------ Internal Analyst Persona ------------------------
def InternalAnalystPageNav():
    st.sidebar.page_link("pages/31_Analyst_Home.py", label="Analyst Dashboard", icon="🖥️")
    st.sidebar.page_link(
        "pages/32_Manage_Permissions.py", label="Permissions", icon="🏢")



# --------------------------------Links Function -----------------------------------------------
def SideBarLinks(show_home=False):
    """
    This function handles adding links to the sidebar of the app based upon the logged-in user's role, which was put in the streamlit session_state object when logging in.
    """

    # add a logo to the sidebar always
    st.sidebar.image("assets/logo.png", width=150)

    # If there is no logged in user, redirect to the Home (Landing) page
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.switch_page("Home.py")

    if show_home:
        # Show the Home page link (the landing page)
        HomeNav()

    # Show the other page navigators depending on the users' role.
    if st.session_state["authenticated"]:

        # casual diner
        if st.session_state["role"] == "casual_diner":
            CasualDinerHomeNav()
            Leaderboard()
            Explore()
            Bookmarked_CD()
            CasualDinerProfile()

        # influencer
        if st.session_state["role"] == "influencer":
            InfluencerHomeNav()
            Leaderboard()
            Explore()
            Bookmarked_Inf()
            InfluencerProfile()

        # restaurant owner
        if st.session_state["role"] == "restaurant_owner":
            RestaurantOwnerPageNav()

        # internal analyst
        if st.session_state["role"] == "internal_analyst":
            InternalAnalystPageNav()


    # Always show the About page at the bottom of the list of links
    AboutPageNav()

    if st.session_state["authenticated"]:
        # Always show a logout button if there is a logged in user
        if st.sidebar.button("Logout"):
            del st.session_state["role"]
            del st.session_state["authenticated"]
            st.switch_page("Home.py")
