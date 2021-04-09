import streamlit as st
import about, contact, home, post
import utils

website_title = "Web Site Name"
author_name = "YOUR NAME"

st.set_page_config(layout="wide")

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

post_modules = utils.load_post_modules()

# this is a workaround since it doesn't appear possible to
# get the key of the button that was clicked
# https://discuss.streamlit.io/t/how-to-use-the-key-field-in-interactive-widgets-api/1007
recent_posts_button_click = []
recent_posts = []
for i in range(min(len(post_modules), 3)):
    recent_posts_button_click.append(
        st.sidebar.button(post_modules[i].title, key=post_modules[i].key)
    )
    recent_posts.append(post_modules[i])

if about_button:
    st.experimental_set_query_params()
    about.render(name=author_name)
elif contact_button:
    st.experimental_set_query_params()
    contact.render(name=author_name)
elif home_button:
    st.experimental_set_query_params()
    home.render(post_modules=post_modules)
elif any(recent_posts_button_click):
    st.experimental_set_query_params()
    post.render(
        post_modules=recent_posts,
        recent_posts_button_click=recent_posts_button_click,
        post_id=None,
    )
elif post_id:
    post.render(
        post_modules=post_modules,
        recent_posts_button_click=None,
        post_id=post_id,
    )
else:
    home.render(post_modules=post_modules)

# hack to hide hamburger menu, header and footer
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
# end hack to hide hamburger menu
