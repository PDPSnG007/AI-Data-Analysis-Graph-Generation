import os
from dotenv import load_dotenv
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel

# Load env locally
load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
if not OPENROUTER_API_KEY:
    raise RuntimeError("OPENROUTER_API_KEY not set")

model = OpenAIModel(
    model_name="mistralai/mistral-7b-instruct",
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
    default_headers={
        "HTTP-Referer": "https://ai-data-analysis-graph-generation-production.up.railway.app",
        "X-Title": "AI Data Analysis Graph Generator"
    }
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
