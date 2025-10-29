# Milestone 2: SoupStrainer Optimizations

This milestone implements tasks 2, 3, and 4 from Milestone 1 using BeautifulSoup's `SoupStrainer` for optimized parsing of large HTML/XML files.

## Files

- `task2.py` - Print all hyperlinks (`<a>` tags) using SoupStrainer
- `task3.py` - Print all unique tag names using SoupStrainer  
- `task4.py` - Print all tags with id attributes using SoupStrainer

## SoupStrainer Optimizations

### Task 2 (Hyperlinks)
- **Optimization**: Uses `SoupStrainer("a")` to parse only `<a>` tags
- **Benefit**: Significantly reduces memory usage and parsing time for large files by ignoring all other elements

### Task 3 (Unique Tag Names)
- **Optimization**: Uses `SoupStrainer(lambda name, attrs: name is not None)` to exclude comments, processing instructions, and other non-tag elements
- **Benefit**: Focuses parsing only on actual HTML/XML tags, improving performance

### Task 4 (Tags with ID)
- **Optimization**: Uses `SoupStrainer(lambda name, attrs: attrs and 'id' in attrs)` to parse only tags that have an id attribute
- **Benefit**: Dramatically reduces processing time for large files by filtering at the parsing level

## Usage

```bash
python task2.py <input_html_or_xml_path>
python task3.py <input_html_or_xml_path>
python task4.py <input_html_or_xml_path>
```

## Performance Benefits

SoupStrainer provides several key advantages:
1. **Memory Efficiency**: Only parses relevant elements, reducing memory footprint
2. **Speed**: Faster parsing by avoiding unnecessary element processing
3. **Scalability**: Better performance on large files with millions of elements
4. **Targeted Processing**: Focuses computational resources on elements of interest

## API definitions (files and line numbers) PART-2 of Milestone 2

- BeautifulSoup constructor (`BeautifulSoup.__init__`)
  - File: `bs4/__init__.py`, line 209
- BeautifulSoup class
  - File: `bs4/__init__.py`, line 133
- SoupStrainer constructor (`SoupStrainer.__init__`)
  - File: `bs4/filter.py`, line 345
- SoupStrainer class
  - File: `bs4/filter.py`, line 313
- Tag.find_all (used via `soup.find_all(...)` and `soup([...])`)
  - File: `bs4/element.py`, line 2715
- Tag.__call__ (alias for `find_all`, used via `soup(["script","style"])`)
  - File: `bs4/element.py`, line 2232
- Tag.find_parent (used via `a.find_parent("div")`)
  - File: `bs4/element.py`, line 992
- PageElement.get_text (used via `a.get_text(strip=True)`)
  - File: `bs4/element.py`, line 524
- PageElement.text property (used via `a.text`)
  - File: `bs4/element.py`, lines 549–551
- Tag.get (attribute access, used via `tag.get("id")`, `a.get("href")`)
  - File: `bs4/element.py`, line 2160
- Tag.__setitem__ (attribute set, used via `p["class"] = ["test"]`)
  - File: `bs4/element.py`, line 2223
- Tag.prettify (used via `soup.prettify()` and when writing output)
  - File: `bs4/element.py`, line 2601
- PageElement.decompose (used via `node.decompose()`)
  - File: `bs4/element.py`, line 635

Notes:
- The file names and line numbers refer to the original BeautifulSoup source code in this repository before any modifications.
- Many APIs are methods of `Tag`/`PageElement` and are available on `BeautifulSoup` instances because `BeautifulSoup` subclasses `Tag`.
