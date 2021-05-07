import streamlit as st
import datetime
import pytz

from utils.siteutils import load_content

long_title = "About"
short_title = "about"
key = 9998
content_date = datetime.datetime(2021, 4, 8).astimezone(pytz.timezone("US/Eastern"))


def render():

    st.header(f"{long_title}")

    content = load_content("dynamic/subpack", "", feed=True)

    for module in content:
        expander = st.beta_expander(module.long_title)
        with expander:
            module.render()

    st.subheader("")

    st.markdown(
        "[RSS](feeds/dynamic_subpack_rss.xml) | [Atom](feeds/dynamic_subpack_atom.xml)"
    )
