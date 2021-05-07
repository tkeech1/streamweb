from utils.feed import create_feed_generator
from utils.siteutils import load_content
import site_config


def test_create_feed_generator():
    content = load_content("tests/testpkg1", "")
    fg = create_feed_generator(content)
    assert fg.title() == site_config.website_title
    assert fg.id() == site_config.website_id
    assert fg.description() == site_config.website_description

    # need to sort the content since the fg.item() method returns
    # content by date ascending
    content = sorted(content, key=lambda x: x.content_date, reverse=False)
    for fe, content_item in zip(fg.item(), content):
        assert fe.id() == str(content_item.key)
        assert fe.title() == content_item.long_title
        assert fe.pubDate() == content_item.content_date
