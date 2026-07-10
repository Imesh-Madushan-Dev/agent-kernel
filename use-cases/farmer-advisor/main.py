"""Farmer Advisor — WhatsApp multi-agent assistant for smallholder farmers (SDG 2).

Run locally:  python main.py   (CLI)
WhatsApp:     serve the AK API and point the Meta webhook at it (see README).
"""

import logging

from dotenv import load_dotenv

load_dotenv()  # GOOGLE_API_KEY + AK_WHATSAPP__* from .env, before any agentkernel/ADK import
logging.getLogger("ak").setLevel(logging.WARNING)  # silence framework INFO logs before module build

from agentkernel.adk import GoogleADKModule

from farmer_advisor.agents import crop_disease_agent, market_price_agent, orchestrator, weather_agent
from farmer_advisor.hooks import ContentFilterHook, PIIRedactHook

all_agents = [orchestrator, crop_disease_agent, market_price_agent, weather_agent]
module = GoogleADKModule(all_agents)
for agent in all_agents:
    module.pre_hook(agent, [PIIRedactHook(), ContentFilterHook()])

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "serve":
        # REST API + web chat UI (/) + WhatsApp & Telegram webhooks (/whatsapp/webhook, /telegram/webhook)
        from agentkernel.api import RESTAPI
        from agentkernel.api.handler import AgentRESTRequestHandler
        from agentkernel.telegram import AgentTelegramRequestHandler
        from agentkernel.whatsapp import AgentWhatsAppRequestHandler

        from farmer_advisor.api import web_router

        handlers = [AgentRESTRequestHandler()]
        for channel in (AgentWhatsAppRequestHandler, AgentTelegramRequestHandler):
            try:
                handlers.append(channel())
            except ValueError as e:  # channel creds not in .env -> serve without it
                print(f"[skip] {channel.__name__}: {e}")

        RESTAPI.add(web_router)
        RESTAPI.run(handlers=handlers)
    else:
        from farmer_advisor import cli

        cli.main()
