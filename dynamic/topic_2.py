import streamlit as st
import datetime

short_title = "text post"
long_title = "Text Post"
key = 2
content_date = datetime.date(2021, 4, 6)


def render():
    st.markdown(f"## [{long_title}](/?content={key})")
    st.write(content_date)
    st.write(
        "Lorem ipsum dolor sit amet, consectetur adipiscing"
        " elit, sed do eiusmod tempor incididunt ut labore et"
        " dolore magna aliqua. Ut enim ad minim veniam, quis "
        "nostrud exercitation ullamco laboris nisi ut aliquip "
        "ex ea commodo consequat. Duis aute irure dolor in "
        "reprehenderit in voluptate velit esse cillum dolore "
        "eu fugiat nulla pariatur. Excepteur sint occaecat "
        "cupidatat non proident, sunt in culpa qui officia "
        "deserunt mollit anim id est laborum. "
    )