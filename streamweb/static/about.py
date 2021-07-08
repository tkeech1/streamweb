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
    location.markdown(
        "I like to work on all types of applications, from web sites to computer vision. "
        "I currently work at [PJM Interconnection](https://pjm.com/) making sure PJM's markets "
        "and settlements systems run smoothly. PJM operates wholesale energy markets and "
        "manages the high-voltage electrical system serving over 65 million people in the mid-Atlantic region. "
    )

    location.header(f"About This Site")
    location.markdown(
        "This site is built on the awesome [Streamlit](https://streamlit.io/) app framework. "
        "I wrote [some code](https://github.com/tkeech1/streamweb) to use Streamlit "
        "as a web site. Feel free to try it out"
    )
