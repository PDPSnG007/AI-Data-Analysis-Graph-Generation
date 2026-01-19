from pydantic_ai import Agent
from schemas import Insight


agent = Agent(
    model="openrouter:mistralai/mistral-7b-instruct",
    system_prompt="""
    You are a business data analyst.
    Interpret provided statistical summaries.
    Avoid speculation.
    Be concise and factual.
    """
)
