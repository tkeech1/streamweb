import streamlit as st
import utils.utils as utils

title = "home"
key = 9999


def render(content_loader=None):

    title_col1, title_col2 = st.beta_columns([2, 1])
    title_col1.header("Posts")

    search_text = title_col2.text_input("Search Posts", "")

    dynamic_content = utils.load_modules(content_loader)

    for m in dynamic_content:
        display = True
        if search_text:
            if search_text.lower() not in m.title.lower():
                display = False
        if display:
            expander = st.beta_expander(m.title)
            with expander:
                m.render()
