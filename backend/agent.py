from pydantic_ai import Agent
from schemas import Insight
from pydantic_ai.models.openai import OpenAIModel
from config import OPENROUTER_API_KEY, MODEL_NAME, BASE_URL


model = OpenAIModel(
    model_name=MODEL_NAME,
    base_url=BASE_URL,   # ✅ allowed
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
