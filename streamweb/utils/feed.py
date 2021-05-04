from distutils.command.config import config
import streamlit as st
from feedgen.feed import FeedGenerator
from typing import List
from types import ModuleType
import pathlib
import site_config
import os


def create_feed(content: List[ModuleType], package_name: str) -> None:

    # Create a directory within the streamlit static asset directory
    STREAMLIT_STATIC_PATH = pathlib.Path(st.__path__[0]) / "static"
    FEEDS_PATH = STREAMLIT_STATIC_PATH / "feeds"
    if not FEEDS_PATH.is_dir():
        FEEDS_PATH.mkdir()

    fg = FeedGenerator()
    fg.id(site_config.website_title)
    fg.title(site_config.website_title)
    fg.description(site_config.website_description)
    fg.author(site_config.website_author)
    fg.link(href=site_config.website_url, rel="alternate")
    fg.language(site_config.website_language)

    for content in content:
        fe = fg.add_entry()
        fe.id(str(content.key))
        fe.title(content.long_title)
        fe.published(content.content_date)
        fe.description(content.long_title)
        fe.link(href=content.long_title)

    fg.atom_file(str(FEEDS_PATH / f"{package_name.replace(os.path.sep, '_')}_atom.xml"))
    fg.rss_file(str(FEEDS_PATH / f"{package_name.replace(os.path.sep, '_')}_rss.xml"))
