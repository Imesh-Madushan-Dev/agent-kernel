# Farmer Advisor — SPEC

## Goal
WhatsApp assistant for smallholder farmers (SDG 2 — Zero Hunger).

## Agents (`agents/`)
- `orchestrator` — routes to the right specialist via ADK `transfer_to_agent`; never answers domain questions.
- `crop_disease` — diagnoses from text symptoms (`diagnose_from_symptoms`, `get_treatment`).
- `market_price` — current crop prices (`get_price`).
- `weather` — 3-day forecast + spray/irrigation advice (`get_forecast`).

## Framework
Google ADK (Gemini 3.1 Flash-Lite) via Agent Kernel (`GoogleADKModule`).

## Interface
WhatsApp (Agent Kernel native channel, config-driven in `config.yaml`). CLI for local dev.

## Capabilities
- Multi-agent handoffs (orchestrator → specialists)
- Guardrails as AK `PreHook`s: PII redaction (phone/NIC) + content/injection filter (`guardrails.py`)
- Session memory via AK session store (in-memory; Redis-ready)

## Data
- `data/crop_diseases.json` — offline disease knowledge base
- `data/market_prices.sample.json` — sample price feed (swap for a real API in `tools.py`)

## Success criteria
Farmer asks a question on WhatsApp → correct specialist answers with actionable advice.
