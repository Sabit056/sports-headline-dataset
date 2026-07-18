"""
config.py

Configuration for Bangla Sports Headline Annotation
Using LM Studio
"""

import os

# ==========================================================
# LM STUDIO
# ==========================================================

# LM Studio Local API
API_URL = "http://127.0.0.1:1234/v1/chat/completions"

# Model ID from LM Studio
MODEL_NAME = "gemma-3-4b-it"

HEADERS = {
    "Content-Type": "application/json"
}

# ==========================================================
# PATHS
# ==========================================================

# Folder containing all newspaper CSVs
INPUT_FOLDER = "data/raw"

# Output folder
OUTPUT_FOLDER = f"data/output/{MODEL_NAME}"

# Log folder
LOG_FOLDER = "logs"

# ==========================================================
# CSV COLUMN NAMES
# ==========================================================

ID_COLUMN = "id"

SOURCE_COLUMN = "source"

HEADLINE_COLUMN = "headline"

URL_COLUMN = "url"

# ==========================================================
# OUTPUT COLUMNS
# ==========================================================

CHECKWORTHY_COLUMN = "checkworthy"

SENTIMENT_COLUMN = "sentiment"

RAW_RESPONSE_COLUMN = "raw_response"

MODEL_COLUMN = "model"

# ==========================================================
# MODEL PARAMETERS
# ==========================================================

TEMPERATURE = 0.0

TOP_P = 1.0

MAX_TOKENS = 512

# ==========================================================
# API SETTINGS
# ==========================================================

TIMEOUT = 120

MAX_RETRIES = 3

RETRY_DELAY = 2

# ==========================================================
# SAVE SETTINGS
# ==========================================================

SAVE_EVERY = 50

# ==========================================================
# DEBUG
# ==========================================================

DEBUG = True

# ==========================================================
# CREATE DIRECTORIES
# ==========================================================
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
os.makedirs(LOG_FOLDER, exist_ok=True)