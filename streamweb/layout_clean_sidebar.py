import streamlit as st
import logging
import site_config
from utils.siteutils import StreamwebSite
from utils.metrics import log_runtime

st.set_page_config(layout="wide")

logger = logging.getLogger()
logger.setLevel(logging.INFO)

sws: StreamwebSite = StreamwebSite(
    site_config.website_id,
    site_config.website_title,
    site_config.website_description,
    site_config.website_author,
    site_config.website_url,
    site_config.website_language,
    site_config.environment,
)


def home():
    @log_runtime
    def render_home_content(content_name: str) -> None:
        title_col1, title_col2 = st.beta_columns([2, 1])
        title_col1.header("Posts")

        search_text = title_col2.text_input("Search Posts", "")

        for module in sws.content_modules[content_name]:
            display = True
            if search_text:
                if search_text.lower() not in module.long_title.lower():
                    display = False
            if display:
                link = (
                    f"<a href='/?content={module.key}' target='_self'>"
                    f"{module.long_title}</a>"
                )
                st.markdown(
                    f'{module.content_date.strftime("%Y.%m.%d")} - {link}',
                    unsafe_allow_html=True,
                )

        st.subheader("")
        st.markdown(
            f"[RSS]({sws.rss_feed[content_name]}) | [Atom]({sws.atom_feed[content_name]})"
        )

    content_id = None
    query_params = st.experimental_get_query_params()
    if "content" in query_params:
        content_id = query_params["content"][0]

    sws.load_content("static")
    sws.load_content("dynamic")

    st.title(site_config.website_title)

    home_button = st.sidebar.button("home")

    static_content_button_click = sws.create_buttons("static")

    st.sidebar.subheader("")
    st.sidebar.subheader("Recent Posts")
    dynamic_content_button_click = sws.create_buttons("dynamic", 3)

    # navigation logic -determines what to display in the main content area
    if home_button:
        # the home_button was clicked
        st.experimental_set_query_params()
        render_home_content(content_name="dynamic")
    elif any(static_content_button_click):
        # static content button was clicked
        st.experimental_set_query_params()
        sws.render_content_by_click(
            "static",
            button_click=static_content_button_click,
        )
    elif any(dynamic_content_button_click):
        # dynamic content button was clicked
        content_id = sws.render_content_by_click(
            content_name="dynamic",
            button_click=dynamic_content_button_click,
        )
        # set the content_id in the URL in case the user wants to bookmark
        st.experimental_set_query_params(content=content_id)
    elif content_id:
        # the url contains a content_id (bookmark or direct link to page)
        sws.render_content_by_key("dynamic", content_key=content_id)
    else:
        # the user browsed to the home page (didn't click the home button)
        st.experimental_set_query_params()
        render_home_content(content_name="dynamic")

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


home()
