import pytest

from bs4 import BeautifulSoup
from bs4.replacer import SoupReplacer

# ============================================================================
# Milestone 2 Tests (Original API)
# ============================================================================

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


# ============================================================================
# Milestone 3 Tests (Transformer API)
# ============================================================================

def test_name_xformer_b_to_blockquote():
    """Test name_xformer: Replace <b> tags with <blockquote> tags"""
    html = "<div><b>bold</b> and <b>more bold</b></div>"
    replacer = SoupReplacer(
        name_xformer=lambda tag: "blockquote" if tag.name == "b" else tag.name
    )
    soup = BeautifulSoup(html, "html.parser", replacer=replacer)

    # All <b> tags should be replaced with <blockquote>
    assert len(soup.find_all("blockquote")) == 2
    assert len(soup.find_all("b")) == 0
    assert soup.find("blockquote").string == "bold"


def test_name_xformer_conditional_replacement():
    """Test name_xformer: Replace tags conditionally based on attributes"""
    html = '<div><span class="important">Keep</span><span>Change</span></div>'
    
    def conditional_name_xformer(tag):
        if tag.name == "span" and "important" not in tag.attrs.get("class", []):
            return "div"
        return tag.name
    
    replacer = SoupReplacer(name_xformer=conditional_name_xformer)
    soup = BeautifulSoup(html, "html.parser", replacer=replacer)
    
    # Only the span without "important" class should be changed to div
    spans = soup.find_all("span")
    assert len(spans) == 1
    assert "important" in spans[0].get("class", [])


def test_attrs_xformer_remove_class_attr():
    """Test attrs_xformer: Remove class attribute from all tags"""
    html = '<div class="container"><p class="text">Hello</p><span class="note">World</span></div>'
    
    def remove_class(tag):
        return {k: v for k, v in tag.attrs.items() if k != "class"}
    
    replacer = SoupReplacer(attrs_xformer=remove_class)
    soup = BeautifulSoup(html, "html.parser", replacer=replacer)
    
    # No tags should have a class attribute
    for tag in soup.find_all(True):  # Find all tags
        assert tag.get("class") is None


def test_attrs_xformer_add_default_class():
    """Test attrs_xformer: Add default class to all <p> tags"""
    html = "<div><p>First</p><p class='old'>Second</p><span>Third</span></div>"
    
    def add_test_class(tag):
        if tag.name == "p":
            new_attrs = dict(tag.attrs)
            new_attrs["class"] = ["test"]
            return new_attrs
        return tag.attrs
    
    replacer = SoupReplacer(attrs_xformer=add_test_class)
    soup = BeautifulSoup(html, "html.parser", replacer=replacer)
    
    # All <p> tags should have class="test"
    p_tags = soup.find_all("p")
    assert len(p_tags) == 2
    for p in p_tags:
        assert p.get("class") == ["test"]
    
    # <span> should not have class attribute
    span = soup.find("span")
    assert span.get("class") is None


def test_xformer_side_effects():
    """Test xformer: Apply side effects to remove class attributes"""
    html = '<div class="outer"><p class="inner">Text</p><a href="#" class="link">Link</a></div>'
    
    def remove_class_attr(tag):
        if "class" in tag.attrs:
            del tag.attrs["class"]
    
    replacer = SoupReplacer(xformer=remove_class_attr)
    soup = BeautifulSoup(html, "html.parser", replacer=replacer)
    
    # No tags should have class attributes
    for tag in soup.find_all(True):
        assert tag.get("class") is None


def test_combined_transformers():
    """Test combining name_xformer and attrs_xformer"""
    html = '<div><b class="bold">Bold text</b><i class="italic">Italic text</i></div>'
    
    replacer = SoupReplacer(
        name_xformer=lambda tag: "strong" if tag.name == "b" else ("em" if tag.name == "i" else tag.name),
        attrs_xformer=lambda tag: {k: v for k, v in tag.attrs.items() if k != "class"}
    )
    soup = BeautifulSoup(html, "html.parser", replacer=replacer)
    
    # Tags should be renamed
    assert len(soup.find_all("strong")) == 1
    assert len(soup.find_all("em")) == 1
    assert len(soup.find_all("b")) == 0
    assert len(soup.find_all("i")) == 0
    
    # No tags should have class attributes
    for tag in soup.find_all(True):
        assert tag.get("class") is None

