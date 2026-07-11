**Dataset Overview**

- **Description:** A collection of Bengali sports headlines scraped from major Bangladeshi news sites. Each CSV contains recent sports headlines with the article URL and source metadata.

**Files**

- **CSV_Folder/bd_pratidin_sports.csv**: Bangladesh Pratidin sports headlines
- **CSV_Folder/dhakatribune_sports_headlines.csv**: Dhaka Tribune sports headlines
- **CSV_Folder/ekattor_sports.csv**: Ekattor sports headlines
- **CSV_Folder/news24_sports_headlines.csv**: News24 sports headlines
- **CSV_Folder/prothomalo_sports_headlines.csv**: Prothom Alo sports headlines
- **CSV_Folder/the_daily_star_sports.csv**: The Daily Star sports headlines

**Schema**

- **Columns:** `id` (int), `source` (string), `headline` (string, Bangla), `url` (string)

**Quick usage (Python / pandas)**

```
import pandas as pd

# load a dataset
df = pd.read_csv("CSV_Folder/bd_pratidin_sports.csv")
print(df.info())
print(df.head())
```

**Notes**

- All files are UTF-8 encoded and contain Bengali text in the `headline` field.
- Some `url` values are protocol-relative (e.g. start with `//`) or may be site-relative; add `https:` or the site base URL before using them in requests.
- Column names are consistent across files, so you can concatenate them with `pd.concat()` for combined processing.

**Attribution & License**

- Source content belongs to the original news publishers. Use and redistribution of scraped content should respect each site's terms of service and copyright.

**Maintainer**

- Repository: this workspace
