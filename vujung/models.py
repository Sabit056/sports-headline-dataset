"""
models.py

Dataclasses used throughout the scraper.
"""

from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class Book:
    """Represents a single Boitoi book."""

    book_id: int

    title: str = ""

    author: str = ""

    genre: str = ""

    publisher: str = ""

    published: str = ""

    language: str = ""

    pages: Optional[int] = None

    price: Optional[float] = None

    rating: Optional[float] = None

    rating_count: Optional[int] = None

    summary: str = ""

    cover: str = ""

    url: str = ""

    share_url: str = ""

    isbn: str = ""

    reviews: int = 0

    def to_dict(self):
        """Convert Book object to dictionary."""
        return asdict(self)

    @classmethod
    def empty(cls):
        """Return an empty Book object."""
        return cls(book_id=0)

    @property
    def has_summary(self):
        return bool(self.summary.strip())

    @property
    def has_author(self):
        return bool(self.author.strip())

    @property
    def has_genre(self):
        return bool(self.genre.strip())

    @property
    def has_publisher(self):
        return bool(self.publisher.strip())

    @property
    def is_valid(self):
        """A valid book must have an ID, title, and URL."""
        return (
            self.book_id > 0
            and bool(self.title.strip())
            and bool(self.url.strip())
        )