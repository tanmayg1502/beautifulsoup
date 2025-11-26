# Milestone 4: Iterable BeautifulSoup

Make BeautifulSoup objects iterable so you can loop through all nodes in the tree without calling `.descendants` explicitly.

## What's New?

You can now do this:

```python
soup = BeautifulSoup(html_doc, 'html.parser')

for node in soup:  # <-- NEW! soup is iterable now
    print(node)
```

Instead of:

```python
for node in soup.descendants:  # <-- Old way (still works)
    print(node)
```

## Implementation

### API: `BeautifulSoup.__iter__()`

- **File**: `bs4/__init__.py`, lines ~1096-1110
- **What it does**: Returns `self.descendants` (a generator)
- **Why**: Makes soup objects iterable in a Pythonic way

```python
def __iter__(self) -> Iterator[PageElement]:
    """Make BeautifulSoup iterable, yielding all nodes in the tree."""
    return self.descendants
```

That's it! Super simple implementation that leverages existing functionality.

## Key Features

✅ **Lazy evaluation** - Nodes are yielded one at a time (no list collection upfront)  
✅ **Memory efficient** - Works great with huge HTML files  
✅ **Depth-first traversal** - Same order as `.descendants`  
✅ **All node types** - Tags, text nodes, comments, everything  
✅ **Reusable** - Can iterate the same soup object multiple times  
✅ **Works with all parsers** - html.parser, lxml, html5lib, etc.

## Usage Examples

### Example 1: Basic Iteration

```python
from bs4 import BeautifulSoup

html = "<html><body><p>Hello</p></body></html>"
soup = BeautifulSoup(html, 'html.parser')

for node in soup:
    print(node)
```

### Example 2: Filter Specific Tags

```python
from bs4.element import Tag

# Find all paragraphs
for node in soup:
    if isinstance(node, Tag) and node.name == 'p':
        print(f"Paragraph: {node.get_text()}")
```

### Example 3: Collect Text

```python
from bs4.element import NavigableString, Comment

text_content = []
for node in soup:
    if isinstance(node, NavigableString) and not isinstance(node, Comment):
        text = str(node).strip()
        if text:
            text_content.append(text)
```

### Example 4: Early Break (Lazy!)

```python
# Stop after finding 5 headings
count = 0
for node in soup:
    if isinstance(node, Tag) and node.name in ['h1', 'h2', 'h3']:
        print(node.get_text())
        count += 1
        if count == 5:
            break  # Only processed nodes until 5 headings found!
```

## Tests

### Test File: `bs4/tests/test_iterable.py`

8 test cases covering:

1. `test_simple_iteration` - Basic iteration works
2. `test_iteration_visits_all_tags` - All tags are visited
3. `test_iteration_visits_text_nodes` - Text nodes included
4. `test_iteration_order` - Depth-first order
5. `test_iteration_with_nested_structure` - Deep nesting works
6. `test_iteration_is_lazy` - Lazy evaluation confirmed
7. `test_iteration_with_empty_document` - Edge case handling
8. `test_multiple_iterations` - Can iterate multiple times

Run tests:

```bash
python -m pytest beautifulsoup/bs4/tests/test_iterable.py -v
```

## Example App

**File**: `apps/m4/example_iteration.py`

Simple example demonstrating iteration over a BeautifulSoup object:

```python
soup = BeautifulSoup(html_doc, 'html.parser')

for node in soup:
    print(node)
```

Run it:

```bash
python beautifulsoup/apps/m4/example_iteration.py
```

## Why This is Cool

### Before M4

```python
# Had to remember to use .descendants
for node in soup.descendants:
    process(node)
```

### After M4

```python
# Just iterate! More Pythonic
for node in soup:
    process(node)
```

### Benefits

- **Pythonic**: Follows Python's iteration protocol
- **Discoverable**: New users will try `for node in soup` naturally
- **Memory efficient**: Lazy generator, not a list
- **Fast**: No overhead, just delegates to existing `.descendants`

## Technical Notes

### Why Not Collect Into a List?

The assignment said: "you should not collect the nodes of the tree onto a list in order to iterate over them."

Our implementation uses generators throughout:
- `__iter__()` returns `self.descendants`
- `descendants` is a generator (property)
- Generators are lazy - they yield one item at a time
- No list creation = memory efficient!

### Traversal Order

Depth-first, same as `.descendants`:

```
<html>
  <head>
    <title>Test</title>
  </head>
  <body>
    <p>Hi</p>
  </body>
</html>
```

Iterates: html → head → title → "Test" → body → p → "Hi"

### Performance

- **Time**: O(n) to visit all n nodes
- **Space**: O(1) for the iterator (lazy)
- **Early exit**: Can break early without wasting time

## Deliverables

✅ `bs4/__init__.py` - Added `__iter__()` method to BeautifulSoup  
✅ `bs4/tests/test_iterable.py` - 8 unit tests  
✅ `apps/m4/example_iteration.py` - Practical examples  
✅ `apps/m4/M4-README.md` - This file

## Quick Reference

```python
from bs4 import BeautifulSoup
from bs4.element import Tag, NavigableString

html = "<html><body><h1>Title</h1><p>Text</p></body></html>"
soup = BeautifulSoup(html, 'html.parser')

# Iterate all nodes
for node in soup:
    print(type(node), node)

# Filter tags
tags = [node for node in soup if isinstance(node, Tag)]

# Filter text
texts = [str(node).strip() for node in soup 
         if isinstance(node, NavigableString) 
         and not isinstance(node, Tag)
         and str(node).strip()]

# Count tag types
from collections import Counter
tag_counts = Counter(node.name for node in soup if isinstance(node, Tag))
print(tag_counts)  # Counter({'html': 1, 'body': 1, 'h1': 1, 'p': 1})
```
