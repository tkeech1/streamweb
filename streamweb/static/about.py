import streamlit as st
import datetime

long_title = "About"
short_title = "about"
key = 9998
content_date = datetime.date(2021, 4, 8)


def render():
    st.header(f"{long_title}")