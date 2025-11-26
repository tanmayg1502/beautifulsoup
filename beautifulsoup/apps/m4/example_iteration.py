#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Example demonstrating the iterable BeautifulSoup feature.

Milestone 4: Make soup an iterable object.
"""

from bs4 import BeautifulSoup


def main():
    """Demonstrate iterating over BeautifulSoup object."""
    
    html_doc = """
    <html>
        <head>
            <title>Test Page</title>
        </head>
        <body>
            <h1>Welcome</h1>
            <p>This is a paragraph.</p>
            <div>
                <span>Some text in a span</span>
            </div>
        </body>
    </html>
    """
    
    # Create soup object
    soup = BeautifulSoup(html_doc, 'html.parser')
    
    # Iterate over all nodes in the tree
    print("Iterating over BeautifulSoup object:")
    print("=" * 50)
    
    for node in soup:
        print(node)
    
    print("\n" + "=" * 50)
    print("Iteration complete!")


if __name__ == "__main__":
    main()
