import streamlit as st


def render(post_modules=None):

    title_col1, title_col2 = st.beta_columns([2, 1])
    title_col1.header("Posts")

    search_text = title_col2.text_input("Search Posts", "")

    for m in post_modules:
        display = True
        if search_text:
            if search_text.lower() not in m.title.lower():
                display = False
        if display:
            expander = st.beta_expander(m.title)
            with expander:
                m.render()
