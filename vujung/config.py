"""
config.py
Configuration for the Boitoi scraper.
"""

from pathlib import Path

# ==========================================================
# Website
# ==========================================================

BASE_URL = "https://boitoi.com.bd"

GENRES_URL = f"{BASE_URL}/genres"

BOOK_PREFIX = "/books/"

GENRE_PREFIX = "/genres/"

AUTHOR_PREFIX = "/authors/"

PUBLISHER_PREFIX = "/publishers/"

NEXT_ACTION = "6007601c467ff0c4e3b9665c8190f5c7818422514a"
# ==========================================================
# HTTP
# ==========================================================

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/138.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}


REQUEST_TIMEOUT = 30

MAX_RETRIES = 5

RETRY_DELAY = 3


# ==========================================================
# Async
# ==========================================================

# Number of concurrent requests
CONCURRENT_REQUESTS = 20

# Delay between requests (seconds)
REQUEST_DELAY = 0.15


# ==========================================================
# Playwright
# ==========================================================

HEADLESS = True

BROWSER_TIMEOUT = 60000


# ==========================================================
# Output
# ==========================================================

OUTPUT_DIR = Path("output")

OUTPUT_DIR.mkdir(exist_ok=True)

CSV_FILE = OUTPUT_DIR / "books.csv"

JSON_FILE = OUTPUT_DIR / "books.json"

VISITED_FILE = OUTPUT_DIR / "visited.txt"

FAILED_FILE = OUTPUT_DIR / "failed.txt"

LOG_FILE = OUTPUT_DIR / "scraper.log"


# ==========================================================
# Save
# ==========================================================

SAVE_EVERY = 20


# ==========================================================
# Debug
# ==========================================================

DEBUG = False

VERBOSE = True


# ==========================================================
# Regex
# ==========================================================

BOOK_URL_REGEX = r"/books/\d+/[^\"']+"

BOOK_ID_REGEX = r"/books/(\d+)/"

PRICE_REGEX = r"৳\s*([0-9.]+)"

RATING_REGEX = r"([0-9.]+)\s*\((\d+)\s*ratings?\)"


# ==========================================================
# CSV Columns
# ==========================================================

CSV_COLUMNS = [
    "book_id",
    "title",
    "author",
    "genre",
    "publisher",
    "published",
    "language",
    "pages",
    "price",
    "rating",
    "rating_count",
    "summary",
    "cover",
    "url",
    "share_url",
    "isbn",
    "reviews",
]