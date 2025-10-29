"""Task 2: Print all hyperlinks (<a> tags) from HTML/XML file using SoupStrainer"""

import sys
from pathlib import Path
from bs4 import BeautifulSoup, SoupStrainer


def main() -> None:
    # check command line args
    if len(sys.argv) < 2:
        print("Usage: python task2.py <input_html_or_xml_path>")
        sys.exit(1)

    input_path = Path(sys.argv[1])
    if not input_path.exists():
        print(f"Input file not found: {input_path}")
        sys.exit(1)

    # read the html content
    with input_path.open("r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    # Use SoupStrainer to parse only <a> tags for better performance
    # This significantly reduces memory usage and parsing time for large files
    strainer = SoupStrainer("a")
    soup = BeautifulSoup(content, "html.parser", parse_only=strainer)
    
    # find_all gets every <a> tag in the document (already filtered by SoupStrainer)
    links = soup.find_all("a")

    # extract href and text from each link
    for a in links:
        href = a.get("href")  # might be None if no href attribute
        text = a.text  # gets the visible text inside the tag
        print(f"href={href}\ttext={text}")

    # summary at the end
    print(f"Total <a> tags: {len(links)}")


if __name__ == "__main__":
    main()
