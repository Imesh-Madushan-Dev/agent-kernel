"""Farmer Advisor — WhatsApp multi-agent assistant for smallholder farmers (SDG 2).

Run locally:  python main.py   (CLI)
WhatsApp:     serve the AK API and point the Meta webhook at it (see README).
"""

from agentkernel.adk import GoogleADKModule

from agents import crop_disease_agent, market_price_agent, orchestrator, weather_agent
from guardrails import ContentFilterHook, PIIRedactHook

all_agents = [orchestrator, crop_disease_agent, market_price_agent, weather_agent]
module = GoogleADKModule(all_agents)
for agent in all_agents:
    module.pre_hook(agent, [PIIRedactHook(), ContentFilterHook()])

if __name__ == "__main__":
    import cli_ui

    cli_ui.main()
