"""Input guardrails: PII redaction + off-topic/injection blocking, per AK PreHook interface."""

import re

from agentkernel.core.hooks import PreHook
from agentkernel.core.model import AgentReply, AgentReplyText, AgentRequest

# Sri Lankan NIC (old 9-digit+V/X and new 12-digit) and phone numbers
_NIC = re.compile(r"\b(?:\d{9}[VvXx]|\d{12})\b")
_PHONE = re.compile(r"\b(?:\+94|0)\d{9}\b")

_BLOCKLIST = (
    "ignore previous instructions",
    "ignore all previous",
    "system prompt",
    "you are now",
    "jailbreak",
)


class PIIRedactHook(PreHook):
    """Redacts phone numbers and NIC numbers from user input before it reaches the model/logs."""

    async def on_run(self, session, agent, requests: list[AgentRequest]) -> list[AgentRequest] | AgentReply:
        for req in requests:
            if req.type == "text":
                req.text = _PHONE.sub("[PHONE]", _NIC.sub("[NIC]", req.text))
        return requests

    def name(self) -> str:
        return "pii_redact"


class ContentFilterHook(PreHook):
    """Halts execution on prompt-injection attempts. ponytail: keyword blocklist; swap for an LLM/API guardrail if it proves too coarse."""

    async def on_run(self, session, agent, requests: list[AgentRequest]) -> list[AgentRequest] | AgentReply:
        for req in requests:
            if req.type == "text" and any(b in req.text.lower() for b in _BLOCKLIST):
                return AgentReplyText(text="Sorry, I can only help with farming questions: crop diseases, market prices, and weather.")
        return requests

    def name(self) -> str:
        return "content_filter"
