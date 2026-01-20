import os
from pydantic_ai import Agent
from dotenv import load_dotenv

# Load .env locally (Railway ignores this safely)
load_dotenv()

# OpenRouter key MUST be present
if not os.getenv("OPENROUTER_API_KEY"):
    raise RuntimeError("OPENROUTER_API_KEY is not set")

# pydantic-ai internally reads OPENAI_API_KEY
# so we map it explicitly
os.environ["OPENAI_API_KEY"] = os.environ["OPENROUTER_API_KEY"]

agent = Agent(
    model="openrouter:mistralai/mistral-7b-instruct",
    system_prompt="""
    You are a business data analyst.
    Interpret provided statistical summaries.
    Avoid speculation.
    Be concise and factual.
    """
)
