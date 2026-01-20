# config.py
import os

MODEL_NAME = "mistralai/mistral-7b-instruct"
BASE_URL = "https://openrouter.ai/api/v1"

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if not OPENROUTER_API_KEY:
    raise RuntimeError("OPENROUTER_API_KEY is not set")
