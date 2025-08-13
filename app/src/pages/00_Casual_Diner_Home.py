import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

# why do we need pd and rng?

feed = requests.get('http://api:4000/cd/CDPost/1').json()

try:
    st.dataframe(feed)
except:
    st.write('Could not connect to database to get feed')

st.set_page_config(layout = 'wide')
API_BASE = "http://localhost:4000"

if "user_id" not in st.session_state:
    st.session_state["user_id"] = 1
if "first_name" not in st.session_state:
    st.session_state["first_name"] = "Casual Diner"


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

# create columns
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


# adding API
def fetch_posts(user_id):
    try:
        response = requests.get(f"{API_BASE}/cd/CDPost/{user_id}")
        response.raise_for_status()
        posts = response.json()
        
        # check if the API returned the "Sadly" msg
        if isinstance(posts, dict) and "Sadly" in posts:
            return []

        formatted_posts = []
        for p in posts:
            formatted_posts.append({
                "PostId": p.get("PostId"),
                "author": f"CD {p.get('CDId')}",
                "content": f"Rating: {p.get('rating')}, Likes: {p.get('Likes')}",
                "image_url": None,
                "comments": []
            })
        return formatted_posts
    except Exception as e:
        st.error(f"Error fetching posts: {e}")
        return []

def post_review(user_id, caption, rating=5, rest_id=1):
    data = {"Rating": rating, "Caption": caption, "RestId": rest_id}
    try:
        response = requests.post(f"{API_BASE}/cd/{user_id}/createpost", json=data)
        if response.status_code == 201:
            return True
        else:
            st.error(f"Failed to post: {response.json()}")
            return False
    except Exception as e:
        st.error(f"Error posting review: {e}")
        return False

def like_post(post_id):
    try:
        response = requests.put(f"{API_BASE}/cd/CDPost", json={"PostId": post_id})
        if response.status_code == 200:
            st.success("Post liked!")
            return True
        else:
            st.error("Failed to like post")
            return False
    except Exception as e:
        st.error(f"Error liking post: {e}")
        return False


# post feed
st.write("### Posts Feed")

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
        if post_review(st.session_state['user_id'], comment):
            st.success("Your post has been posted!")
            st.session_state["posts"] = fetch_posts(st.session_state['user_id'])
        
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
    flex-direction: row; /* row layout */
    gap: 20px;
    align-items: flex-start;
}
.post-text {
    flex: 1; /* take remaining space */
    display: flex;
    flex-direction: column;
    gap: 5px;
}
.post-author {
    font-weight: bold;
    font-size: 16px;
}
.post-content {
    font-size: 14px;
}
.post-img {
    width: 150px;  /* smaller image */
    height: 100px; /* fixed height */
    object-fit: cover;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)


# get posts
if "posts" not in st.session_state:
    if st.session_state["user_id"]:
        st.session_state["posts"] = fetch_posts(st.session_state["user_id"])
    else:
        st.session_state["posts"] = []



for i, post in enumerate(st.session_state["posts"]):
    st.markdown(f"""
    <div class="rounded-rect">
        <div class="post-text">
            <div class="post-author">{post['author']}</div>
            <div class="post-content">{post['content']}</div>
        </div>
        {"<img class='post-img' src='" + post['image_url'] + "'/>" if post['image_url'] else ""}
    </div>
    """, unsafe_allow_html=True)

    # like button
    if st.button("Like", key=f"like_{i}"):
        if like_post(post["PostId"]):
            st.session_state["posts"] = fetch_posts(st.session_state['user_id'])


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
