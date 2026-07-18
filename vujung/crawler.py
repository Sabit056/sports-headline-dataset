"""
crawler.py

Hidden API crawler for Boitoi genres.

Uses the Next.js Server Action:
getMoreCategoryBooks(categoryId, page)

Returns lightweight Book objects.
"""

from __future__ import annotations
from config import NEXT_ACTION
import json
import re
from typing import Dict, List
from urllib.parse import quote

import httpx

from config import (
    BASE_URL,
    HEADERS,
    REQUEST_TIMEOUT,
    NEXT_ACTION,
)



from models import Book
from utils import logger


# ------------------------------------------------------------------
# Update this if Boitoi changes their deployment.
# Later we'll discover this automatically.
# ------------------------------------------------------------------




class GenreCrawler:

    def __init__(self):

        self.next_action = NEXT_ACTION

        self.client = httpx.Client(
            timeout=REQUEST_TIMEOUT,
            headers=HEADERS,
            follow_redirects=True,
        )

    def close(self):
        self.client.close()

    # -------------------------------------------------------------

    def _headers(self):

        headers = HEADERS.copy()

        headers.update(
            {
                "Accept": "text/x-component",
                "Content-Type": "text/plain;charset=UTF-8",
                "Origin": BASE_URL,
                "Next-Action": self.next_action
            }
        )

        return headers

    # -------------------------------------------------------------

    def _book_url(
        self,
        book_id: int,
        title: str,
    ) -> str:

        slug = quote(title.strip())

        return f"{BASE_URL}/books/{book_id}/{slug}"

    # -------------------------------------------------------------

    def fetch_page(
        self,
        genre_id: int,
        genre_slug: str,
        page: int,
    ) -> str:

        url = f"{BASE_URL}/genres/{genre_id}/{genre_slug}"

        payload = json.dumps(
            [str(genre_id), page],
            ensure_ascii=False,
        )

        response = self.client.post(
            url,
            headers=self._headers(),
            content=payload.encode("utf-8"),
        )

        response.raise_for_status()

        return response.content.decode(
            "utf-8",
            errors="replace",
        )

    # -------------------------------------------------------------

    def parse_books(
        self,
        text: str,
    ) -> List[dict]:

        match = re.search(
            r"1:(\[.*\])",
            text,
            flags=re.DOTALL,
        )

        if not match:
            return []

        try:

            return json.loads(match.group(1))

        except Exception as e:

            logger.error(e)

            return []

    # -------------------------------------------------------------

    def crawl_genre(
        self,
        genre_id: int,
        genre_slug: str,
    ) -> List[Book]:

        books: Dict[int, Book] = {}

        page = 1

        while True:

            logger.info(
                f"{genre_slug} | page {page}"
            )

            response = self.fetch_page(
                genre_id,
                genre_slug,
                page,
            )

            items = self.parse_books(response)

            if not items:

                logger.info("Reached end.")

                break

            for item in items:

                book_id = item["id"]

                if book_id in books:
                    continue

                author = ""

                if item.get("authors"):

                    author = (
                        item["authors"][0].get("name_bn")
                        or item["authors"][0].get("name")
                        or ""
                    )

                books[book_id] = Book(
                    book_id=book_id,
                    title=item.get("title", ""),
                    author=author,
                    cover=item.get("cover", ""),
                    price=float(item.get("price", 0)),
                    rating=float(item.get("rating", 0)),
                    rating_count=item.get("reviews", 0),
                    url=self._book_url(
                        book_id,
                        item.get("title", ""),
                    ),
                    share_url=item.get("share_url", ""),
                )

            page += 1

        logger.info(
            f"Collected {len(books)} books."
        )

        return list(books.values())

    # -------------------------------------------------------------

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()