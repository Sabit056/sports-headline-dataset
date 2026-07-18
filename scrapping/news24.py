import requests
import pandas as pd
import time

BASE_URL = "https://www.news24bd.tv/api/catpagination/category/sports?page={}"

TARGET = 8000

dataset = []
seen = set()

page = 1

headers = {
    "User-Agent": "Mozilla/5.0"
}

while len(dataset) < TARGET:

    print(f"Page {page}")

    response = requests.get(
        BASE_URL.format(page),
        headers=headers,
        timeout=30
    )

    if response.status_code != 200:
        print("Request failed:", response.status_code)
        break

    data = response.json()

    articles = data["category"]["data"]

    if not articles:
        print("No more articles.")
        break

    new_articles = 0

    for article in articles:

        article_id = article["n_id"]

        if article_id in seen:
            continue

        seen.add(article_id)

        dataset.append({
            "source": "News24",
            "headline": article["n_head"],
            "url": f"https://www.news24bd.tv/details/{article_id}"
        })

        new_articles += 1

    print(f"Collected: {len(dataset)}")

    if new_articles == 0:
        break

    page += 1
    time.sleep(0.5)

# Create DataFrame
df = pd.DataFrame(dataset)

# Add sequential ID
df.insert(0, "id", range(1, len(df) + 1))

# Save CSV
df.to_csv(
    "news24_sports_headlines.csv",
    index=False,
    encoding="utf-8-sig"
)

print(f"\nSaved {len(df)} articles.")
print(df.head())