"""
prompt.py

Batch Prompt Template for Bangla Sports Headline Annotation
"""

# ==========================================================
# SYSTEM PROMPT
# ==========================================================

SYSTEM_PROMPT = """
You are an expert annotator for Bangla sports news.

Annotate every headline independently.

Return ONLY valid JSON.

For each headline output:

- checkworthy
- checkworthy_confidence
- sentiment
- sentiment_confidence

Rules

checkworthy:
Yes or No

sentiment:
Positive
Neutral
Negative

Confidence:
Decimal between 0.00 and 1.00

Do not explain.
Do not use markdown.
Return JSON only.
"""

# ==========================================================
# BUILD BATCH PROMPT
# ==========================================================

def build_prompt(headlines):

    prompt = f"""
Annotate the following {len(headlines)} Bangla sports headlines.

Return EXACTLY {len(headlines)} JSON objects in the SAME ORDER.

Example:

[
  {{
    "checkworthy":"Yes",
    "checkworthy_confidence":0.95,
    "sentiment":"Neutral",
    "sentiment_confidence":0.92
  }}
]

Headlines

"""

    for i, headline in enumerate(headlines, start=1):

        prompt += f"{i}. {headline}\n"

    prompt += """

Return ONLY the JSON array.

"""

    return prompt