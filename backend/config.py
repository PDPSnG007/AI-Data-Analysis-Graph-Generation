# config.py
import os

MODEL_NAME = "openrouter:mistralai/mistral-7b-instruct"

# Optional sanity check
if not os.getenv("OPENAI_API_KEY"):
    raise RuntimeError("OPENAI_API_KEY is not set")
