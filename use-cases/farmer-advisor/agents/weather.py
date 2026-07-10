from agentkernel.adk import GoogleADKToolBuilder
from google.adk.agents import Agent

from tools import get_forecast

MODEL = "gemini-3.1-flash-lite"

weather_agent = Agent(
    name="weather",
    model=MODEL,
    description="Specialist agent for weather forecasts and spraying/irrigation advice",
    instruction="""
    You give farmers the local weather forecast and practical advice.
    Always use the get_forecast tool. Advise on spraying (avoid before rain/wind) and
    irrigation (skip if rain is coming) based on the forecast.
    Keep answers short and simple. Refuse non-farming questions.
    """,
    tools=GoogleADKToolBuilder.bind([get_forecast]),
)
