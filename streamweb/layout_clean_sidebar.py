import streamlit as st
import sys
from typing import List
from types import ModuleType

# import utils.utils as utils
from utils.siteutils import (
    load_content,
    render_content_by_click,
    render_content_by_key,
)


def render_home_content(content: List[ModuleType]) -> None:
    title_col1, title_col2 = st.beta_columns([2, 1])
    title_col1.header("Posts")

    search_text = title_col2.text_input("Search Posts", "")

    for module in content:
        display = True
        if search_text:
            if search_text.lower() not in module.long_title.lower():
                display = False
        if display:
            expander = st.beta_expander(module.long_title)
            with expander:
                module.render()


def create_buttons(
    content: List[ModuleType], number_items_to_display: int
) -> List[bool]:
    # this is a workaround since it doesn't appear possible to
    # get the key of the button that was clicked
    # https://discuss.streamlit.io/t/how-to-use-the-key-field-in-interactive-widgets-api/1007
    button_click_flags = []
    for c in content[:number_items_to_display]:
        button_click_flags.append(st.sidebar.button(c.short_title, key=c.key))
    return button_click_flags


website_title = "Web Site Name"
author_name = "YOUR NAME"
recent_dynamic_content_list_length = 3

st.set_page_config(layout="wide")

environment = None
if len(sys.argv) > 1:
    environment = sys.argv[1]

content_id = None
query_params = st.experimental_get_query_params()
if "content" in query_params:
    content_id = query_params["content"][0]


static_content = load_content("static", environment)
dynamic_content = load_content("dynamic", environment)

st.title(website_title)

home_button = st.sidebar.button("home")

static_content_button_click = create_buttons(static_content, len(static_content))

st.sidebar.subheader("")
st.sidebar.subheader("Recent Posts")
dynamic_content_button_click = create_buttons(
    dynamic_content, recent_dynamic_content_list_length
)

# navigation logic -determines what to display in the main content area
if home_button:
    # the home_button was clicked
    st.experimental_set_query_params()
    render_home_content(content=dynamic_content)
elif any(static_content_button_click):
    # static content button was clicked
    st.experimental_set_query_params()
    render_content_by_click(
        content=static_content,
        button_click=static_content_button_click,
        environment=environment,
    )
elif any(dynamic_content_button_click):
    # dynamic content button was clicked
    content_id = render_content_by_click(
        content=dynamic_content,
        button_click=dynamic_content_button_click,
        environment=environment,
    )
    # set the content_id in the URL in case the user wants to bookmark
    st.experimental_set_query_params(content=content_id)
elif content_id:
    # the url contains a content_id (bookmark or direct link to page)
    render_content_by_key(
        content=dynamic_content, content_key=content_id, environment=environment
    )
else:
    # the user browsed to the home page (didn't click the home button)
    st.experimental_set_query_params()
    render_home_content(content=dynamic_content)


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
