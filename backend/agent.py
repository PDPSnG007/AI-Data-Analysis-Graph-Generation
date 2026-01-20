import os
from dotenv import load_dotenv
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel

# Load local .env
load_dotenv()

# Your OpenRouter key
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
if not OPENROUTER_API_KEY:
    raise RuntimeError("OPENROUTER_API_KEY not set")

# Configure the OpenAIModel to use OpenRouter endpoint
model = OpenAIModel(
    model_name="mistralai/mistral-7b-instruct",
    base_url="https://openrouter.ai/api/v1",  # MUST point to OpenRouter
    api_key=OPENROUTER_API_KEY
)

agent = Agent(
    model=model,
    system_prompt="""
    You are a business data analyst.
    Interpret provided statistical summaries.
    Avoid speculation.
    Be concise and factual.
    """
)
