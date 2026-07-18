"""
storage.py

Thread-safe storage layer.
"""

from __future__ import annotations

import csv
import json
import threading
from pathlib import Path
from typing import Iterable

from config import (
    CSV_COLUMNS,
    CSV_FILE,
    JSON_FILE,
    VISITED_FILE,
    FAILED_FILE,
)

from models import Book


class Storage:

    def __init__(self):

        CSV_FILE.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.lock = threading.Lock()

    # ---------------------------------------------------------
    # Internal
    # ---------------------------------------------------------

    def _row(self, book: Book) -> dict:
        """
        Return only columns that exist in CSV_COLUMNS.
        """

        data = book.to_dict()

        return {
            column: data.get(column, "")
            for column in CSV_COLUMNS
        }

    # ---------------------------------------------------------
    # CSV
    # ---------------------------------------------------------

    def save_book(self, book: Book):

        row = self._row(book)

        with self.lock:

            write_header = not CSV_FILE.exists()

            with open(
                CSV_FILE,
                "a",
                newline="",
                encoding="utf-8-sig",
            ) as f:

                writer = csv.DictWriter(
                    f,
                    fieldnames=CSV_COLUMNS,
                    extrasaction="ignore",
                )

                if write_header:
                    writer.writeheader()

                writer.writerow(row)

    # ---------------------------------------------------------

    def save_books(
        self,
        books: Iterable[Book],
    ):

        books = list(books)

        if not books:
            return

        with self.lock:

            write_header = not CSV_FILE.exists()

            with open(
                CSV_FILE,
                "a",
                newline="",
                encoding="utf-8-sig",
            ) as f:

                writer = csv.DictWriter(
                    f,
                    fieldnames=CSV_COLUMNS,
                    extrasaction="ignore",
                )

                if write_header:
                    writer.writeheader()

                for book in books:
                    writer.writerow(
                        self._row(book)
                    )

    # ---------------------------------------------------------
    # JSON
    # ---------------------------------------------------------

    def save_json(
        self,
        books: Iterable[Book],
    ):

        with self.lock:

            with open(
                JSON_FILE,
                "w",
                encoding="utf-8",
            ) as f:

                json.dump(
                    [book.to_dict() for book in books],
                    f,
                    ensure_ascii=False,
                    indent=2,
                )

    # ---------------------------------------------------------
    # Visited
    # ---------------------------------------------------------

    def load_visited(self):

        if not VISITED_FILE.exists():
            return set()

        with open(
            VISITED_FILE,
            "r",
            encoding="utf-8",
        ) as f:

            return {
                line.strip()
                for line in f
                if line.strip()
            }

    # ---------------------------------------------------------

    def mark_visited(
        self,
        book_id: int,
    ):

        with self.lock:

            with open(
                VISITED_FILE,
                "a",
                encoding="utf-8",
            ) as f:

                f.write(f"{book_id}\n")

    # ---------------------------------------------------------
    # Failed
    # ---------------------------------------------------------

    def mark_failed(
        self,
        book_id: int,
    ):

        with self.lock:

            with open(
                FAILED_FILE,
                "a",
                encoding="utf-8",
            ) as f:

                f.write(f"{book_id}\n")

    # ---------------------------------------------------------
    # Utilities
    # ---------------------------------------------------------

    def clear_csv(self):

        if CSV_FILE.exists():
            CSV_FILE.unlink()

    def clear_json(self):

        if JSON_FILE.exists():
            JSON_FILE.unlink()

    def clear_visited(self):

        if VISITED_FILE.exists():
            VISITED_FILE.unlink()

    def clear_failed(self):

        if FAILED_FILE.exists():
            FAILED_FILE.unlink()

    def clear_all(self):

        self.clear_csv()
        self.clear_json()
        self.clear_visited()
        self.clear_failed()