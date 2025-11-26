# -*- coding: utf-8 -*-
"""Tests for BeautifulSoup iterable functionality (Milestone 4)."""

import pytest
from bs4 import BeautifulSoup
from bs4.element import Tag, NavigableString

from . import SoupTest


class TestIterableBeautifulSoup(SoupTest):
    """Test that BeautifulSoup objects are iterable and traverse the tree correctly."""
    
    def test_simple_iteration(self):
        """Test iteration over a simple HTML document."""
        html = "<html><head><title>Test</title></head><body><p>Hello</p></body></html>"
        soup = self.soup(html)
        
        # Collect all nodes by iterating
        nodes = list(soup)
        
        # Verify we get nodes back
        assert len(nodes) > 0
        
        # Verify we get the expected types (Tags and NavigableStrings)
        for node in nodes:
            assert isinstance(node, (Tag, NavigableString))
    
    def test_iteration_visits_all_tags(self):
        """Test that iteration visits all tags in the document."""
        html = "<html><head><title>Test</title></head><body><h1>Title</h1><p>Para</p></body></html>"
        soup = self.soup(html)
        
        # Collect all tags by iterating
        tags = [node for node in soup if isinstance(node, Tag)]
        tag_names = [tag.name for tag in tags]
        
        # Verify all expected tags are present
        assert 'html' in tag_names
        assert 'head' in tag_names
        assert 'title' in tag_names
        assert 'body' in tag_names
        assert 'h1' in tag_names
        assert 'p' in tag_names
    
    def test_iteration_visits_text_nodes(self):
        """Test that iteration visits text nodes (NavigableStrings)."""
        html = "<html><body><p>Hello World</p><div>Test</div></body></html>"
        soup = self.soup(html)
        
        # Collect all text nodes
        text_nodes = [node for node in soup if isinstance(node, NavigableString) and not isinstance(node, Tag)]
        texts = [str(node).strip() for node in text_nodes if str(node).strip()]
        
        # Verify we get the text content
        assert 'Hello World' in texts
        assert 'Test' in texts
    
    def test_iteration_order(self):
        """Test that iteration follows depth-first traversal order."""
        html = "<html><head><title>Title</title></head><body><p>Para</p></body></html>"
        soup = self.soup(html)
        
        # Collect tags in iteration order
        tags = [node for node in soup if isinstance(node, Tag)]
        tag_names = [tag.name for tag in tags]
        
        # Verify depth-first order: html -> head -> title -> body -> p
        assert tag_names.index('html') < tag_names.index('head')
        assert tag_names.index('head') < tag_names.index('title')
        assert tag_names.index('title') < tag_names.index('body')
        assert tag_names.index('body') < tag_names.index('p')
    
    def test_iteration_with_nested_structure(self):
        """Test iteration with deeply nested HTML structure."""
        html = """
        <html>
            <body>
                <div id="outer">
                    <div id="middle">
                        <div id="inner">
                            <span>Deep text</span>
                        </div>
                    </div>
                </div>
            </body>
        </html>
        """
        soup = self.soup(html)
        
        # Collect all nodes
        nodes = list(soup)
        
        # Verify we can iterate without error
        assert len(nodes) > 0
        
        # Verify all nested divs are found
        tags = [node for node in soup if isinstance(node, Tag)]
        div_ids = [tag.get('id') for tag in tags if tag.name == 'div' and tag.get('id')]
        
        assert 'outer' in div_ids
        assert 'middle' in div_ids
        assert 'inner' in div_ids
        
        # Verify the span is found
        span_tags = [tag for tag in tags if tag.name == 'span']
        assert len(span_tags) == 1
        assert span_tags[0].string == 'Deep text'
    
    def test_iteration_is_lazy(self):
        """Test that iteration is lazy and doesn't collect all nodes upfront."""
        html = "<html><body>" + "".join([f"<p>Paragraph {i}</p>" for i in range(100)]) + "</body></html>"
        soup = self.soup(html)
        
        # Verify that we can iterate and break early
        count = 0
        for node in soup:
            if isinstance(node, Tag) and node.name == 'p':
                count += 1
                if count == 5:
                    break
        
        # We should have found 5 paragraphs and stopped early
        assert count == 5
    
    def test_iteration_with_empty_document(self):
        """Test iteration with an empty or minimal document."""
        html = "<html></html>"
        soup = self.soup(html)
        
        # Should be able to iterate without error
        nodes = list(soup)
        
        # Should have at least the html tag
        tags = [node for node in nodes if isinstance(node, Tag)]
        assert len(tags) >= 1
        assert tags[0].name == 'html'
    
    def test_multiple_iterations(self):
        """Test that we can iterate over the same soup object multiple times."""
        html = "<html><body><p>Test</p></body></html>"
        soup = self.soup(html)
        
        # First iteration
        nodes1 = list(soup)
        
        # Second iteration
        nodes2 = list(soup)
        
        # Both iterations should produce the same sequence
        assert len(nodes1) == len(nodes2)
        
        # Verify the nodes are structurally the same
        for node1, node2 in zip(nodes1, nodes2):
            if isinstance(node1, Tag) and isinstance(node2, Tag):
                assert node1.name == node2.name
            else:
                assert str(node1) == str(node2)
