import os
from pydantic_ai import Agent
from schemas import Insight

# Load local .env (optional for local testing)
from dotenv import load_dotenv
load_dotenv()

# Must match the variable name you set in Railway / .env
api_key = os.getenv("OPENROUTER_API_KEY")
if not api_key:
    raise RuntimeError("OPENROUTER_API_KEY not set in environment")

# Set environment variable for pydantic_ai to pick it up
os.environ["OPENAI_API_KEY"] = api_key 

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
