import streamlit as st
import datetime
import pytz
import pandas as pd
from utils.metrics import log_runtime

short_title = "metrics"
long_title = "Web Site Metrics"
key = 345
content_date = datetime.datetime(2021, 1, 1).astimezone(pytz.timezone("US/Eastern"))

DATE_COLUMN = "date/time"


def load_data():
    data = pd.read_csv(
        "perf_metrics.log",
        names=[
            "datetime",
            "ms",
            "page",
            "runtime",
            "useragent",
            "origin",
            "remoteip",
            "uri",
            "path",
            "query",
            "host",
            "fullurl",
            "requesttime",
        ],
    )
    return data


@log_runtime
def render(location):
    location.header(f"{long_title}")
    location.markdown(content_date.strftime("%m/%d/%Y %H:%M:%S %Z"))

    data_load_state = location.text("Loading data...")

    data = load_data().drop("ms", axis=1)

    location.write(data.tail())

    data_load_state.text("")

    location.subheader("Page Views")
    location.write(data["page"].value_counts())

    data = data.groupby(by="page")

    location.write("")

    location.subheader("Mean")
    location.write(data.mean())

    location.subheader("Median")
    location.write(data.median())

    location.subheader("Max")
    location.write(data["runtime"].max())

    location.subheader("Max")
    location.write(data["requesttime"].max())

    del data
