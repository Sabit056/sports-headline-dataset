import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

API_URL = "https://bangla.dhakatribune.com/api/theme_engine/get_ajax_contents"

headers = {
    "User-Agent": "Mozilla/5.0"
}

start = 0
count = 16

seen = set()
dataset = []

while True:

    params = {
        "widget": 622,
        "start": start,
        "count": count,
        "page_id": 1205,
        "subpage_id": 0,
        "author": 0,
        "tags": "",
        "archive_time": "",
        "filter": ""
    }

    response = requests.get(API_URL, params=params, headers=headers)

    if response.status_code != 200:
        print("Request Failed!")
        break

    data = response.json()

    soup = BeautifulSoup(data["html"], "html.parser")

    articles = soup.select("a.link_overlay")

    # Stop if no articles are returned
    if not articles:
        print("No more articles found.")
        break

    new_headlines = 0

    for article in articles:

        headline = article.get_text(strip=True)
        link = article.get("href")

        # Convert relative URL to absolute URL
        if link.startswith("//"):
            link = "https:" + link

        if headline not in seen:
            seen.add(headline)

            dataset.append({
                "source": "Kaler Kantho",
                "headline": headline,
                "url": link
            })

            new_headlines += 1

    print(f"Collected {len(dataset)} headlines...")

    # Stop if API says finished
    if data.get("finished", False):
        print("Reached the end.")
        break

    # Stop if duplicate page
    if new_headlines == 0:
        print("No new headlines.")
        break

    start += count


# ---------------- Save CSV ----------------

df = pd.DataFrame(dataset)

# Add serial ID
df.insert(0, "id", range(1, len(df) + 1))

filename = "kalerkantho_sports_headlines.csv"

df.to_csv(
    filename,
    index=False,
    encoding="utf-8-sig"
)

print("\n==============================")
print(f"Total Headlines : {len(df)}")
print(f"CSV Saved As    : {filename}")
print("Location        :", os.path.abspath(filename))
print("==============================")