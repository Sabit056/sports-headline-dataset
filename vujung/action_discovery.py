"""
action_discovery.py

Automatically discovers the Next.js Server Action ID
used by Boitoi's infinite scrolling.
"""

from __future__ import annotations

import re

import httpx
from bs4 import BeautifulSoup

from config import (
    BASE_URL,
    HEADERS,
    REQUEST_TIMEOUT,
)

from utils import logger


class ActionDiscovery:

    ACTION_REGEX = re.compile(
        r'createServerReference\(\s*"([a-f0-9]+)".*?"getMoreCategoryBooks"',
        re.DOTALL,
    )

    def __init__(self):

        self.client = httpx.Client(
            headers=HEADERS,
            timeout=REQUEST_TIMEOUT,
            follow_redirects=True,
        )

    # ---------------------------------------------------------

    def close(self):

        self.client.close()

    # ---------------------------------------------------------

    def __enter__(self):

        return self

    def __exit__(self, *args):

        self.close()

    # ---------------------------------------------------------

    def discover(self):

        logger.info("Discovering Next.js action...")

        #
        # IMPORTANT:
        # Open ANY genre page, not /genres.
        #
        url = f"{BASE_URL}/genres/71/self-development"

        r = self.client.get(url)

        r.raise_for_status()

        soup = BeautifulSoup(r.text, "lxml")

        ########################################################
        # Find every JS bundle
        ########################################################

        bundles = []

        for script in soup.find_all("script", src=True):

            src = script.get("src")

            if not src:
                continue

            if not src.endswith(".js"):
                continue

            if src.startswith("/"):
                src = BASE_URL + src

            bundles.append(src)

        logger.info(
            f"Scanning {len(bundles)} JavaScript bundles..."
        )

        ########################################################
        # Scan every bundle
        ########################################################

        for bundle in bundles:

            try:

                js = self.client.get(bundle)

                js.raise_for_status()

                text = js.text

            except Exception:

                continue

            if "getMoreCategoryBooks" not in text:
                continue

            logger.info(
                f"Action bundle found:\n{bundle}"
            )

            m = self.ACTION_REGEX.search(text)

            if m:

                action = m.group(1)

                logger.info(
                    f"Next Action: {action}"
                )

                return action

        raise RuntimeError(
            "Could not discover getMoreCategoryBooks."
        )