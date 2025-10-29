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
