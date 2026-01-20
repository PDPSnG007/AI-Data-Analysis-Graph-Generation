from pydantic_ai import Agent
from schemas import Insight
from pydantic_ai.models.openai import OpenAIModel
from config import MODEL_NAME

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
