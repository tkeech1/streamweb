import streamlit as st
import datetime

title = "1st Post"
key = 1
post_date = datetime.date(2021, 4, 1)


def render():
    st.markdown(f"## [{title}](/?post={key})")
    st.write(post_date)

    st.write(
        "Lorem ipsum dolor sit amet, consectetur adipiscing"
        " elit, sed do eiusmod tempor incididunt ut labore et"
        " dolore magna aliqua. Ut enim ad minim veniam, quis "
        "nostrud exercitation ullamco laboris nisi ut aliquip "
        "ex ea commodo consequat. Duis aute irure dolor in "
        "reprehenderit in voluptate velit esse cillum dolore "
        "eu fugiat nulla pariatur. Excepteur sint occaecat "
        "cupidatat non proident, sunt in culpa qui officia "
        "deserunt mollit anim id est laborum."
    )
