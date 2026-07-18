"""
majority_vote.py

Create final labels using majority voting.
"""

import os
from collections import Counter

import pandas as pd

# ==========================================================
# CONFIG
# ==========================================================

MERGED_FOLDER = "data/merged"

FINAL_FOLDER = "data/final"

os.makedirs(FINAL_FOLDER, exist_ok=True)

# ==========================================================


def majority_vote(labels):
    """
    Return the majority label.
    """

    labels = [
        str(x).strip()
        for x in labels
        if pd.notna(x) and str(x).strip() != ""
    ]

    if len(labels) == 0:
        return None

    counter = Counter(labels)

    return counter.most_common(1)[0][0]


def agreement(labels):
    """
    Return agreement ratio.

    Example:

    Yes Yes Yes -> 3/3

    Yes Yes No -> 2/3
    """

    labels = [
        str(x).strip()
        for x in labels
        if pd.notna(x) and str(x).strip() != ""
    ]

    if len(labels) == 0:
        return "0/3"

    counter = Counter(labels)

    return f"{counter.most_common(1)[0][1]}/3"


def process_file(filename):

    path = os.path.join(
        MERGED_FOLDER,
        filename
    )

    df = pd.read_csv(path)

    final_checkworthy = []

    final_sentiment = []

    checkworthy_agreement = []

    sentiment_agreement = []

    manual_review = []

    for _, row in df.iterrows():

        check_labels = [

            row["qwen_checkworthy"],
            row["gemma_checkworthy"],
            row["llama_checkworthy"]

        ]

        sentiment_labels = [

            row["qwen_sentiment"],
            row["gemma_sentiment"],
            row["llama_sentiment"]

        ]

        cw = majority_vote(check_labels)

        st = majority_vote(sentiment_labels)

        final_checkworthy.append(cw)

        final_sentiment.append(st)

        cw_agree = agreement(check_labels)

        st_agree = agreement(sentiment_labels)

        checkworthy_agreement.append(cw_agree)

        sentiment_agreement.append(st_agree)

        # Manual review if not unanimous

        if cw_agree != "3/3" or st_agree != "3/3":

            manual_review.append(True)

        else:

            manual_review.append(False)

    df["final_checkworthy"] = final_checkworthy

    df["final_sentiment"] = final_sentiment

    df["checkworthy_agreement"] = checkworthy_agreement

    df["sentiment_agreement"] = sentiment_agreement

    df["manual_review"] = manual_review

    output = os.path.join(
        FINAL_FOLDER,
        filename
    )

    df.to_csv(
        output,
        index=False,
        encoding="utf-8-sig"
    )

    print(f"Saved -> {output}")


def main():"""
majority_vote.py

Perform majority voting on outputs from
Qwen, Gemma and Llama.
"""

import os
import glob
from collections import Counter

import pandas as pd


# ==========================================================
# CONFIG
# ==========================================================

MERGED_FOLDER = "merged"

OUTPUT_FOLDER = "final"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)


# ==========================================================
# VALID LABELS
# ==========================================================

VALID_CHECKWORTHY = {"Yes", "No"}

VALID_SENTIMENT = {
    "Positive",
    "Neutral",
    "Negative"
}


# ==========================================================
# CLEAN LABEL
# ==========================================================

def clean_label(value):

    if pd.isna(value):
        return None

    value = str(value).strip()

    if value == "":
        return None

    return value


# ==========================================================
# MAJORITY VOTE
# ==========================================================

def majority_vote(labels):

    labels = [clean_label(x) for x in labels]

    labels = [x for x in labels if x is not None]

    if len(labels) == 0:
        return None

    counter = Counter(labels)

    winner = counter.most_common(1)[0][0]

    return winner


# ==========================================================
# TIE DETECTION
# ==========================================================

def has_tie(labels):

    labels = [clean_label(x) for x in labels]

    labels = [x for x in labels if x is not None]

    if len(labels) == 0:
        return True

    counter = Counter(labels)

    values = list(counter.values())

    if len(values) == 1:
        return False

    values.sort(reverse=True)

    return values[0] == values[1]


# ==========================================================
# PROCESS ONE FILE
# ==========================================================

def process_file(csv_file):

    filename = os.path.basename(csv_file)

    print(f"Processing {filename}")

    df = pd.read_csv(csv_file)

    final_checkworthy = []

    final_sentiment = []

    review_needed = []

    agreement_score = []

    for _, row in df.iterrows():

        check_labels = [

            row["qwen_checkworthy"],
            row["gemma_checkworthy"],
            row["llama_checkworthy"]

        ]

        sentiment_labels = [

            row["qwen_sentiment"],
            row["gemma_sentiment"],
            row["llama_sentiment"]

        ]

        cw = majority_vote(check_labels)

        st = majority_vote(sentiment_labels)

        final_checkworthy.append(cw)

        final_sentiment.append(st)

        tie = has_tie(check_labels) or has_tie(sentiment_labels)

        review_needed.append(tie)

        score = len(set(check_labels)) + len(set(sentiment_labels))

        agreement_score.append(score)

    df["final_checkworthy"] = final_checkworthy

    df["final_sentiment"] = final_sentiment

    df["manual_review"] = review_needed

    df["agreement_score"] = agreement_score

    output_file = os.path.join(
        OUTPUT_FOLDER,
        filename
    )

    df.to_csv(
        output_file,
        index=False,
        encoding="utf-8-sig"
    )

    print("Saved:", output_file)


# ==========================================================
# MAIN
# ==========================================================

def main():

    files = glob.glob(
        os.path.join(MERGED_FOLDER, "*.csv")
    )

    print(f"Found {len(files)} merged files")

    for file in files:

        process_file(file)

    print("=" * 60)

    print("ALL DONE")


# ==========================================================

if __name__ == "__main__":

    main()

    files = [

        f

        for f in os.listdir(MERGED_FOLDER)

        if f.endswith(".csv")

    ]

    print(f"Found {len(files)} merged files.")

    for file in files:

        process_file(file)

    print("\nFinished.")


if __name__ == "__main__":
    main()