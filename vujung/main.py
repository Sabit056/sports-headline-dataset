"""
main.py

Boitoi Scraper

Usage

python main.py
"""

from action_discovery import ActionDiscovery
from crawler import GenreCrawler
from discover import GenreDiscoverer
from engine import ScraperEngine


def main():

    ##############################################################
    # Discover Next.js action
    ##############################################################

    
    ##############################################################
    # Discover genres
    ##############################################################

    with GenreDiscoverer() as discover:

        genres = discover.tuples()

    ##############################################################
    # Create engine
    ##############################################################

    engine = ScraperEngine(workers=10)
    engine.run(genres)

    ##############################################################
    # Run
    ##############################################################

    engine.run(genres)

    print()

    print("=" * 70)

    print("Finished!")

    print("=" * 70)


if __name__ == "__main__":

    main()