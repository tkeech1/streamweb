import streamlit as st


def render(
    post_modules=None,
    recent_posts_button_click=None,
    post_id=None,
):

    try:
        if post_id:
            post_id = int(post_id)
            # TODO - this will be slow with a lot of posts
            for post in post_modules:
                if post_id == post.key:
                    post.render()
                    return
        elif any(recent_posts_button_click):
            for i, clicked in enumerate(recent_posts_button_click):
                if clicked:
                    post_modules[i].render()
                    return

        st.write("Post not found")
    except:
        st.write("Post not found")
