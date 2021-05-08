import streamlit as st
import datetime
import pytz
from utils.metrics import log_runtime

long_title = "Contact"
short_title = "contact"
key = 9994
content_date = datetime.datetime(2021, 4, 7).astimezone(pytz.timezone("US/Eastern"))


@log_runtime
def render():
    st.header(f"{long_title}")
