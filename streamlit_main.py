import streamlit as st
import about, contact, home, post
import utils
import sys

website_title = "Web Site Name"
author_name = "YOUR NAME"
recent_post_list_length = 3

st.set_page_config(layout="wide")

environment = None
if len(sys.argv) > 1:
    environment = sys.argv[1]

post_id = None
query_params = st.experimental_get_query_params()
if "post" in query_params:
    post_id = query_params["post"][0]

home_button = st.sidebar.button("home")
about_button = st.sidebar.button("about")
contact_button = st.sidebar.button("contact")

st.title(website_title)
st.sidebar.subheader("")
st.sidebar.subheader("Recent Posts")

post_modules_loader = utils.PostModuleLoader(
    package_name="posts", environment=environment
)
post_modules = utils.load_post_modules(post_modules_loader)

# this is a workaround since it doesn't appear possible to
# get the key of the button that was clicked
# https://discuss.streamlit.io/t/how-to-use-the-key-field-in-interactive-widgets-api/1007
recent_posts_button_click = []
for recent_post in post_modules[0:recent_post_list_length]:
    recent_posts_button_click.append(
        st.sidebar.button(recent_post.title, key=recent_post.key)
    )

if about_button:
    st.experimental_set_query_params()
    about.render()
elif contact_button:
    st.experimental_set_query_params()
    contact.render()
elif home_button:
    st.experimental_set_query_params()
    home.render(post_modules=post_modules)
elif any(recent_posts_button_click):
    post_id = post.render_recent_post(
        post_modules_loader=post_modules_loader,
        recent_posts_button_click=recent_posts_button_click,
    )
    st.experimental_set_query_params(post=post_id)
elif post_id:
    post.render_post(
        post_modules_loader=post_modules_loader,
        post_id=post_id,
    )
else:
    home.render(post_modules=post_modules)

# workaround to hide hamburger menu, header and footer
# https://github.com/streamlit/streamlit/issues/395
hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        </style>
        """
# hide footer
# footer {visibility: hidden;}
st.markdown(hide_menu_style, unsafe_allow_html=True)
# end workaround to hide hamburger menu