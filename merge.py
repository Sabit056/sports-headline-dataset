"""
merge.py

Merge annotations from multiple models.
"""

import os
import pandas as pd

# ==========================================================
# CONFIG
# ==========================================================

BASE_OUTPUT = "data/output"

MODELS = {
    "qwen": "qwen_qwen3-4b-instruct-2507",
    "gemma": "gemma-3-4b-it",
    "llama": "llama-3.2-3b-instruct"
}

MERGED_FOLDER = "data/merged"

os.makedirs(MERGED_FOLDER, exist_ok=True)

# ==========================================================


def merge_file(filename):

    print(f"Merging {filename}")

    dfs = {}

    for short_name, folder in MODELS.items():

        path = os.path.join(
            BASE_OUTPUT,
            folder,
            filename
        )

        dfs[short_name] = pd.read_csv(path)

    qwen = dfs["qwen"]

    merged = pd.DataFrame()

    # --------------------------------------------------
    # Original columns
    # --------------------------------------------------

    merged["id"] = qwen["id"]
    merged["source"] = qwen["source"]
    merged["headline"] = qwen["headline"]
    merged["url"] = qwen["url"]

    # --------------------------------------------------
    # Checkworthy
    # --------------------------------------------------

    merged["qwen_checkworthy"] = dfs["qwen"]["checkworthy"]
    merged["gemma_checkworthy"] = dfs["gemma"]["checkworthy"]
    merged["llama_checkworthy"] = dfs["llama"]["checkworthy"]

    # --------------------------------------------------
    # Sentiment
    # --------------------------------------------------

    merged["qwen_sentiment"] = dfs["qwen"]["sentiment"]
    merged["gemma_sentiment"] = dfs["gemma"]["sentiment"]
    merged["llama_sentiment"] = dfs["llama"]["sentiment"]

    # --------------------------------------------------
    # Save
    # --------------------------------------------------

    output = os.path.join(
        MERGED_FOLDER,
        filename
    )

    merged.to_csv(
        output,
        index=False,
        encoding="utf-8-sig"
    )

    print(f"Saved -> {output}")


def main():

    first_model_folder = os.path.join(
        BASE_OUTPUT,
        MODELS["qwen"]
    )

    files = [

        f

        for f in os.listdir(first_model_folder)

        if f.endswith(".csv")

    ]

    print(f"Found {len(files)} CSV files.")

    for file in files:

        merge_file(file)

    print("\nFinished merging all files.")


if __name__ == "__main__":
    main()