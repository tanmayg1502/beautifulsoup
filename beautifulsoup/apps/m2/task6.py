"""Task 6 (via SoupReplacer): Change all <b> tags to <blockquote> during parsing"""

import sys
from pathlib import Path
from bs4 import BeautifulSoup
from bs4.replacer import SoupReplacer


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python task6_replacer.py <input_html_or_xml_path> [output_path]")
        sys.exit(1)

    input_path = Path(sys.argv[1])
    if not input_path.exists():
        print(f"Input file not found: {input_path}")
        sys.exit(1)

    output_path = (
        Path(sys.argv[2])
        if len(sys.argv) >= 3
        else input_path.with_suffix(input_path.suffix + ".blockquote.html")
    )

    with input_path.open("r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    replacer = SoupReplacer("b", "blockquote")
    soup = BeautifulSoup(content, "html.parser", replacer=replacer)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        f.write(soup.prettify())

    print("Replaced <b> with <blockquote> during parsing")
    print(f"Wrote: {output_path}")


if __name__ == "__main__":
    main()


