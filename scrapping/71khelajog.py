import requests
from bs4 import BeautifulSoup
import pandas as pd

SOURCE = "Ekattor"
LIMIT = 7500

start = 0

dataset = []
seen = set()

while len(dataset) < LIMIT:

    url = (
        "https://ekattor.tv/api/theme_engine/get_ajax_contents"
        f"?widget=600"
        f"&start={start}"
        f"&count=10"
        f"&page_id=1095"
        f"&subpage_id=0"
        f"&author=0"
        f"&tags="
        f"&archive_time="
        f"&filter="
    )

    r = requests.get(url)

    if r.status_code != 200:
        print("Status:", r.status_code)
        break

    data = r.json()

    soup = BeautifulSoup(data["html"], "html.parser")

    new_articles = 0

    for a in soup.select("a"):

        href = a.get("href")

        if not href:
            continue

        if "/sports/" not in href:
            continue

        headline = a.get_text(" ", strip=True)

        if not headline:
            continue

        if href in seen:
            continue

        seen.add(href)

        dataset.append({
            "source": SOURCE,
            "headline": headline,
            "url": href
        })

        new_articles += 1

        if len(dataset) >= LIMIT:
            break

    print(
        f"Start={start} | "
        f"Collected={len(dataset)} | "
        f"Finished={data['finished']}"
    )

    if data["finished"]:
        break

    if new_articles == 0:
        break

    start = data["start"]

df = pd.DataFrame(dataset)

df.insert(0, "id", range(1, len(df)+1))

df.to_csv(
    "ekattor_sports.csv",
    index=False,
    encoding="utf-8-sig"
)

print(df.head())
print(f"Saved {len(df)} articles.")