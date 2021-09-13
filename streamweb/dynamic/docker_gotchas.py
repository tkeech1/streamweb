import streamlit as st
import datetime
import pytz
from datetime import date
from utils.metrics import log_runtime

short_title = "A Few Docker Gotchas"
long_title = "A Few Docker Gotchas That Always Get Me"
key = 5
content_date = datetime.datetime(2021, 9, 12).astimezone(pytz.timezone("US/Eastern"))
assets_dir = "./assets/" + str(key) + '/'

@log_runtime
def render(location: st):
    location.markdown(f"## [{long_title}](/?content={key})")
    location.write(f"*{content_date.strftime('%m.%d.%Y')}*")

    