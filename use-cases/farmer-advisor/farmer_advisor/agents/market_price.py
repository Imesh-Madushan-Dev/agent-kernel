from agentkernel.adk import GoogleADKToolBuilder
from google.adk.agents import Agent

from farmer_advisor.tools import get_price

from .language import LANGUAGE_RULES

MODEL = "gemini-3.1-flash-lite"

market_price_agent = Agent(
    name="market_price",
    model=MODEL,
    description="Specialist agent for current crop market prices",
    instruction="""
    You give farmers current market prices for their crops.
    Always use the get_price tool. If the farmer names a market, pass it; otherwise show all markets.
    Reply with: crop, price per unit for each market, and the as-of date. Keep it short.
    Refuse non-farming questions.
    """
    + LANGUAGE_RULES,
    tools=GoogleADKToolBuilder.bind([get_price]),
)
