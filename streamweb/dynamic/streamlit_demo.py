import streamlit as st
import datetime
import pytz
import pandas as pd
import numpy as np
from utils.metrics import log_runtime

long_title = "Streamlit Example Dashboard"
short_title = "Streamlit Example Dashboard"
key = 4
content_date = datetime.datetime(2021, 4, 8).astimezone(pytz.timezone("US/Eastern"))


@log_runtime
def render(location: st):
    location.markdown(f"## [{long_title}](/?content={key})")
    location.write(content_date.strftime("%m/%d/%Y"))
    location.write("A Data Table:")

    df = pd.DataFrame({"first column": [1, 2, 3, 4], "second column": [10, 20, 30, 40]})

    location.write(df)

    location.line_chart(df)

    if location.checkbox("Show random chart"):
        chart_data2 = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])
        location.line_chart(chart_data2)

    option = location.selectbox("Which number do you like best?", df["first column"])

    location.write("You selected: ", option)

    location.write("Columns")
    left_column, right_column = st.beta_columns(2)
    pressed = left_column.button("Press me?")
    if pressed:
        right_column.write("Woohoo!")

    progress_bar = location.progress(0)
    status_text = location.empty()
    chart = location.line_chart(np.random.randn(10, 2))
