import streamlit as st
import posts
import importlib
import os

# https://docs.streamlit.io/en/stable/caching.html#the-hash-funcs-parameter


class PostModuleLoader:
    def __init__(self, package_name, environment):
        self.package_name = package_name
        self.environment = environment


def hash_module_modified(module_loader):

    if module_loader.environment == "prd":
        # skip dynamic module loading
        return module_loader.package_name
    else:
        # for development, load modules dynamically if files have changed
        last_modified = 0
        for filename in os.listdir(module_loader.package_name):
            if not filename == "__init__.py" and filename.endswith(".py"):
                if (
                    os.path.getmtime(os.path.join(module_loader.package_name, filename))
                    > last_modified
                ):
                    last_modified = os.path.getmtime(
                        os.path.join(module_loader.package_name, filename)
                    )
        return (module_loader.package_name, last_modified)


# TODO - This function reloads all modules if any module has
# changed. Change to load only those modules that have changed
# since last load
@st.cache(hash_funcs={PostModuleLoader: hash_module_modified})
def load_post_modules(module_loader):
    importlib.invalidate_caches()
    global posts

    post_modules = []
    for module_name in posts.__all__:
        module = importlib.import_module(
            name=f".{module_name}", package=module_loader.package_name
        )
        post_modules.append(module)

    return sorted(post_modules, key=lambda x: x.post_date, reverse=True)
