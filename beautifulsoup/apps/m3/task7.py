"""Task 7 (via SoupReplacer M3): Add or replace class="test" on all <p> tags during parsing"""

import sys
from pathlib import Path
from bs4 import BeautifulSoup
from bs4.replacer import SoupReplacer


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python task7.py <input_html_or_xml_path> [output_path]")
        sys.exit(1)

    input_path = Path(sys.argv[1])
    if not input_path.exists():
        print(f"Input file not found: {input_path}")
        sys.exit(1)

    # Descriptive output filename
    output_path = (
        Path(sys.argv[2])
        if len(sys.argv) >= 3
        else input_path.with_suffix(input_path.suffix + ".p-class-test.html")
    )

    with input_path.open("r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    # Define an attribute transformer that sets class="test" on all <p> tags
    def set_p_class_to_test(tag):
        if tag.name == "p":
            # Replace or add class="test" on <p> tags
            new_attrs = dict(tag.attrs)
            new_attrs["class"] = ["test"]
            return new_attrs
        return tag.attrs

    # Create SoupReplacer using Milestone 3 API
    replacer = SoupReplacer(attrs_xformer=set_p_class_to_test)
    
    # Parse with the replacer - transformations happen during parsing
    soup = BeautifulSoup(content, "html.parser", replacer=replacer)

    # Count the transformed <p> tags
    count = len(soup.find_all("p"))

    # Save the modified tree
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        f.write(soup.prettify())

    print(f"Updated class=\"test\" on <p> tags during parsing: {count}")
    print(f"Wrote: {output_path}")


if __name__ == "__main__":
    main()
