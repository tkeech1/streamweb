"""Tests for `stsiteutils` package."""

import importlib
from utils.siteutils import (
    load_content,
    render_content_by_click,
    render_content_by_key,
)


def test_load_content():
    assert load_content("tests/testpkg1", "") == [
        importlib.import_module(name=f".module2", package="tests.testpkg1"),
        importlib.import_module(name=f".module1", package="tests.testpkg1"),
    ]
    assert load_content("tests/testpkg1", "prd") == [
        importlib.import_module(name=f".module2", package="tests.testpkg1"),
        importlib.import_module(name=f".module1", package="tests.testpkg1"),
    ]
    assert load_content("tests/testpkg2", "") == [
        importlib.import_module(name=f".module3", package="tests.testpkg2")
    ]
    assert load_content("tests/testpkg2", "prd") == [
        importlib.import_module(name=f".module3", package="tests.testpkg2")
    ]


def test_render_content_by_click():
    content = load_content("tests/testpkg1", "")
    assert render_content_by_click(content, [True, False]) == 2
    assert render_content_by_click(content, [False, True]) == 1
    assert render_content_by_click(content, [False, False]) == None
    assert render_content_by_click(content, [False, False], "prd") == None


def test_render_content_by_key():
    content = load_content("tests/testpkg1", "")
    assert render_content_by_key(content, "2") == 2
    assert render_content_by_key(content, "1") == 1
    assert render_content_by_key(content, "4") == None
    assert render_content_by_key(content, "4", "prd") == None
