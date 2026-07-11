from playwright.sync_api import sync_playwright
import pandas as pd
import time

dataset = []
seen = set()

TARGET = 7500

with sync_playwright() as p:

    browser = p.chromium.launch(headless=False)

    page = browser.new_page()

    page_number = 1

    while len(dataset) < TARGET:

        print(f"\nPage {page_number}")

        page.goto(
            f"https://www.bd-pratidin.com/sports?page={page_number}",
            wait_until="domcontentloaded",
            timeout=60000
        )

        page.wait_for_timeout(3000)

        headlines = page.locator("h5.mt-3.mt-lg-0.ps-3.fw-bold-mob")
        links = page.locator("a.stretched-link")

        h_count = headlines.count()
        l_count = links.count()

        print("Headlines:", h_count)
        print("Links:", l_count)

        if h_count == 0:
            break

        new_articles = 0

        for i in range(min(h_count, l_count)):

            headline = headlines.nth(i).inner_text().strip()
            url = links.nth(i).get_attribute("href")

            if not headline or not url:
                continue

            if url in seen:
                continue

            seen.add(url)

            dataset.append({
                "source": "Bangladesh Pratidin",
                "headline": headline,
                "url": url
            })

            new_articles += 1

        print("Collected:", len(dataset))

        if new_articles == 0:
            print("No new articles.")
            break

        page_number += 1

        time.sleep(1)

    browser.close()


df = pd.DataFrame(dataset)

df.insert(0, "id", range(1, len(df) + 1))

df.to_csv(
    "bd_pratidin_sports.csv",
    index=False,
    encoding="utf-8-sig"
)

print(df.head())
print(f"Saved {len(df)} headlines.")