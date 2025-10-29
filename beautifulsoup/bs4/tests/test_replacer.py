import pytest

from bs4 import BeautifulSoup
from bs4.replacer import SoupReplacer


def test_replacer_basic_b_to_blockquote():
    html = "<div><b>bold</b> and <b>more</b></div>"
    replacer = SoupReplacer("b", "blockquote")
    soup = BeautifulSoup(html, "html.parser", replacer=replacer)

    # All <b> tags should be replaced to <blockquote> during parsing
    assert soup.encode() == b"<div><blockquote>bold</blockquote> and <blockquote>more</blockquote></div>"
    assert len(soup.find_all("blockquote")) == 2
    assert len(soup.find_all("b")) == 0


def test_replacer_nested_and_attributes_preserved():
    html = '<div id="outer"><p><b class="x">hello <i>there</i></b></p></div>'
    replacer = SoupReplacer("b", "blockquote")
    soup = BeautifulSoup(html, "html.parser", replacer=replacer)

    # Ensure the replacement maintained structure and attributes
    tag = soup.find("blockquote")
    assert tag is not None
    assert tag.get("class") == ["x"]
    assert tag.find("i").string == "there"
    # and only a single blockquote exists
    assert len(soup.find_all("blockquote")) == 1

