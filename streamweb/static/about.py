import streamlit as st
import datetime
import pytz
from utils.metrics import log_runtime

long_title = "About Me"
short_title = "about"
key = 9998
content_date = datetime.datetime(2021, 4, 8).astimezone(pytz.timezone("US/Eastern"))


@log_runtime
def render(location: st):

    location.header(f"{long_title}")

    location.header(f"About This Site")
    location.markdown(
        "This site is built on the awesome [Streamlit](https://streamlit.io/) app framework. "
    )
