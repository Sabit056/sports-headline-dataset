"""
discover.py

Automatically discover all Boitoi genres.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

import httpx
from bs4 import BeautifulSoup

from config import (
    BASE_URL,
    HEADERS,
    REQUEST_TIMEOUT,
)

from utils import logger


@dataclass(slots=True)
class Genre:

    id: int

    slug: str

    name: str

    url: str


class GenreDiscoverer:

    def __init__(self):

        self.client = httpx.Client(
            headers=HEADERS,
            timeout=REQUEST_TIMEOUT,
            follow_redirects=True,
        )

    # ------------------------------------------------------

    def close(self):

        self.client.close()

    # ------------------------------------------------------

    def __enter__(self):

        return self

    def __exit__(self, *args):

        self.close()

    # ------------------------------------------------------

    def discover(self):

        url = f"{BASE_URL}/genres"

        logger.info(
            "Downloading genre page..."
        )

        r = self.client.get(url)

        r.raise_for_status()

        soup = BeautifulSoup(
            r.text,
            "lxml",
        )

        genres = {}

        for a in soup.select('a[href^="/genres/"]'):

            href = a.get("href")

            if not href:
                continue

            m = re.match(
                r"/genres/(\d+)/([^/?]+)",
                href,
            )

            if not m:
                continue

            genre_id = int(m.group(1))

            slug = m.group(2)

            name = a.get_text(
                " ",
                strip=True,
            )

            genres[genre_id] = Genre(
                id=genre_id,
                slug=slug,
                name=name,
                url=BASE_URL + href,
            )

        genres = sorted(
            genres.values(),
            key=lambda g: g.id,
        )

        logger.info(
            f"Discovered {len(genres)} genres."
        )

        return genres

    # ------------------------------------------------------

    def tuples(self):

        """
        Return:

        [
            (71, "self-development"),
            (88, "science-fiction"),
        ]
        """

        return [

            (g.id, g.slug)

            for g in self.discover()

        ]