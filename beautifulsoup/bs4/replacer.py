from __future__ import annotations

from typing import Optional, Callable, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from bs4.element import Tag


class SoupReplacer(object):
    """A flexible API to replace or transform tags during parsing.

    Milestone-2 API (simple tag name replacement):
        replacer = SoupReplacer("b", "blockquote")
        BeautifulSoup(markup, replacer=replacer)

    Milestone-3 API (transformer functions):
        # Transform tag names
        replacer = SoupReplacer(name_xformer=lambda tag: "blockquote" if tag.name == "b" else tag.name)
        
        # Transform attributes
        replacer = SoupReplacer(attrs_xformer=lambda tag: {k:v for k,v in tag.attrs.items() if k != "class"})
        
        # Side-effect transformations
        def remove_class_attr(tag):
            if "class" in tag.attrs:
                del tag.attrs["class"]
        replacer = SoupReplacer(xformer=remove_class_attr)
        
        BeautifulSoup(markup, replacer=replacer)
    """

    # Milestone-2 attributes
    original_tag: Optional[str]
    replacement_tag: Optional[str]
    
    # Milestone-3 attributes
    name_xformer: Optional[Callable[[Any], Optional[str]]]
    attrs_xformer: Optional[Callable[[Any], dict]]
    xformer: Optional[Callable[[Any], None]]

    def __init__(
        self, 
        original_tag: Optional[str] = None, 
        replacement_tag: Optional[str] = None,
        name_xformer: Optional[Callable[[Any], Optional[str]]] = None,
        attrs_xformer: Optional[Callable[[Any], dict]] = None,
        xformer: Optional[Callable[[Any], None]] = None
    ):
        """Constructor supporting both Milestone-2 and Milestone-3 APIs.
        
        Args:
            original_tag: (M2) Tag name to replace
            replacement_tag: (M2) New tag name
            name_xformer: (M3) Function that takes a tag and returns a new name
            attrs_xformer: (M3) Function that takes a tag and returns new attributes dict
            xformer: (M3) Function that takes a tag and modifies it (side effects)
        """
        # Milestone-2 API
        self.original_tag = original_tag
        self.replacement_tag = replacement_tag
        
        # Milestone-3 API
        self.name_xformer = name_xformer
        self.attrs_xformer = attrs_xformer
        self.xformer = xformer
        
        # Validate that at least one transformation is specified
        if (original_tag is None and replacement_tag is None and 
            name_xformer is None and attrs_xformer is None and xformer is None):
            raise ValueError("At least one transformation must be specified")
        
        # Validate M2 API usage
        if (original_tag is not None or replacement_tag is not None):
            if original_tag is None or replacement_tag is None:
                raise ValueError("Both original_tag and replacement_tag must be provided together")
            if name_xformer is not None or attrs_xformer is not None or xformer is not None:
                raise ValueError("Cannot mix Milestone-2 and Milestone-3 APIs")

    def replace_tag_name(self, name: Optional[str]) -> Optional[str]:
        """Return the possibly replaced tag name (Milestone-2 compatibility).

        If the incoming name matches the configured original_tag,
        return replacement_tag; otherwise, return the incoming name.
        """
        if name is None:
            return None
        if self.original_tag and name == self.original_tag:
            return self.replacement_tag
        return name
    
    def transform_endtag_name(self, name: Optional[str]) -> Optional[str]:
        """Transform an end tag name to match transformed start tags.
        
        For M2: uses the simple original_tag -> replacement_tag mapping
        For M3: creates a minimal tag-like object and applies name_xformer
        
        Args:
            name: The original tag name from the closing tag
            
        Returns:
            The transformed tag name to use for matching
        """
        if name is None:
            return None
        
        # M2 API: use simple replacement
        if self.original_tag is not None:
            return self.replace_tag_name(name)
        
        # M3 API: apply name_xformer if present
        if self.name_xformer is not None:
            # Create a minimal tag-like object for the transformer
            class MinimalTag:
                def __init__(self, tag_name: str):
                    self.name = tag_name
                    self.attrs = {}
            
            mock_tag = MinimalTag(name)
            transformed = self.name_xformer(mock_tag)
            return transformed if transformed is not None else name
        
        return name
    
    def apply_transformers(self, tag: 'Tag') -> None:
        """Apply all configured transformers to the given tag (Milestone-3).
        
        This method applies transformations in order:
        1. name_xformer: transforms the tag's name
        2. attrs_xformer: transforms the tag's attributes
        3. xformer: applies side effects to the tag
        
        Args:
            tag: The Tag object to transform
        """
        # Apply name transformer
        if self.name_xformer is not None:
            new_name = self.name_xformer(tag)
            if new_name is not None:
                tag.name = new_name
        
        # Apply attribute transformer
        if self.attrs_xformer is not None:
            new_attrs = self.attrs_xformer(tag)
            if new_attrs is not None:
                tag.attrs = new_attrs
        
        # Apply general transformer (side effects)
        if self.xformer is not None:
            self.xformer(tag)


