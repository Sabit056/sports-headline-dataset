"""
engine.py

Main scraping engine.
"""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Iterable

from crawler import GenreCrawler
from detail_scraper import DetailScraper, get_scraper
from storage import Storage
from utils import logger
from tqdm import tqdm


class ScraperEngine:

    def __init__(
        self,
        workers: int = 10,
    ):

        self.workers = workers

        self.storage = Storage()

        self.visited = self.storage.load_visited()

    # ---------------------------------------------------------

    def _scrape_one(
        self,
        book,
    ):

        if str(book.book_id) in self.visited:
            return None

        try:

            scraper = get_scraper()

            scraper.scrape(book)

            self.storage.save_book(book)

            self.storage.mark_visited(book.book_id)

            self.visited.add(str(book.book_id))

            return book

        except Exception as e:

            self.storage.mark_failed(book.book_id)

            logger.exception(
                f"Book {book.book_id} failed: {e}"
            )

            return None

    # ---------------------------------------------------------

    def discover_books(
        self,
        genres: Iterable[tuple[int, str]],
    ):

        unique = {}

        with GenreCrawler() as crawler:

            for genre_id, slug in genres:

                logger.info(
                    f"Crawling genre: {slug}"
                )

                books = crawler.crawl_genre(
                    genre_id,
                    slug,
                )

                for book in books:

                    unique.setdefault(
                        book.book_id,
                        book,
                    )

        books = list(unique.values())

        logger.info(
            f"Discovered {len(books)} unique books."
        )

        return books

    # ---------------------------------------------------------

    def scrape_books(
        self,
        books,
    ):

        success = 0
        failed = 0

        with ThreadPoolExecutor(
            max_workers=self.workers,
        ) as executor:

            futures = [
                executor.submit(
                    self._scrape_one,
                    book,
                )
                for book in books
            ]

            for future in tqdm(
                as_completed(futures),
                total=len(futures),
                desc="Scraping books",
            ):

                result = future.result()

                if result is None:
                    failed += 1
                else:
                    success += 1

        logger.info(
            f"Finished scraping."
        )

        logger.info(
            f"Success : {success}"
        )

        logger.info(
            f"Failed  : {failed}"
        )

    # ---------------------------------------------------------

    def run(
        self,
        genres,
    ):

        logger.info("=" * 80)

        logger.info(
            "Starting crawler..."
        )

        logger.info("=" * 80)

        books = self.discover_books(
            genres,
        )
        books = [
            b
            for b in books
            if str(b.book_id) not in self.visited
        ]
        logger.info(
            f"{len(books)} books remaining."
        )
        logger.info(
            f"{len(books)} unique books found."
        )

        self.scrape_books(
            books,
        )

        logger.info("=" * 80)

        logger.info(
            "Finished."
        )

        logger.info("=" * 80)