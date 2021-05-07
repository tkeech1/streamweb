import streamlit as st
import datetime
import pytz

long_title = "Contact"
short_title = "contact"
key = 9994
content_date = datetime.datetime(2021, 4, 7).astimezone(pytz.timezone("US/Eastern"))


def render():
    st.header(f"{long_title}")
