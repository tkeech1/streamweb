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
    title_col1, title_col2 = st.beta_columns([3, 2])
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


website_title = "Web Site Name"
author_name = "YOUR NAME"
recent_dynamic_content_list_length = 3

st.set_page_config(layout="centered")

environment = None
if len(sys.argv) > 1:
    environment = sys.argv[1]

content_id = None
query_params = st.experimental_get_query_params()
if "content" in query_params:
    content_id = query_params["content"][0]

st.title(website_title)

static_content = load_content("static", environment)

# this is a workaround since it doesn't appear possible to
# get the key of the button that was clicked
# https://discuss.streamlit.io/t/how-to-use-the-key-field-in-interactive-widgets-api/1007
static_content_button_click = []
[*button_columns] = st.beta_columns(len(static_content) + 6)
home_button = button_columns[0].button("home")
for content, button_column in zip(static_content, button_columns[1:]):
    static_content_button_click.append(
        button_column.button(content.short_title, key=content.key)
    )

dynamic_content = load_content("dynamic", environment)

if home_button:
    st.experimental_set_query_params()
    render_home_content(content=dynamic_content)
elif any(static_content_button_click):
    st.experimental_set_query_params()
    render_content_by_click(
        content=static_content,
        button_click=static_content_button_click,
    )
elif content_id:
    render_content_by_key(
        content=dynamic_content,
        content_key=content_id,
    )
else:
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
