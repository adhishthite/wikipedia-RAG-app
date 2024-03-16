import os
import requests
from bs4 import BeautifulSoup
import time
import json
from urllib.robotparser import RobotFileParser


def init_data_folder():
    """Initializes the data folder."""
    os.makedirs("data", exist_ok=True)


def get_wiki_links(url: str) -> list[str]:
    """Fetches and extracts links from a Wikipedia page."""
    response = requests.get(url)
    response.raise_for_status()  # Check for HTTP errors

    soup = BeautifulSoup(response.content, "html.parser")

    # Find valid Wikipedia links within the main content
    content_div = soup.find("div", id="mw-content-text")
    links = []
    for a_tag in content_div.find_all("a", href=True):
        href = a_tag["href"]
        if href.startswith("/wiki/") and ":" not in href:  # Filter for relevant links
            links.append("https://en.wikipedia.org" + href)

    return links


def process_and_store_page(url: str, content: bytes):
    """Extracts text, creates JSON, and stores it."""
    soup = BeautifulSoup(content, "html.parser")
    title = soup.find("h1", id="firstHeading").text

    # Extract relevant text (adjust selectors as needed)
    text_paragraphs = [p.text for p in soup.find_all("p")]
    text = " ".join(text_paragraphs)

    data = {"title": title, "url": url, "content": text}

    with open(os.path.join("data", f"{title}.json"), "w") as f:  # Create individual JSON files
        json.dump(data, f, indent=4)


def crawl_wikipedia(start_url, max_depth=2):
    """Crawls Wikipedia pages."""
    init_data_folder()  # Create data folder if it doesn't exist

    rp = RobotFileParser()
    rp.set_url("https://en.wikipedia.org/robots.txt")
    rp.read()

    visited = set()
    to_visit = [(start_url, 0)]  # A queue of (url, depth) pairs

    while to_visit:
        current_url, depth = to_visit.pop(0)

        if current_url not in visited:
            if rp.can_fetch("*", current_url):
                visited.add(current_url)
                print(f"Visiting: {current_url} at depth {depth}")

                response = requests.get(current_url)
                response.raise_for_status()

                process_and_store_page(current_url, response.content)  # Store data

                if depth < max_depth:
                    links = get_wiki_links(current_url)
                    for link in links:
                        to_visit.append((link, depth + 1))
            else:
                print(f"Skipping: {current_url} (Blocked by robots.txt)")

            time.sleep(1)  # Delay to be polite


if __name__ == "__main__":
    start_page = "https://en.wikipedia.org/wiki/Web_scraping"
    crawl_wikipedia(start_page)  # Start the crawl
