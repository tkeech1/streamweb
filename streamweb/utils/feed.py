from enum import Enum
from feedgen.feed import FeedGenerator
import pathlib
import os
import streamlit as st


class FeedType(Enum):
    RSS = "rss"
    ATOM = "atom"


def create_feed_file(
    fg: FeedGenerator, feed_file_name: str, feed_type: FeedType
) -> str:

    path_within_strealit_static = "feeds"

    # Create a directory within the streamlit static asset directory
    STREAMLIT_STATIC_PATH = pathlib.Path(st.__path__[0]) / "static"
    FEEDS_PATH = STREAMLIT_STATIC_PATH / path_within_strealit_static
    if not FEEDS_PATH.is_dir():
        FEEDS_PATH.mkdir()

    final_file_name = feed_file_name.replace(os.path.sep, "_")
    if feed_type == FeedType.ATOM:
        fg.atom_file(str(FEEDS_PATH / f"{final_file_name}_atom.xml"))
        return f"{path_within_strealit_static}{os.sep}{final_file_name}_atom.xml"
    else:
        fg.rss_file(str(FEEDS_PATH / f"{final_file_name}_rss.xml"))
        return f"{path_within_strealit_static}{os.sep}{final_file_name}_rss.xml"
