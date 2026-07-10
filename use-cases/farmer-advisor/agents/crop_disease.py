from agentkernel.adk import GoogleADKToolBuilder
from google.adk.agents import Agent

from tools import diagnose_from_symptoms, get_treatment

MODEL = "gemini-flash"

crop_disease_agent = Agent(
    name="crop_disease",
    model=MODEL,
    description="Specialist agent that diagnoses crop diseases and suggests treatment",
    instruction="""
    You help farmers identify crop diseases and treat them.
    Ask for the crop name and visible symptoms if not given.
    Always use the diagnose_from_symptoms tool to diagnose; use get_treatment for a known disease.
    Reply with: disease name, confidence, treatment steps, and prevention tips.
    Keep answers short and simple — farmers read them on WhatsApp. Refuse non-farming questions.
    """,
    tools=GoogleADKToolBuilder.bind([diagnose_from_symptoms, get_treatment]),
)
