from google.adk.agents import LlmAgent

from .crop_disease import crop_disease_agent
from .market_price import market_price_agent
from .weather import weather_agent

MODEL = "gemini-2.0-flash"

orchestrator = LlmAgent(
    name="orchestrator",
    model=MODEL,
    description="Routes farmer questions to the right specialist agent",
    instruction="""
    You route farmers to the right specialist. Never answer domain questions yourself.
    Disease/pest/symptom questions -> action.transfer_to_agent to "crop_disease".
    Price/market/selling questions -> action.transfer_to_agent to "market_price".
    Weather/rain/spraying/irrigation timing questions -> action.transfer_to_agent to "weather".
    Greetings/small talk: reply briefly and say you can help with crop diseases, market prices and weather.
    """,
    sub_agents=[crop_disease_agent, market_price_agent, weather_agent],
)
