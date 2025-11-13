# Milestone 3: SoupReplacer Transformer API

This milestone extends the SoupReplacer API from Milestone 2 with transformer functions that enable conditional tag and attribute modifications during parsing.

## Files

- `task7.py` - Add `class="test"` to all `<p>` tags using the new `attrs_xformer` API

## New SoupReplacer API (Milestone 3)

### API: `SoupReplacer(name_xformer=None, attrs_xformer=None, xformer=None)`

Three types of transformer functions:

1. **`name_xformer`** - Function that takes a tag and returns a new tag name
2. **`attrs_xformer`** - Function that takes a tag and returns new attributes dict
3. **`xformer`** - Function that takes a tag and applies side effects (no return value)

### Examples

```python
# Transform tag names conditionally
b_to_blockquote = SoupReplacer(
    name_xformer=lambda tag: "blockquote" if tag.name == "b" else tag.name
)
soup = BeautifulSoup(html, "html.parser", replacer=b_to_blockquote)

# Transform attributes
def add_class_to_p(tag):
    if tag.name == "p":
        new_attrs = dict(tag.attrs)
        new_attrs["class"] = ["test"]
        return new_attrs
    return tag.attrs

p_transformer = SoupReplacer(attrs_xformer=add_class_to_p)
soup = BeautifulSoup(html, "html.parser", replacer=p_transformer)

# Side effects (modify tag in place)
def remove_class_attr(tag):
    if "class" in tag.attrs:
        del tag.attrs["class"]

class_remover = SoupReplacer(xformer=remove_class_attr)
soup = BeautifulSoup(html, "html.parser", replacer=class_remover)
```

## Usage

```bash
python task7.py <input_html_path> [output_path]
```

## Implementation Details

- **Files changed**: `bs4/replacer.py` (extended with M3 API), `bs4/__init__.py` (applies transformers during parsing)
- **Behavior**: Transformations happen during parsing for performance
- **Backward compatible**: Milestone 2 API (`SoupReplacer("b", "blockquote")`) still works
- **Tests**: `bs4/tests/test_replacer.py` - 6 new tests (8 total: 2 M2 + 6 M3)

### Test Cases (Milestone 3)

1. `test_name_xformer_b_to_blockquote` - Basic name transformation
2. `test_name_xformer_conditional_replacement` - Conditional replacements based on attributes
3. `test_attrs_xformer_remove_class_attr` - Remove class attributes from all tags
4. `test_attrs_xformer_add_default_class` - Add default class to specific tags
5. `test_xformer_side_effects` - Side-effect based transformations
6. `test_combined_transformers` - Combine name and attribute transformers

Run tests: `pytest bs4/tests/test_replacer.py -v`

## Technical Brief: M2 vs M3 API

### Milestone 2 (Simple)
- API: `SoupReplacer(og_tag, alt_tag)`
- Use case: Simple one-to-one tag name replacement
- Pros: Very simple, easy to use
- Cons: Limited to tag names only, no conditional logic, can't modify attributes

### Milestone 3 (Powerful)
- API: `SoupReplacer(name_xformer=..., attrs_xformer=..., xformer=...)`
- Use case: Complex transformations with conditional logic
- Pros: Flexible, handles attributes, supports conditionals, composable
- Cons: Slightly more complex for simple cases

### Comparison Table

| Feature | M2 | M3 |
|---------|----|----|
| Tag name replacement | ✅ | ✅ |
| Attribute transformation | ❌ | ✅ |
| Conditional logic | ❌ | ✅ |
| Combine transformers | ❌ | ✅ |

### Recommendation

**Adopt M3 as the primary API while keeping M2 for backward compatibility.**

**Why?**
- M3 handles all M2 use cases plus way more (attributes, conditionals)
- Real-world HTML/XML transformation needs flexibility
- Both APIs coexist in same implementation

**When to use each:**
- Simple tag swap → M2: `SoupReplacer("b", "strong")`
- Conditional or attribute changes → M3: Use transformer functions
- Complex scenarios (e.g., "add class to all p tags without id") → Only M3 can do this

## Deliverables

✅ `bs4/replacer.py` - Extended SoupReplacer with `name_xformer`, `attrs_xformer`, `xformer`  
✅ `bs4/__init__.py` - Integrated transformer application during parsing  
✅ `bs4/tests/test_replacer.py` - 6 new test cases  
✅ `apps/m3/task7.py` - Task 7 implementation using M3 API  
✅ `apps/m3/M3-README.md` - This technical brief
