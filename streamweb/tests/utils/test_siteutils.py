"""Tests for `stsiteutils` package."""

import importlib
from utils.siteutils import StreamwebSite
from streamlit import caching
import streamlit as st
import pytest
import tests.site_config as site_config


@pytest.fixture
def streamwebsite_dev():
    yield StreamwebSite("id", "title", "desc", {"name": "name", "email": "example@example.com"}, "url", "lang", "dev")
    caching.clear_cache()


@pytest.fixture
def streamwebsite_prd():
    yield StreamwebSite("id", "title", "desc", {"name": "name", "email": "example@example.com"}, "url", "lang", "prd")
    caching.clear_cache()


@pytest.fixture
def sws_feedgen():
    yield StreamwebSite(
        "test_id",
        "TEST Web Site Name",
        "TEST A description of the web site.",
        {"name": "test"},
        "test",
        "test",
        "prd",
    )
    caching.clear_cache()


def test_load_content_dev(streamwebsite_dev: StreamwebSite):

    streamwebsite_dev.load_content("tests/testpkg1")
    assert streamwebsite_dev.content_modules["tests/testpkg1"] == [
        importlib.import_module(name=f".module2", package="tests.testpkg1"),
        importlib.import_module(name=f".module1", package="tests.testpkg1"),
    ]

    streamwebsite_dev.load_content("tests/testpkg2")
    assert streamwebsite_dev.content_modules["tests/testpkg2"] == [
        importlib.import_module(name=f".module3", package="tests.testpkg2")
    ]


def test_load_content_prd(streamwebsite_prd: StreamwebSite):

    streamwebsite_prd.load_content("tests/testpkg1")
    assert streamwebsite_prd.content_modules["tests/testpkg1"] == [
        importlib.import_module(name=f".module2", package="tests.testpkg1"),
        importlib.import_module(name=f".module1", package="tests.testpkg1"),
    ]

    streamwebsite_prd.load_content("tests/testpkg2")
    assert streamwebsite_prd.content_modules["tests/testpkg2"] == [
        importlib.import_module(name=f".module3", package="tests.testpkg2")
    ]


def test_render_content_by_click(streamwebsite_dev: StreamwebSite):
    streamwebsite_dev.load_content("tests/testpkg1")
    assert (
        streamwebsite_dev.render_content_by_click("tests/testpkg1", st, [True, False])
        == 2
    )
    assert (
        streamwebsite_dev.render_content_by_click("tests/testpkg1", st, [False, True])
        == 1
    )
    assert (
        streamwebsite_dev.render_content_by_click("tests/testpkg1", st, [False, False])
        == -1
    )


def test_render_content_by_key(streamwebsite_dev: StreamwebSite):
    streamwebsite_dev.load_content("tests/testpkg1")
    assert streamwebsite_dev.render_content_by_key("tests/testpkg1", st, "2") == 2
    assert streamwebsite_dev.render_content_by_key("tests/testpkg1", st, "1") == 1
    assert streamwebsite_dev.render_content_by_key("tests/testpkg1", st, "4") == -1


def test_create_feed_generator(sws_feedgen: StreamwebSite):
    sws_feedgen.load_content("tests/testpkg1")
    fg = sws_feedgen.create_feed_generator("tests/testpkg1")
    assert fg.title() == site_config.website_title
    assert fg.id() == site_config.website_id
    assert fg.description() == site_config.website_description

    # need to sort the content since the fg.item() method returns
    # content by date ascending
    content = sorted(
        sws_feedgen.content_modules["tests/testpkg1"],
        key=lambda x: x.content_date,
        reverse=False,
    )
    for fe, content_item in zip(fg.item(), content):
        assert fe.id() == f"{sws_feedgen.website_url}?content={str(content_item.key)}"
        assert fe.title() == content_item.long_title
        assert fe.pubDate() == content_item.content_date
