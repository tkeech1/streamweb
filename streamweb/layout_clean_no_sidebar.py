import streamlit as st
import logging
import site_config
from utils.siteutils import StreamwebSite

st.set_page_config(layout="centered")

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def main(sws: StreamwebSite, content_id: str):

    sws.load_content("static")
    sws.load_content("dynamic")

    st.markdown(
        f"# <a href='/' target='_self'>{sws.website_title}</a>",
        unsafe_allow_html=True,
    )

    if content_id:
        # the url contains a content_id (bookmark or direct link to page)
        sws.render_content_by_key("dynamic", location=st, content_key=content_id)
    else:
        # the user browsed to the home page (didn't click the home button)
        st.experimental_set_query_params()
        sws.create_link_list(content_name="dynamic", location=st, item_label="Posts")

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
    site_config.environment,
)

content_id = ""
query_params = st.experimental_get_query_params()
if "content" in query_params:
    content_id = query_params["content"][0]

main(sws, content_id)
