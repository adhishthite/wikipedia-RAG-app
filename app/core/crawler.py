import hashlib
import json
import os
import time
from multiprocessing import Pool, Manager
from urllib.robotparser import RobotFileParser

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


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
            links.append("https://mr.wikipedia.org" + href)

    return links


def process_and_store_page(url: str):
    """Fetches, extracts text, creates JSON, and stores it."""
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, "html.parser")
    title = soup.find("h1", id="firstHeading").text

    # Extract relevant text (adjust selectors as needed)
    text_paragraphs = [p.text for p in soup.find_all("p")]
    text = " ".join(text_paragraphs)

    data = {"title": title, "url": url, "content": text}

    # Create a unique file name using MD5 hashing algorithm
    file_name = get_string_hash(url)

    with open(
            os.path.join("data", f"{file_name}.json"), "w"
    ) as f:  # Create individual JSON files
        json.dump(data, f, indent=4, ensure_ascii=False)


def crawl_and_process_page(args):
    """Crawls and processes a single Wikipedia page."""
    current_url, depth, max_depth, rp, visited, to_visit, crawled_urls = args

    new_links = []

    if current_url not in visited:
        visited.append(current_url)

        if rp.can_fetch("*", current_url):
            print(f"Visiting: {current_url} at depth {depth}")

            url_hash = get_string_hash(current_url)
            if url_hash not in crawled_urls:
                process_and_store_page(current_url)
            else:
                print(f"Skipping: (Already processed) {url_hash}")

            if depth < max_depth:
                links = get_wiki_links(current_url)
                for link in links:
                    if link not in visited:
                        new_links.append((link, depth + 1))
        else:
            print(f"Skipping: {current_url} (Blocked by robots.txt)")

        time.sleep(0.5)  # Delay to be polite

    return new_links


def crawl_wikipedia(start_url: str, max_depth: int = 2):
    """Crawls Wikipedia pages."""
    init_data_folder()  # Create data folder if it doesn't exist
    crawled_urls: set = get_crawled_urls()  # Get a list of already crawled URLs

    rp = RobotFileParser()
    rp.set_url("https://mr.wikipedia.org/robots.txt")
    rp.read()

    manager = Manager()
    visited = manager.list()
    to_visit = manager.list([(start_url, 0)])  # A queue of (url, depth) pairs

    with Pool(processes=os.cpu_count()) as pool:
        with tqdm(total=0, desc="Crawling", unit="page") as pbar:
            while to_visit:
                args_list = [
                    (url, depth, max_depth, rp, visited, to_visit, crawled_urls)
                    for url, depth in to_visit
                ]
                results = pool.map(crawl_and_process_page, args_list)

                new_links = [item for sublist in results for item in sublist]
                to_visit[:] = new_links
                pbar.update(len(args_list))


def get_crawled_urls(data_path: str = "data") -> set[str]:
    """Returns a list of crawled URLs."""
    if not os.path.exists(data_path):
        return set()
    # Strip the extension and get the hash of the filename
    return set([file_name.split(".")[0] for file_name in os.listdir(data_path)])


def get_string_hash(string: str) -> str:
    """Returns the MD5 hash of a string."""
    return hashlib.md5(string.encode()).hexdigest()


if __name__ == "__main__":
    start_page = "https://mr.wikipedia.org/wiki/%E0%A4%A4%E0%A4%BF%E0%A4%AC%E0%A5%87%E0%A4%9F%E0%A5%80_%E0%A4%AD%E0%A4%BE%E0%A4%B7%E0%A4%BE"
    crawl_wikipedia(start_url=start_page, max_depth=3)  # Start the crawl
