import streamlit as st
import dynamic, static
import importlib
import os
from typing import List, Tuple
from types import ModuleType

# https://docs.streamlit.io/en/stable/caching.html#the-hash-funcs-parameter

production = "prd"


class ModuleLoader:
    def __init__(self, package_name, environment):
        self.package_name = package_name
        self.environment = environment


def hash_module_modified(module_loader: ModuleLoader) -> Tuple[str, int]:

    if module_loader.environment == production:
        # skip dynamic module loading
        return (module_loader.package_name, 0)
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
@st.cache(hash_funcs={ModuleLoader: hash_module_modified})
def load_modules(module_loader: ModuleLoader) -> List[ModuleType]:
    importlib.invalidate_caches()

    all_modules = []
    if module_loader.package_name == "dynamic":
        global dynamic
        all_modules = dynamic.__all__
    else:
        global static
        all_modules = static.__all__

    loaded_modules = []
    for module_name in all_modules:
        module = importlib.import_module(
            name=f".{module_name}", package=module_loader.package_name
        )
        # if the module has already been loaded, reload() so the import system sees the changes to the module
        # changes to modules were not visible without the call to reload()
        module = importlib.reload(module)
        loaded_modules.append(module)

    return sorted(loaded_modules, key=lambda x: x.content_date, reverse=True)


def render_content_by_click(
    content: List[ModuleType], button_click: List[bool], environment: str = "dev"
) -> str:
    try:
        if any(button_click):
            for i, clicked in enumerate(button_click):
                if clicked:
                    content = content[i]
                    content.render()
                    return content.key

        raise Exception("Content not found")
    except Exception as e:
        if environment == production:
            st.write(f"Content not found.")
        else:
            st.write(f"{e}")


# TODO - print error messages to screen in dev mode
def render_content_by_key(
    content: List[ModuleType], content_id: str, environment: str = "dev"
) -> str:
    try:
        if content_id:
            for content in content:
                if int(content_id) == content.key:
                    content.render()
                    return content.key

        raise Exception("Content not found")
    except Exception as e:
        if environment == production:
            st.write(f"Content not found.")
        else:
            st.write(f"{e}")


def load_content(package_name: str, environment: str) -> List[ModuleType]:
    content_loader = ModuleLoader(package_name=package_name, environment=environment)
    return load_modules(content_loader)
