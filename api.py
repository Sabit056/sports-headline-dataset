"""
api.py

Batch communication with LM Studio
"""

import json
import re
import time
import requests

from config import (
    API_URL,
    MODEL_NAME,
    HEADERS,
    TEMPERATURE,
    TOP_P,
    MAX_TOKENS,
    TIMEOUT,
    MAX_RETRIES,
    RETRY_DELAY,
    DEBUG,
)

from prompt import (
    SYSTEM_PROMPT,
    build_prompt,
)


# ==========================================================
# Exceptions
# ==========================================================

class APIError(Exception):
    pass


class JSONParseError(Exception):
    pass


# ==========================================================
# Parse confidence safely
# ==========================================================

def parse_confidence(value):

    try:

        if value is None:
            return 0.0

        if isinstance(value, str):

            value = value.replace("%", "").strip()

        value = float(value)

        if value > 1:
            value /= 100

        value = max(0.0, min(1.0, value))

        return round(value, 3)

    except:

        return 0.0


# ==========================================================
# Extract JSON Array
# ==========================================================

def extract_json_array(text):

    if text is None:

        raise JSONParseError(
            "Model returned empty response."
        )

    text = text.strip()

    text = text.replace("```json", "")
    text = text.replace("```", "")
    text = text.strip()

    match = re.search(
        r"\[.*\]",
        text,
        re.DOTALL
    )

    if not match:

        raise JSONParseError(
            f"No JSON array found.\n\n{text}"
        )

    json_text = match.group()

    try:

        return json.loads(json_text)

    except Exception as e:

        raise JSONParseError(
            f"\nInvalid JSON Array\n\n{json_text}\n\n{e}"
        )


# ==========================================================
# Build Payload
# ==========================================================

def build_payload(headlines):

    return {

        "model": MODEL_NAME,

        "messages": [

            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },

            {
                "role": "user",
                "content": build_prompt(headlines)
            }

        ],

        "temperature": TEMPERATURE,

        "top_p": TOP_P,

        "max_tokens": MAX_TOKENS

    }


# ==========================================================
# Call Batch API
# ==========================================================

def call_api_batch(headlines):

    payload = build_payload(headlines)

    for attempt in range(MAX_RETRIES):

        try:

            response = requests.post(
                API_URL,
                headers=HEADERS,
                json=payload,
                timeout=TIMEOUT
            )

            response.raise_for_status()

            data = response.json()
            print(data["choices"][0]["finish_reason"])

            message = data["choices"][0]["message"]

            content = message.get("content")

            if content is None:

                raise APIError(
                    "Model returned empty content."
                )

            if DEBUG:

                print("=" * 80)
                print("Batch Size:", len(headlines))
                print("=" * 80)
                print(content)
                print("=" * 80)

            results = extract_json_array(content)

            if len(results) != len(headlines):

                raise APIError(
                    f"Expected {len(headlines)} results "
                    f"but got {len(results)}."
                )

            annotations = []

            for item in results:

                checkworthy = (
                    item.get("checkworthy", "")
                    .strip()
                    .title()
                )

                sentiment = (
                    item.get("sentiment", "")
                    .strip()
                    .title()
                )

                if checkworthy not in ["Yes", "No"]:

                    raise APIError(
                        f"Invalid checkworthy label: {checkworthy}"
                    )

                if sentiment not in [
                    "Positive",
                    "Neutral",
                    "Negative"
                ]:

                    raise APIError(
                        f"Invalid sentiment label: {sentiment}"
                    )

                annotations.append({

                    "checkworthy": checkworthy,

                    "checkworthy_confidence":
                        parse_confidence(
                            item.get(
                                "checkworthy_confidence"
                            )
                        ),

                    "sentiment": sentiment,

                    "sentiment_confidence":
                        parse_confidence(
                            item.get(
                                "sentiment_confidence"
                            )
                        ),

                    "raw_response": json.dumps(
                        item,
                        ensure_ascii=False
                    )

                })

            return annotations

        except Exception as e:

            if DEBUG:

                print(
                    f"\nRetry {attempt+1}/{MAX_RETRIES}"
                )

                print(type(e).__name__)

                print(e)

            time.sleep(RETRY_DELAY)

    raise APIError(
        "Maximum retries exceeded."
    )