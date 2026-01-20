import os

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_API_KEY = OPENROUTER_API_KEY.strip().replace("\n", "").replace("\r", "")
if not OPENROUTER_API_KEY:
    raise RuntimeError("OPENROUTER_API_KEY is not set")

MODEL_NAME = os.getenv("MODEL_NAME", "mistralai/mistral-7b-instruct").strip()
BASE_URL = "https://openrouter.ai/api/v1"
