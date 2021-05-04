import streamlit as st
import datetime
import pytz
import pandas as pd
import numpy as np

long_title = "Streamlit Example Dashboard"
short_title = "Streamlit Example Dashboard"
key = 4
content_date = datetime.datetime(2021, 4, 8).astimezone(pytz.timezone("US/Eastern"))


def render():
    st.markdown(f"## [{long_title}](/?content={key})")
    st.write(content_date.strftime("%m/%d/%Y"))
    st.write("A Data Table:")

    df = pd.DataFrame({"first column": [1, 2, 3, 4], "second column": [10, 20, 30, 40]})

    st.write(df)

    st.line_chart(df)

    if st.checkbox("Show random chart"):
        chart_data2 = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])
        st.line_chart(chart_data2)

    option = st.selectbox("Which number do you like best?", df["first column"])

    st.write("You selected: ", option)

    st.write("Columns")
    left_column, right_column = st.beta_columns(2)
    pressed = left_column.button("Press me?")
    if pressed:
        right_column.write("Woohoo!")

    progress_bar = st.progress(0)
    status_text = st.empty()
    chart = st.line_chart(np.random.randn(10, 2))

    """for i in range(100):
        # Update progress bar.
        progress_bar.progress(i + 1)

        new_rows = np.random.randn(10, 2)

        # Update status text.
        status_text.text("The latest random number is: %s" % new_rows[-1, 1])

        # Append data to the chart.
        chart.add_rows(new_rows)

        import time

        # Pretend we're doing some computation that takes time.
        time.sleep(0.1)

    status_text.text("Done!")
    st.balloons()
    """
