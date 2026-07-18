"""
utils.py

Utility functions for the Boitoi scraper.
"""

from __future__ import annotations

import logging
import random
import re
import time
from pathlib import Path
from typing import Iterable, Optional

from bs4 import BeautifulSoup

from config import (
    BASE_URL,
    HEADERS,
    LOG_FILE,
    REQUEST_DELAY,
    VERBOSE,
)


# ==========================================================
# Logging
# ==========================================================

def setup_logger(name: str = "boitoi") -> logging.Logger:
    """
    Create and return a configured logger.
    """

    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s : %(message)s",
        "%Y-%m-%d %H:%M:%S",
    )

    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


logger = setup_logger()


# ==========================================================
# HTML helpers
# ==========================================================

def soup(html: str) -> BeautifulSoup:
    """Create BeautifulSoup object."""
    return BeautifulSoup(html, "lxml")


def clean_text(text: Optional[str]) -> str:
    """Normalize whitespace."""
    if not text:
        return ""

    return re.sub(r"\s+", " ", text).strip()


def node_text(node) -> str:
    """Safely get node text."""
    if node is None:
        return ""

    return clean_text(node.get_text(" ", strip=True))


# ==========================================================
# URL helpers
# ==========================================================

def absolute_url(url: str) -> str:
    """
    Convert relative URL to absolute.
    """

    if not url:
        return ""

    if url.startswith("http"):
        return url

    if not url.startswith("/"):
        url = "/" + url

    return BASE_URL + url


def normalize_book_url(url: str) -> str:
    """
    Normalize book URL.
    """

    url = absolute_url(url)

    return url.split("?")[0].rstrip("/")


# ==========================================================
# Regex helpers
# ==========================================================

BOOK_ID_RE = re.compile(r"/books/(\d+)/")


def extract_book_id(url: str) -> int:
    """
    Extract book ID from URL.
    """

    m = BOOK_ID_RE.search(url)

    if not m:
        return 0

    return int(m.group(1))


def extract_number(text: str) -> Optional[int]:
    """
    Extract first integer.
    """

    m = re.search(r"\d+", text)

    if not m:
        return None

    return int(m.group())


def extract_float(text: str) -> Optional[float]:
    """
    Extract first float.
    """

    m = re.search(r"[0-9]+(?:\.[0-9]+)?", text)

    if not m:
        return None

    return float(m.group())


# ==========================================================
# File helpers
# ==========================================================

def load_lines(path: Path) -> set[str]:
    """
    Load text file into a set.
    """

    if not path.exists():
        return set()

    with open(path, "r", encoding="utf-8") as f:
        return {line.strip() for line in f if line.strip()}


def append_line(path: Path, text: str):
    """
    Append one line.
    """

    with open(path, "a", encoding="utf-8") as f:
        f.write(text + "\n")


# ==========================================================
# Delay
# ==========================================================

def polite_delay():
    """
    Small randomized delay.
    """

    delay = REQUEST_DELAY + random.uniform(0.2, 0.8)
    time.sleep(delay)


# ==========================================================
# Deduplicate
# ==========================================================

def unique(items: Iterable) -> list:
    """
    Preserve order while removing duplicates.
    """

    seen = set()
    out = []

    for item in items:

        if item in seen:
            continue

        seen.add(item)
        out.append(item)

    return out


# ==========================================================
# Debug
# ==========================================================

def log(message: str):
    """
    Console logging.
    """

    if VERBOSE:
        print(message)

    logger.info(message)