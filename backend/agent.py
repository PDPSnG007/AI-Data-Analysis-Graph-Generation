from pydantic_ai import Agent
from schemas import Insight
from pydantic_ai.models.openai import OpenAIModel
from config import MODEL_NAME
import os


api_key = os.getenv("OPENAI_API_KEY")  # Only needed if you want to check
if not api_key:
    raise RuntimeError("OPENAI_API_KEY not set at runtime")
    
model = OpenAIModel(
    model_name=MODEL_NAME
)

agent = Agent(
    model="openrouter:mistralai/mistral-7b-instruct",
    system_prompt="""
    You are a business data analyst.
    Interpret provided statistical summaries.
    Avoid speculation.
    Be concise and factual.
    """
)
