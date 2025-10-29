from __future__ import annotations

from typing import Optional


class SoupReplacer(object):
    """A simple API to replace tag names during parsing.

    For Milestone-2, this supports only a single mapping from one tag
    name to another, specified via the constructor.

    Usage:
        replacer = SoupReplacer("b", "blockquote")
        BeautifulSoup(markup, replacer=replacer)
    """

    original_tag: str
    replacement_tag: str

    def __init__(self, original_tag: str, replacement_tag: str):
        self.original_tag = original_tag
        self.replacement_tag = replacement_tag

    def replace_tag_name(self, name: Optional[str]) -> Optional[str]:
        """Return the possibly replaced tag name.

        If the incoming name matches the configured original_tag,
        return replacement_tag; otherwise, return the incoming name.
        """
        if name is None:
            return None
        if name == self.original_tag:
            return self.replacement_tag
        return name


