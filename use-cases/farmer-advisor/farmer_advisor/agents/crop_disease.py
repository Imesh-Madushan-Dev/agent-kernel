from agentkernel.adk import GoogleADKToolBuilder
from google.adk.agents import Agent

from farmer_advisor.tools import diagnose_from_symptoms, get_treatment

from .language import LANGUAGE_RULES

MODEL = "gemini-3.1-flash-lite"

crop_disease_agent = Agent(
    name="crop_disease",
    model=MODEL,
    description="Specialist agent that diagnoses crop diseases from symptoms or leaf photos and suggests treatment",
    instruction="""
    You help farmers identify crop diseases and treat them.
    If the farmer sends a PHOTO: examine the image yourself — identify the crop and the visible
    symptoms (spots, color, lesions, wilting, affected part), then pass that description to
    diagnose_from_symptoms to cross-check the local knowledge base. If the plant looks healthy
    or the photo is not a plant, say so honestly.
    If the farmer describes symptoms in text: ask for the crop name and visible symptoms if not given.
    Always use the diagnose_from_symptoms tool to diagnose; use get_treatment for a known disease.
    Reply with: disease name, confidence, treatment steps, and prevention tips.
    Keep answers short and simple — farmers read them on WhatsApp. Refuse non-farming questions.
    """
    + LANGUAGE_RULES,
    tools=GoogleADKToolBuilder.bind([diagnose_from_symptoms, get_treatment]),
)
