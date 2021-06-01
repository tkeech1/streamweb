import streamlit as st
import datetime
import pytz
from utils.metrics import log_runtime

short_title = "1st post"
long_title = "1st Post"
key = 1
content_date = datetime.datetime(2021, 4, 1).astimezone(pytz.timezone("US/Eastern"))


@log_runtime
def render(location: st):
    location.markdown(f"## [{long_title}](/?content={key})")
    location.write(content_date.strftime("%m/%d/%Y"))

    location.write(
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
