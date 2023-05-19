from altair.vegalite.v4.schema.core import TimeUnit
import streamlit as st
import datetime
import pytz
import pandas as pd
import altair as alt
from utils.metrics import log_runtime

short_title = "metrics"
long_title = "Site Metrics"
key = 345
content_date = datetime.datetime(2021, 1, 1).astimezone(pytz.timezone("US/Eastern"))

DATE_COLUMN = "date/time"


def load_data():
    data = pd.read_csv(
        "/home/python/streamweb-logs/perf_metrics.log",
        names=[
            "datetime",
            "ms",
            "page",
            "runtime",
        ],
    )
    return data


@log_runtime
def render(location):
    location.header(f"{long_title}")
    # location.markdown(content_date.strftime("%m/%d/%Y %H:%M:%S %Z"))
    data_load_state = location.text("Loading data...")
    data = load_data().drop("ms", axis=1)
    data_load_state.text("")

    heading_font_size = 20
    title_font_size = 14
    label_font_size = 12
    width = 650
    height = 500

    data["date"] = data["datetime"].apply(lambda x: x.split(" ")[0])

    # count_by_day = (
    #     (data[["date", "page", "datetime"]].groupby(by=["date", "page"]).count())
    #     .reset_index()
    #     .rename(columns={"datetime": "Count", "page": "Page", "date": "Date"})
    # )

    # selection = alt.selection_single(fields=["Page"], bind="legend")
    # chart = (
    #     (
    #         alt.Chart(count_by_day)
    #         .mark_line(tooltip=True, point=True)
    #         .encode(
    #             alt.X("Date", title="Date", timeUnit="yearmonthdate"),
    #             alt.Y("Count", title="Hits"),
    #             color="Page",
    #             opacity=alt.condition(selection, alt.value(1), alt.value(0.2)),
    #         )
    #     )
    #     .add_selection(selection)
    #     .properties(width=width, height=height, title="Hits by Date")
    #     .configure_axis(labelFontSize=label_font_size, titleFontSize=title_font_size)
    #     .configure_legend(titleFontSize=title_font_size, labelFontSize=label_font_size)
    #     .configure_title(
    #         fontSize=heading_font_size,
    #     )
    #     .interactive()
    # )
    # location.write(chart)

    # st.markdown("""---""")

    # chart = (
    #     (
    #         alt.Chart(
    #             data["page"]
    #             .value_counts()
    #             .reset_index()
    #             .rename(columns={"count": "Hits", "page": "Page"})
    #         )
    #         .mark_bar(tooltip=True)
    #         .encode(
    #             alt.X("Page", title="Page"),
    #             alt.Y("Hits", title="Hits"),
    #             color="Page",
    #             tooltip=["Page", "Hits"],
    #         )
    #     )
    #     .properties(width=width, height=height, title="Total Hits")
    #     .configure_axis(labelFontSize=label_font_size, titleFontSize=title_font_size)
    #     .configure_legend(titleFontSize=title_font_size, labelFontSize=label_font_size)
    #     .configure_title(
    #         fontSize=heading_font_size,
    #     )
    # )
    # location.write(chart)

    # st.markdown("""---""")

    selection = alt.selection_single(fields=["Page"], bind="legend")
    chart = (
        (
            alt.Chart(
                data[["datetime", "page", "runtime"]].rename(
                    columns={
                        "page": "Page",
                        "runtime": "Runtime",
                        "datetime": "Date & Time",
                    }
                )
            )
            .mark_circle(tooltip=True)
            .encode(
                alt.X(
                    "Date & Time",
                    title="Date & Time",
                    axis=alt.Axis(tickCount=10, grid=False, labels=False),
                ),
                alt.Y(
                    "Runtime:Q",
                    title="Runtime",
                ),
                color="Page",
                tooltip=["Date & Time", "Page", "Runtime"],
                opacity=alt.condition(selection, alt.value(1), alt.value(0.2)),
            )
        )
        .add_selection(selection)
        .properties(width=width, height=height, title="Runtime by Page")
        .configure_axis(labelFontSize=label_font_size, titleFontSize=title_font_size)
        .configure_legend(titleFontSize=title_font_size, labelFontSize=label_font_size)
        .configure_title(
            fontSize=heading_font_size,
        )
        .interactive()
    )
    location.write(chart)

    st.markdown("""---""")

    chart = (
        (
            alt.Chart(
                data
                .reset_index()
                .rename(columns={"page": "Page", "runtime": "Runtime"})
            )
            .mark_bar(tooltip=True)
            .encode(
                alt.X("Page", title="Page"),
                alt.Y("median(Runtime)", title="Runtime"),
                color="Page",
                tooltip=["Page", "Runtime"],
            )
        )
        .properties(width=width, height=height, title="Median Runtime")
        .configure_axis(labelFontSize=label_font_size, titleFontSize=title_font_size)
        .configure_legend(titleFontSize=title_font_size, labelFontSize=label_font_size)
        .configure_title(
            fontSize=heading_font_size,
        )
    )
    location.write(chart)

    del data
