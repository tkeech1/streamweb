import streamlit as st
import importlib
from feedgen.feed import FeedGenerator
import os
from os.path import basename, isfile, join
import glob
from typing import List, Tuple, Dict
from types import ModuleType
import logging
from utils.feed import create_feed_file, FeedType
from utils.metrics import log_runtime


logger = logging.getLogger(__name__)

# https://docs.streamlit.io/en/stable/caching.html#the-hash-funcs-parameter

production_label = "prd"


class ModuleLoader:
    def __init__(self, package_name: str, environment: str):
        self.package_name = package_name
        self.environment = environment


def hash_module_modified(module_loader: ModuleLoader) -> Tuple[str, float]:

    if module_loader.environment == production_label:
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


class StreamwebSite:
    def __init__(
        self,
        website_id: str,
        website_title: str,
        website_description: str,
        website_author: Dict[str, str],
        website_url: str,
        website_language: str,
        environment: str = "dev",
    ):
        self.website_id = website_id
        self.website_title = website_title
        self.website_description = website_description
        self.website_author = website_author
        self.website_url = website_url
        self.website_language = website_language
        self.environment = environment
        self.content_modules = {}
        self.rss_feed = {}
        self.atom_feed = {}

    def load_content(self, package_name: str) -> None:
        content_loader = ModuleLoader(
            package_name=package_name, environment=self.environment
        )

        self.content_modules[package_name] = self.load_modules(content_loader)
        self.atom_feed[package_name], self.rss_feed[package_name] = self.load_feeds(
            content_loader
        )

    # TODO - This function reloads all modules if any module has
    # changed. Change to load only those modules that have changed
    # since last load
    @st.cache(hash_funcs={ModuleLoader: hash_module_modified})
    def load_modules(self, module_loader: ModuleLoader) -> List[ModuleType]:

        logger.info(
            f"loading content modules in '{module_loader.package_name}' package "
        )

        importlib.invalidate_caches()

        all_modules = []
        if os.path.isdir(module_loader.package_name):
            modules = glob.glob(join(module_loader.package_name, "*.py"))
            all_modules = [
                basename(f)[:-3]
                for f in modules
                if isfile(f) and not f.endswith("__init__.py")
            ]

        loaded_modules = []
        for module_name in all_modules:
            module = importlib.import_module(
                name=f".{module_name}",
                package=module_loader.package_name.replace(os.path.sep, "."),
            )
            # if the module has already been loaded, reload() so the
            # import system sees the changes to the module
            # changes to modules were not visible without the call to reload()
            module = importlib.reload(module)
            loaded_modules.append(module)

        return sorted(loaded_modules, key=lambda x: x.content_date, reverse=True)

    # TODO - This function reloads all modules if any module has
    # changed. Change to load only those modules that have changed
    # since last load
    @st.cache(hash_funcs={ModuleLoader: hash_module_modified})
    def load_feeds(self, module_loader: ModuleLoader) -> Tuple[str, str]:

        logging.info(
            f"loading feeds for modules in '{module_loader.package_name}' package "
        )

        rss_feed = self.create_feed(
            module_loader.package_name,
            module_loader.package_name.replace(os.sep, "_"),
            FeedType.RSS,
        )

        atom_feed = self.create_feed(
            module_loader.package_name,
            module_loader.package_name.replace(os.sep, "_"),
            FeedType.ATOM,
        )

        return atom_feed, rss_feed

    def create_buttons(
        self, content_name, location: st, number_items_to_display: int = 999999
    ) -> List[bool]:
        # this is a workaround since it doesn't appear possible to
        # get the key of the button that was clicked
        # https://discuss.streamlit.io/t/how-to-use-the-key-field-in-interactive-widgets-api/1007
        button_click_flags = []
        for c in self.content_modules[content_name][
            : min(number_items_to_display, len(self.content_modules[content_name]))
        ]:
            # button_click_flags.append(location.button(c.short_title, key=c.key))
            button_click_flags.append(location.button(c.short_title))
        return button_click_flags

    def create_link_list(
        self,
        content_name: str,
        location: st,
        search_text: str,
    ) -> None:

        for module in self.content_modules[content_name]:
            display = True
            if search_text:
                if search_text.lower() not in module.long_title.lower():
                    display = False
            if display:
                link = (
                    f"<a href='/?content={module.key}' target='_self'>"
                    f"{module.long_title}</a>"
                )
                location.markdown(
                    f'{module.content_date.strftime("%Y.%m.%d")} - {link}',
                    unsafe_allow_html=True,
                )

    def render_content_by_click(
        self,
        content_name: str,
        location: st,
        button_click: List[bool],
    ) -> int:
        try:
            if any(button_click):
                for i, clicked in enumerate(button_click):
                    if clicked:
                        content = self.content_modules[content_name][i]
                        content.render(location)
                        return content.key

            raise Exception("Content not found")
        except Exception as e:
            if self.environment == production_label:
                location.write("Content not found.")
            else:
                location.write(f"{e}")
            return -1

    def render_content_by_key(
        self, content_name: str, location: st, content_key: str
    ) -> int:
        try:
            if content_key:
                for content in self.content_modules[content_name]:
                    if int(content_key) == content.key:
                        content.render(location)
                        return content.key

            raise Exception("Content not found")
        except Exception as e:
            if self.environment == production_label:
                location.write("Content not found.")
            else:
                location.write(f"{e}")
            return -1

    def create_feed_generator(self, content_name: str) -> FeedGenerator:
        fg = FeedGenerator()
        fg.id(self.website_id)
        fg.title(self.website_title)
        fg.description(self.website_description)
        fg.author(self.website_author)
        fg.link(href=self.website_url, rel="alternate")
        fg.language(self.website_language)

        for c in self.content_modules[content_name]:
            fe = fg.add_entry()
            fe.id(f"{self.website_url}?content={str(c.key)}")
            fe.title(c.long_title)
            fe.published(c.content_date)
            fe.description(c.long_title)
            fe.link(href=f"{self.website_url}?content={str(c.key)}")

        return fg

    def create_feed(
        self,
        content_name: str,
        feed_name: str,
        feed_type: FeedType,
    ) -> str:
        fg = self.create_feed_generator(
            content_name,
        )
        return create_feed_file(fg, feed_name, feed_type)
