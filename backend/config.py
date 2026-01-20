import os

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_API_KEY = OPENROUTER_API_KEY.strip().replace("\n", "").replace("\r", "")

MODEL_NAME = os.getenv("MODEL_NAME", "mistralai/mistral-7b-instruct").strip()
