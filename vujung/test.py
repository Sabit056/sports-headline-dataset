from crawler import GenreCrawler
from detail_scraper import DetailScraper

with GenreCrawler() as crawler:

    books = crawler.crawl_genre(
        71,
        "self-development"
    )

book = books[0]

with DetailScraper() as scraper:

    scraper.scrape(book)

print(book)