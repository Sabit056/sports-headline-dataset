"""
annotate.py

Batch annotation using LM Studio
"""

import os
import glob
import pandas as pd
from tqdm import tqdm

from config import (
    INPUT_FOLDER,
    OUTPUT_FOLDER,
    LOG_FOLDER,
    HEADLINE_COLUMN,
    CHECKWORTHY_COLUMN,
    SENTIMENT_COLUMN,
    RAW_RESPONSE_COLUMN,
    MODEL_COLUMN,
    MODEL_NAME,
    SAVE_EVERY,
)

from api import call_api_batch

# ==========================================================
# SETTINGS
# ==========================================================

TEST_MODE = False
TEST_ROWS = 20

BATCH_SIZE = 5

CHECK_CONF_COLUMN = "checkworthy_confidence"
SENTIMENT_CONF_COLUMN = "sentiment_confidence"

# ==========================================================
# CREATE FOLDERS
# ==========================================================

os.makedirs(OUTPUT_FOLDER, exist_ok=True)
os.makedirs(LOG_FOLDER, exist_ok=True)

LOG_FILE = os.path.join(
    LOG_FOLDER,
    "annotation_errors.log"
)

# ==========================================================
# LOGGER
# ==========================================================

def log_error(message):

    with open(LOG_FILE, "a", encoding="utf-8") as f:

        f.write(message + "\n")


# ==========================================================
# ANNOTATE ONE CSV
# ==========================================================

def annotate_csv(csv_path):

    filename = os.path.basename(csv_path)

    output_csv = os.path.join(
        OUTPUT_FOLDER,
        filename
    )

    print("=" * 80)
    print(f"Processing : {filename}")

    # ------------------------------------------------------

    if os.path.exists(output_csv):

        print("Resuming previous annotation...")

        df = pd.read_csv(output_csv)
        df[CHECK_CONF_COLUMN] = pd.to_numeric(
            df[CHECK_CONF_COLUMN],
            errors="coerce"
        )

        df[SENTIMENT_CONF_COLUMN] = pd.to_numeric(
            df[SENTIMENT_CONF_COLUMN],
            errors="coerce"
        )

    else:

        print("Starting new annotation...")

        df = pd.read_csv(csv_path)

    # ------------------------------------------------------
    # Create output columns
    # ------------------------------------------------------

   # String columns
    for col in [
        CHECKWORTHY_COLUMN,
        SENTIMENT_COLUMN,
        RAW_RESPONSE_COLUMN,
        MODEL_COLUMN,
    ]:
        if col not in df.columns:
            df[col] = ""

# Float columns
    for col in [
        CHECK_CONF_COLUMN,
        SENTIMENT_CONF_COLUMN,
    ]:
        if col not in df.columns:
            df[col] = 0.0
    # ------------------------------------------------------
    # Resume position
    # ------------------------------------------------------

    start = 0

    for i in range(len(df)):

        value = str(
            df.loc[i, CHECKWORTHY_COLUMN]
        ).strip()

        if value == "" or value.lower() == "nan":

            start = i
            break

    # ------------------------------------------------------

    if TEST_MODE:

        end = min(
            start + TEST_ROWS,
            len(df)
        )

    else:

        end = len(df)

    print(f"Rows : {start} -> {end-1}")

    # ------------------------------------------------------
    # Progress Bar
    # ------------------------------------------------------

    progress = tqdm(
        range(start, end, BATCH_SIZE),
        desc=filename
    )

    # ======================================================
    # Batch Annotation Loop Starts Here
    # ======================================================
    for batch_start in progress:

        batch_end = min(
            batch_start + BATCH_SIZE,
            end
        )

        headlines = [

            str(df.loc[i, HEADLINE_COLUMN]).strip()

            for i in range(batch_start, batch_end)

        ]

        try:

            results = call_api_batch(headlines)

            # Safety check

            if len(results) != len(headlines):

                raise Exception(
                    f"Expected {len(headlines)} results "
                    f"but got {len(results)}."
                )

            # ------------------------------------------
            # Write results back to dataframe
            # ------------------------------------------

            for offset, result in enumerate(results):

                idx = batch_start + offset

                df.loc[idx, CHECKWORTHY_COLUMN] = result["checkworthy"]

                df.loc[idx, CHECK_CONF_COLUMN] = result["checkworthy_confidence"]

                df.loc[idx, SENTIMENT_COLUMN] = result["sentiment"]

                df.loc[idx, SENTIMENT_CONF_COLUMN] = result["sentiment_confidence"]

                df.loc[idx, RAW_RESPONSE_COLUMN] = result["raw_response"]

                df.loc[idx, MODEL_COLUMN] = MODEL_NAME

        except Exception as e:

            log_error(
                f"""
                File : {filename}

                Rows : {batch_start} - {batch_end-1}

                Headlines :

                {headlines}

                Error :

                {e}

                {'='*80}
                """
            ) 
            continue

        # ------------------------------------------
        # Save checkpoint
        # ------------------------------------------

        if batch_end % SAVE_EVERY == 0:

            df.to_csv(

                output_csv,

                index=False,

                encoding="utf-8-sig"

            )

    # ======================================================
    # Final Save
    # ======================================================

    df.to_csv(

        output_csv,

        index=False,

        encoding="utf-8-sig"

    )

    print(f"Finished : {filename}")
    # ==========================================================
# MAIN
# ==========================================================

def main():

    csv_files = sorted(
        glob.glob(
            os.path.join(INPUT_FOLDER, "*.csv")
        )
    )

    if len(csv_files) == 0:

        print("\nNo CSV files found.")
        return

    print("=" * 80)
    print(f"Found {len(csv_files)} CSV file(s)")
    print("=" * 80)

    for csv_path in csv_files:

        annotate_csv(csv_path)

    print("\n" + "=" * 80)
    print("ALL FILES COMPLETED")
    print("=" * 80)


# ==========================================================
# ENTRY POINT
# ==========================================================

if __name__ == "__main__":

    main()