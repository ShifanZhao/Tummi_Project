import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Welcome Casual Diner, {st.session_state['first_name']}.")
st.write('')
st.write('')
st.write('### What would you like to do today?')



if search_query:
    st.write(f"Searching for: **{search_query}**")
    # TODO: Connect to API or DB to show real search results

st.markdown("---")



st.markdown("# Explore")
st.sidebar.header("Explore")

@st.dialog("Recommendations Nearby")
def show_recommendations_dialog():
    
    df = pd.DataFrame({
    'Name': ["Test"],
    'lat': [42.361145],
    'lon': [-71.057083],
    })

    st.map(df)

    st.write("Restaurants:")
    st.dataframe(df, hide_index=True)
    
    
@st.dialog("Trending Restaurants")
def show_trending_dialog():
    
    df = pd.DataFrame(
    rng(0).standard_normal(size=(10, 2)),
    columns=("Name", "Rating"),
)

    st.dataframe(df, hide_index=True)
    

if st.button("Recs Nearby", key="recs_btn"):
    show_recommendations_dialog()

if st.button("Trending", key="trending_btn"):
    show_trending_dialog()


st.write("### Posts Feed (w/ sample data, need API)")

# Sample posts data
posts = [
    {"author": "Tiffany", "content": "Loved the spicy ramen at Sushi Zen!", "image_url": "https://via.placeholder.com/600x400"},
    {"author": "Billy", "content": "Check out the new vegan place downtown!", "image_url": None},
    {"author": "Alice", "content": "Had an amazing burger at Burger Barn 🍔", "image_url": "https://via.placeholder.com/600x400"},
]
# TODO: connect with API to get real info


for post in posts:
    st.markdown(f"**{post['author']}**")
    st.write(post['content'])
    if post['image_url']:
        st.image(post['image_url'], width=300)
    st.markdown("---")