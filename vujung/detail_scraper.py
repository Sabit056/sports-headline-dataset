"""
detail_scraper.py

Scrape full information from a Boitoi book page.
"""

from __future__ import annotations

import re
import time
from typing import Optional

import httpx
from bs4 import BeautifulSoup
import threading


from config import (
    HEADERS,
    REQUEST_TIMEOUT,
)

from models import Book

_thread_local = threading.local()

def get_scraper():

    if not hasattr(_thread_local, "scraper"):

        _thread_local.scraper = DetailScraper()

    return _thread_local.scraper

class DetailScraper:

    def __init__(self):

        self.client = httpx.Client(
            headers=HEADERS,
            timeout=REQUEST_TIMEOUT,
            follow_redirects=True,
        )

    def close(self):
        self.client.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    # ---------------------------------------------------------

    @staticmethod
    def clean(text: Optional[str]) -> str:

        if not text:
            return ""

        return " ".join(text.split())

    # ---------------------------------------------------------

    def scrape(self, book: Book) -> Book:

        for attempt in range(5):

            try:

                r = self.client.get(book.url)

                r.raise_for_status()

                break

            except Exception:

                if attempt == 4:
                    raise

        time.sleep(2)
        r.raise_for_status()

        soup = BeautifulSoup(r.text, "lxml")

        ###################################################
        # Summary
        ###################################################

        summary = ""

        h3 = soup.find(
            lambda tag:
            tag.name in ("h2", "h3")
            and "About" in tag.get_text()
        )

        if h3:

            p = h3.find_next("p")

            if p:
                summary = self.clean(p.get_text())

        book.summary = summary

        ###################################################
        # Genre
        ###################################################

        genre = soup.select_one(
            'a[href^="/genres/"]'
        )

        if genre:
            book.genre = self.clean(
                genre.get_text()
            )

        ###################################################
        # Publisher
        ###################################################

        publisher = soup.select_one(
            'a[href^="/publishers/"]'
        )

        if publisher:
            book.publisher = self.clean(
                publisher.get_text()
            )

        ###################################################
        # Cover
        ###################################################

        img = soup.find(
            "img",
            alt=book.title
        )

        if img:

            src = img.get("src")

            if src:
                book.cover = src

        ###################################################
        # Meta Information
        ###################################################

        text = soup.get_text("\n", strip=True)

        def find(label):

            m = re.search(
                rf"{label}\s*(.+)",
                text
            )

            if m:
                return self.clean(
                    m.group(1)
                )

            return ""

        book.language = find("Language")
        book.published = find("Published")

        ###################################################
        # Pages
        ###################################################

        m = re.search(
            r"Pages\s*(\d+)",
            text
        )

        if m:
            book.pages = int(
                m.group(1)
            )

        ###################################################
        # Price
        ###################################################

        m = re.search(
            r"৳\s*([0-9.]+)",
            text
        )

        if m:
            book.price = float(
                m.group(1)
            )

        ###################################################
        # Rating
        ###################################################

        m = re.search(
            r"([0-9.]+)\s*\((\d+)\s*ratings?\)",
            text
        )

        if m:

            book.rating = float(
                m.group(1)
            )

            book.rating_count = int(
                m.group(2)
            )

        return book