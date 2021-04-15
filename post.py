import streamlit as st
import utils


def render_recent_post(
    post_modules_loader=None,
    recent_posts_button_click=None,
):
    if any(recent_posts_button_click):
        for i, clicked in enumerate(recent_posts_button_click):
            if clicked:
                post_module = utils.load_post_modules(post_modules_loader)[i]
                post_module.render()
                return post_module.key

    st.write("Post not found")


def render_post(post_modules_loader=None, post_id=None):
    try:
        if post_id:
            for module in utils.load_post_modules(post_modules_loader):
                if int(post_id) == module.key:
                    module.render()
                    return

        st.write("Post not found")
    except Exception as e:
        st.write("An error occurred while loading content.")
