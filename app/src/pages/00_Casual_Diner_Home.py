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



# search bar
search_query = st.text_input("Search", placeholder="Search restaurants, cuisines, etc.")

if search_query:
    st.write(f"You searched for: {search_query}")
    # TODO: Connect to API or DB to show real search results

st.markdown("---")



# recs nearby pop up
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
    
# trending pop up
@st.dialog("Trending Restaurants")
def show_trending_dialog():
    
    df = pd.DataFrame(
    rng(0).standard_normal(size=(10, 2)),
    columns=("Name", "Rating"),
)

    st.dataframe(df, hide_index=True)

# friend recs pop up
@st.dialog("Friend Recommendations")
def show_friendrecs_diaglog():

    df = pd.DataFrame(
        rng(0).standard_normal(size=(10,3)),
        columns=("Friend", "Restaurant", "Rating")
    )

    st.dataframe(df, hide_index=True)

# Create columns with custom spacing (gap between buttons)
col1, col2, col3, col4, col5, col6, col7 = st.columns([0.01, 0.5, 0.1, 0.5, 0.1, 0.5, 2])

with col2:
    if st.button("Recs Nearby", use_container_width=True):
        show_recommendations_dialog()

with col4:
    if st.button("Trending", use_container_width=True):
        show_trending_dialog()

with col6:
    if st.button("Friend Recs", use_container_width=True):
        show_friendrecs_diaglog()



st.write("")
st.write("")


#post feed
st.write("### Posts Feed (w/ sample data, need API)")


# rectangle for posts
st.markdown("""
<style>
.rounded-rect {
    background-color: #f0f2f6;
    border-radius: 15px;
    padding: 20px;
    margin: 10px 0; /* space between posts */
    border: 2px solid #ddd;
    display: flex;
    flex-direction: column;
    gap: 10px;
}
.post-author {
    font-weight: bold;
    font-size: 16px;
}
.post-content {
    font-size: 14px;
}
</style>
""", unsafe_allow_html=True)

# sample posts data
posts = [
    {"author": "Tiffany", "content": "Loved the spicy ramen at Sushi Zen!", "image_url": "https://via.placeholder.com/600x400"},
    {"author": "Billy", "content": "Check out the new vegan place downtown!", "image_url": None},
    {"author": "Alice", "content": "Had an amazing burger at Burger Barn 🍔", "image_url": "https://via.placeholder.com/600x400"},
]

# display posts stacked vertically
for post in posts:
    st.markdown(f"""
    <div class="rounded-rect">
        <div class="post-author">{post['author']}</div>
        <div class="post-content">{post['content']}</div>
        {"<img src='" + post['image_url'] + "' width='100%' style='border-radius: 10px;'/>" if post['image_url'] else ""}
    </div>
    """, unsafe_allow_html=True)
