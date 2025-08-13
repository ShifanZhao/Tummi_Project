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

# create columns with custom spacing (gap between buttons)
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
st.markdown("---")

# post feed
st.write("### Posts Feed (w/ sample data, need API)")

st.write("### Add a Comment")

# comment box for users
comment = st.text_area(
    "",
    placeholder="Write a post...",
    max_chars=300
)

# image upload
image_file = st.file_uploader(
    "Add a picture (optional):",
    type=["jpg", "jpeg", "png"]
)

# submit button
if st.button("Post Review"):
    if comment.strip() == "" and image_file is None:
        st.warning("Please write a review or add an image before posting.")
    else:
        st.success("Your post has been posted!")
        
        # Display posted comment
        st.write(f"**You wrote:** {comment}")
        
        if image_file is not None:
            st.image(image_file, caption="Uploaded Image", use_column_width=True)


# rectangle for posts
st.markdown("""
<style>
.rounded-rect {
    background-color: #f0f2f6;
    border-radius: 15px;
    padding: 20px;
    margin: 10px 0;
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
.post-img {
    width: 100%;
    max-width: 500px;
    border-radius: 10px;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# sample posts data in session state
if "posts" not in st.session_state:
    st.session_state["posts"] = [
        {"author": "Tiffany", "content": "Loved the spicy ramen at Sushi Zen!", "image_url": "https://via.placeholder.com/600x400", "comments": []},
        {"author": "Billy", "content": "Check out the new vegan place downtown!", "image_url": None, "comments": []},
        {"author": "Alice", "content": "Had an amazing burger at Burger Barn 🍔", "image_url": "https://via.placeholder.com/600x400", "comments": []},
    ]

for i, post in enumerate(st.session_state["posts"]):
    st.markdown(f"""
    <div class="rounded-rect">
        {"<img class='post-img' src='" + post['image_url'] + "'/>" if post['image_url'] else ""}
        <div class="post-author">{post['author']}</div>
        <div class="post-content">{post['content']}</div>
    </div>
    """, unsafe_allow_html=True)

    # comment box
    comment_text = st.text_area(
        label="", 
        placeholder="Write a comment...",
        key=f"comment_{i}",
        max_chars=300
    )

    if st.button("Post Comment", key=f"btn_{i}"):
        if comment_text.strip() == "":
            st.warning("Please write a comment.")
        else:
            st.session_state["posts"][i]["comments"].append({"text": comment_text})
            st.success("Your comment has been posted!")

    # display comments
    if st.session_state["posts"][i]["comments"]:
        with st.expander(f"View {len(st.session_state['posts'][i]['comments'])} Comment(s)"):
            for c in st.session_state["posts"][i]["comments"]:
                st.write(c["text"])
