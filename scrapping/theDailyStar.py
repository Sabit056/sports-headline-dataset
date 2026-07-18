from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import pandas as pd
import time

dataset = []
seen = set()
Target = 7500

with sync_playwright() as p:

    browser = p.chromium.launch(headless=False)
    page = browser.new_page(viewport={"width": 1366, "height": 768})

    page.goto(
        "https://bangla.thedailystar.net/sports",
        wait_until="domcontentloaded"
    )

    page.wait_for_timeout(3000)

    while len(dataset) < Target:

        soup = BeautifulSoup(page.content(), "html.parser")

        articles = soup.select("h3.card-title a")

        for article in articles:

            headline = article.get_text(strip=True)

            href = article.get("href")

            if not href:
                continue

            if href.startswith("/"):
                url = "https://bangla.thedailystar.net" + href
            else:
                url = href

            if url in seen:
                continue

            seen.add(url)

            dataset.append({
                "source": "The Daily Star",
                "headline": headline,
                "url": url
            })

        print("Collected:", len(dataset))

        try:
            button = page.locator('a[title="Go to next page"]')

            if button.count() == 0:
                print("No more pages.")
                break

            button.first.click()

            page.wait_for_load_state("domcontentloaded")
            page.wait_for_timeout(2000)

        except Exception as e:
            print("Finished:", e)
            break

    browser.close()

df = pd.DataFrame(dataset)

df.insert(0, "id", range(1, len(df) + 1))

df.to_csv(
    "the_daily_star_sports.csv",
    index=False,
    encoding="utf-8-sig"
)

print(df.head())
print(f"Saved {len(df)} headlines.")