import streamlit as st
import datetime
import pytz
import pandas as pd
import numpy as np
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
def render():
    st.header(f"{long_title}")
    st.markdown(content_date.strftime("%m/%d/%Y %H:%M:%S %Z"))

    data_load_state = st.text("Loading data...")

    data = load_data().drop("ms", axis=1)

    st.write(data.tail())

    data_load_state.text("")

    st.subheader("Page Views")
    st.write(data["page"].value_counts())

    data = data.groupby(by="page")

    st.write("")

    st.subheader("Mean")
    st.write(data.mean())

    st.subheader("Median")
    st.write(data.median())

    st.subheader("Max")
    st.write(data["runtime"].max())

    st.subheader("Max")
    st.write(data["requesttime"].max())

    del data
