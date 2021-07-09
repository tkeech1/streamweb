import streamlit as st
import logging
import site_config
from utils.siteutils import StreamwebSite
from utils.metrics import log_runtime

st.set_page_config(layout="wide")
# st.set_page_config(layout="centered")

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def main(sws: StreamwebSite, content_id: str):

    sws.load_content("static")
    sws.load_content("dynamic")

    st.title(sws.website_title)

    home_button = st.sidebar.button("home")

    static_content_button_click = sws.create_buttons("static", st.sidebar)
    st.sidebar.subheader("")

    st.sidebar.subheader("")
    st.sidebar.subheader("Recent Posts")
    dynamic_content_button_click = sws.create_buttons("dynamic", st.sidebar, 3)

    @log_runtime
    def home(location: st, sws: StreamwebSite):

        location.markdown(sws.website_description)

        location.header("Posts")

        sws.create_link_list(content_name="dynamic", location=location, search_text="")

        location.subheader("")
        location.markdown(
            f"[RSS]({sws.rss_feed['dynamic']}) | [Atom]({sws.atom_feed['dynamic']})"
        )

    # main_col, _ = st.beta_columns([2, 1])

    # navigation logic - determines what to display in the main content area
    if home_button:
        # the home_button was clicked
        st.experimental_set_query_params()
        home(st, sws)
    elif any(static_content_button_click):
        # static content button was clicked
        st.experimental_set_query_params()
        sws.render_content_by_click(
            content_name="static",
            location=st,
            button_click=static_content_button_click,
        )
    elif any(dynamic_content_button_click):
        # dynamic content button was clicked
        cid = sws.render_content_by_click(
            content_name="dynamic",
            location=st,
            button_click=dynamic_content_button_click,
        )
        # set the content_id in the URL in case the user wants to bookmark
        st.experimental_set_query_params(content=cid)
    elif content_id:
        # the url contains a content_id (bookmark or direct link to page)
        sws.render_content_by_key("dynamic", location=st, content_key=content_id)
    else:
        # the user browsed to the home page (didn't click the home button)
        st.experimental_set_query_params()
        home(st, sws)

    # workaround to hide hamburger menu, header and footer
    # https://github.com/streamlit/streamlit/issues/395
    hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        </style>
        """
    # hide footer
    # footer {visibility: hidden;}
    st.markdown(hide_menu_style, unsafe_allow_html=True)
    # end workaround to hide hamburger menu


sws: StreamwebSite = StreamwebSite(
    site_config.website_id,
    site_config.website_title,
    site_config.website_description,
    site_config.website_author,
    site_config.website_url,
    site_config.website_language,
)

content_id = ""
query_params = st.experimental_get_query_params()
if "content" in query_params:
    content_id = query_params["content"][0]

main(sws, content_id)
