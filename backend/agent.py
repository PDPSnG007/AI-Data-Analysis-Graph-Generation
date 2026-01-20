# agent.py
import os
from pydantic_ai import Agent
from pydantic_ai.providers import OpenRouterProvider
from schemas import Insight
from dotenv import load_dotenv

# Load .env locally
load_dotenv()

# Get API key from environment variable
api_key = os.getenv("OPENROUTER_API_KEY")
if not api_key:
    raise RuntimeError("OPENROUTER_API_KEY not set in environment")

# Initialize Agent with explicit OpenRouterProvider
agent = Agent(
    model="openrouter:mistralai/mistral-7b-instruct",
    provider=OpenRouterProvider(api_key=api_key),
    system_prompt="""
    You are a business data analyst.
    Interpret provided statistical summaries.
    Avoid speculation.
    Be concise and factual.
    """
)
