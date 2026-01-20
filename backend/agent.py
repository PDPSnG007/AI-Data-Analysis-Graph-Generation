import os
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel

# Must be set at runtime!
api_key = os.getenv("OPENROUTER_API_KEY")
if not api_key:
    raise RuntimeError("OPENROUTER_API_KEY not set")

# For pydantic-ai (current version)
os.environ["OPENAI_API_KEY"] = api_key
os.environ["OPENAI_BASE_URL"] = "https://openrouter.ai/api/v1"

model = OpenAIModel(
    model_name="mistralai/mistral-7b-instruct"
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
