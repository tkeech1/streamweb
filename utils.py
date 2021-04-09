import streamlit as st
import posts
import importlib


@st.cache
def load_post_modules():
    importlib.invalidate_caches()
    global posts

    post_modules = []
    for module_name in posts.__all__:
        module = importlib.import_module(name=f".{module_name}", package="posts")
        post_modules.append(module)

    post_modules = sorted(post_modules, key=lambda x: x.post_date, reverse=True)
    return post_modules
