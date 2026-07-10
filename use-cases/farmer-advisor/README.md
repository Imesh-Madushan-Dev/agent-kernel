# Farmer Advisor 🌾

A WhatsApp multi-agent assistant for smallholder farmers, built on **Agent Kernel** with **Google ADK (Gemini)**. Targets **SDG 2 — Zero Hunger** (secondary: SDG 1, SDG 8).

## 1. Problem Statement

Smallholder farmers in Sri Lanka lack instant, local advice on crop diseases, market prices, and weather. Extension officers are scarce, and wrong or late decisions (what to spray, when to sell, when to irrigate) directly cut yield and income.

## 2. Solution Overview

A WhatsApp assistant the farmer already knows how to use. An **orchestrator** agent routes each question to a specialist:

| Agent | What it does |
| --- | --- |
| `orchestrator` | Classifies intent, hands off to a specialist (never answers itself) |
| `crop_disease` | Diagnoses from described symptoms **or a leaf photo** (Gemini vision + local knowledge base), gives treatment + prevention |
| `market_price` | Current crop prices per market (Pettah, Dambulla, Kandy) |
| `weather` | 3-day forecast + spraying/irrigation advice |

Guardrails run as Agent Kernel pre-execution hooks on every agent: **PII redaction** (phone/NIC) and a **content filter** that blocks prompt injection and off-topic requests. Session memory is handled by the AK session store (in-memory; switch to Redis in `config.yaml` for production). The REST chat API runs in **streaming mode** (`execution.mode: stream`), so the web UI renders replies token by token.

## Project Structure

```text
farmer-advisor/
├── main.py                  # entrypoint: CLI (default) or `serve` (API + web UI + webhooks)
├── config.yaml              # AK settings: session, streaming, WhatsApp/Telegram channels
├── farmer_advisor/          # application package
│   ├── agents/              # orchestrator + specialist agents (Google ADK)
│   ├── tools/               # business logic, one module per domain (disease, market, weather)
│   ├── hooks/               # guardrail pre-hooks (PII redaction, content filter)
│   ├── api/                 # custom FastAPI routes (serves the web UI)
│   ├── data/                # disease knowledge base + sample price feed (JSON)
│   └── cli.py               # Rich terminal chat UI
├── web/                     # browser chat UI (Tailwind, streaming, photo upload)
└── tests/                   # pytest (tools + guardrails, no LLM key needed)
```

## 3. Setup Instructions

```bash
cd use-cases/farmer-advisor
uv sync                      # installs agentkernel[cli,adk]
cp .env.example .env         # then fill in your keys
```

Required in `.env`:
- `GOOGLE_API_KEY` — Gemini API key
- `AK_WHATSAPP__*` — WhatsApp Business API credentials (only needed for the WhatsApp channel)

## 4. How to Run

**Local CLI (dev):**

```bash
uv run python main.py
```

Example conversation:

```
> My rice plants have gray spots on the leaves and the tips are drying
Likely Rice Blast (high confidence). Treatment: apply tricyclazole-based fungicide...
> What is the tomato price in Dambulla?
Tomato: LKR 290/kg at Dambulla (as of 2026-07-10).
> Can I spray tomorrow in Kandy?
Tomorrow in Kandy: light rain (60% chance) — avoid spraying, wait for a dry window.
```

**Web UI + REST API (streaming):**

```bash
uv run python main.py serve
# open http://localhost:8000/ — replies stream in live; attach a plant photo for diagnosis
```

**WhatsApp channel:** serve the AK API (`uv run python main.py serve`), expose it publicly (e.g. ngrok), and set the Meta webhook to `<public-url>/whatsapp/webhook` with your verify token. `config.yaml` already routes WhatsApp messages to the `orchestrator` agent — including photos of sick plants.

**Tests:**

```bash
uv run pytest
```
