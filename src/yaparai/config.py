"""Configuration — reads API key, base URL, and org ID from environment."""

import os

YAPARAI_API_KEY = os.environ.get("YAPARAI_API_KEY", "")
YAPARAI_BASE_URL = os.environ.get("YAPARAI_BASE_URL", "https://api.yaparai.com")
YAPARAI_ORG_ID = os.environ.get("YAPARAI_ORG_ID", "")
