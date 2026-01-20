import os

# config.py
import os

if not os.getenv("OPENROUTER_API_KEY"):
    raise RuntimeError("OPENROUTER_API_KEY is not set")

MODEL_NAME = "mistralai/mistral-7b-instruct"
BASE_URL = "https://openrouter.ai/api/v1"

