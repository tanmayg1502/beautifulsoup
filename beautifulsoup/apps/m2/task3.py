"""Task 3: Print all unique tag names in the document using SoupStrainer"""

import sys
from pathlib import Path
from bs4 import BeautifulSoup, SoupStrainer


def main() -> None:
    # standard arg checking
    if len(sys.argv) < 2:
        print("Usage: python task3.py <input_html_or_xml_path>")
        sys.exit(1)

    input_path = Path(sys.argv[1])
    if not input_path.exists():
        print(f"Input file not found: {input_path}")
        sys.exit(1)

    with input_path.open("r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    # For task3, we need all tags, so we use a simple SoupStrainer that accepts all elements
    # This still provides some optimization by filtering out non-element content
    strainer = SoupStrainer()
    soup = BeautifulSoup(content, "html.parser", parse_only=strainer)

    # using set comprehension to get unique tag names
    # find_all() with no args gets everything (already filtered by SoupStrainer)
    tag_names = {tag.name for tag in soup.find_all() if tag.name is not None}
    
    # sort them alphabetically for cleaner output
    for name in sorted(tag_names):
        print(name)

    # helps to see how many different tags are used
    print(f"Unique tag names: {len(tag_names)}")


if __name__ == "__main__":
    main()
