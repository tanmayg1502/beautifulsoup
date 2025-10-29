"""Task 4: Print all tags that have an id attribute using SoupStrainer"""

import sys
from pathlib import Path
from bs4 import BeautifulSoup, SoupStrainer


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python task4.py <input_html_or_xml_path>")
        sys.exit(1)

    input_path = Path(sys.argv[1])
    if not input_path.exists():
        print(f"Input file not found: {input_path}")
        sys.exit(1)

    # read file content
    with input_path.open("r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    # Use SoupStrainer to parse only tags that have an id attribute
    # This is a significant optimization for large files as it only processes relevant tags
    strainer = SoupStrainer(id=True)
    soup = BeautifulSoup(content, "html.parser", parse_only=strainer)
    
    # find_all gets all tags (already filtered by SoupStrainer to only include those with id)
    tags_with_id = soup.find_all()
    
    # display each tag with its id value
    for tag in tags_with_id:
        print(f"<{tag.name} id=\"{tag.get('id')}\"> ... </{tag.name}>")

    # show total count
    print(f"Total tags with id: {len(tags_with_id)}")


if __name__ == "__main__":
    main()
