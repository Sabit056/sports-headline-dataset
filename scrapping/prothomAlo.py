import requests
import pandas as pd
import time
import os

API_URL = "https://www.prothomalo.com/api/v1/collections/sports-all"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

LIMIT = 10          # Prothom Alo API page size
OFFSET = 0
TARGET = 8000       # Change to 6000 if you want

dataset = []
seen = set()

while len(dataset) < TARGET:

    params = {
        "item-type": "story",
        "offset": OFFSET,
        "limit": LIMIT
    }

    response = requests.get(API_URL, params=params, headers=HEADERS)

    if response.status_code != 200:
        print("Request failed:", response.status_code)
        break

    data = response.json()

    items = data.get("items", [])

    if not items:
        print("No more articles found.")
        break

    print(f"Offset {OFFSET} -> {len(items)} articles")

    for article in items:

        try:
            story = article["story"]

            headline = story["headline"].strip()
            url = story["url"]

            # Remove duplicates
            if headline not in seen:

                seen.add(headline)

                dataset.append({
                    "source": "Prothom Alo",
                    "headline": headline,
                    "url": url
                })

        except Exception as e:
            print("Skipped article:", e)

    print(f"Collected: {len(dataset)}")

    OFFSET += LIMIT

    time.sleep(0.2)

# ---------------- SAVE CSV ----------------

df = pd.DataFrame(dataset)

# Add serial number
df.insert(0, "id", range(1, len(df) + 1))

filename = "prothomalo_sports_headlines.csv"

df.to_csv(
    filename,
    index=False,
    encoding="utf-8-sig"
)

print("\n==============================")
print("Scraping Finished!")
print("Total Headlines:", len(df))
print("Saved As:", filename)
print("Location:", os.path.abspath(filename))
print("==============================")