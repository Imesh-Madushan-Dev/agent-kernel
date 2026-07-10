
# Farmer Advisor — Architecture & Build Spec (Agent Kernel Use Case)

> Hand this file to Claude Code as the source of truth. Build strictly inside
> `use-cases/farmer-advisor/`. Do NOT modify the framework core (`ak-py/`).
> Follow Agent Kernel conventions found in `examples/cli/adk`, `examples/cli/multi`,
> and `examples/cli/guardrail`.

## 1. Overview

A WhatsApp-based multi-agent assistant for smallholder farmers.
- **SDG 2 (Zero Hunger)**, with secondary impact on SDG 1 & SDG 8.
- Built on **Agent Kernel** using **Google ADK (Gemini)** as the model layer.
- **WhatsApp** is the user-facing channel (Agent Kernel native integration).

## 2. Tech Stack

| Layer            | Choice                                        |
| ---------------- | --------------------------------------------- |
| Framework        | Agent Kernel                                  |
| Model / Agents   | Google ADK (Gemini 2.x)                       |
| Interface        | WhatsApp (AK channel)                         |
| Session / Memory | AK session store (in-memory → Redis for prod) |
| Guardrails       | AK guardrail hooks (PII + content)            |
| Config           | `config.yaml` + `.env`                        |
| Lang / Tooling   | Python 3.12, uv, black, isort, pytest         |

## 3. Design Principles (industrial consistency)

1. **Feature-first, not type-first** — each agent is a self-contained module
   with its own instructions, tools, and tests.
2. **Single Responsibility** — one agent = one domain. Orchestrator only routes.
3. **Thin agents, fat tools** — business logic lives in `tools/`, not in prompts.
4. **Config over hardcoding** — models, keys, thresholds live in config/env.
5. **Typed everything** — type hints on every function; Pydantic for I/O schemas.
6. **No secrets in git** — `.env` is git-ignored; `.env.example` is committed.
7. **Deterministic, testable** — tools are pure functions where possible; agents
   are covered by pytest (fuzzy/semantic modes per DEVELOPER_GUIDE).
8. **Conventional commits** — `feat:`, `fix:`, `docs:`, `test:`, `chore:`.

## 4. Directory Structure

```

use-cases/farmer-advisor/

├── [README.md](http://README.md)                  # 4 required sections (problem, solution, setup, run)

├── [SPEC.md](http://SPEC.md)                    # coding-agent-readable spec (this doc, trimmed)

├── [AGENTS.md](http://AGENTS.md)                  # agent-readable project docs

├── config.yaml                # AK settings (model, channel, guardrails, session)

├── .env.example               # template for secrets (committed)

├── .env                       # real secrets (GIT-IGNORED)

├── .gitignore

├── pyproject.toml             # deps for this use case (if isolated)

├── [main.py](http://main.py)                    # entrypoint: builds module, runs CLI / channel

│

├── src/

│   └── farmer_advisor/

│       ├── **init**.py

│       ├── [app.py](http://app.py)             # assembles orchestrator + agents into AK module

│       ├── [settings.py](http://settings.py)        # loads/validates config.yaml + .env (Pydantic)

│       │

│       ├── agents/

│       │   ├── **init**.py

│       │   ├── [orchestrator.py](http://orchestrator.py)    # triage/routing agent (handoffs)

│       │   ├── crop_[disease.py](http://disease.py)    # diagnose disease, suggest treatment

│       │   ├── market_[price.py](http://price.py)    # current crop market prices

│       │   └── [weather.py](http://weather.py)         # forecast + spray/irrigation advice (BONUS)

│       │

│       ├── tools/

│       │   ├── **init**.py

│       │   ├── crop_disease_[tools.py](http://tools.py)   # lookup/diagnose logic

│       │   ├── market_[tools.py](http://tools.py)         # price fetch (API/mock)

│       │   └── weather_[tools.py](http://tools.py)        # forecast fetch (API/mock)

│       │

│       ├── prompts/

│       │   ├── [orchestrator.md](http://orchestrator.md)

│       │   ├── crop_[disease.md](http://disease.md)

│       │   ├── market_[price.md](http://price.md)

│       │   └── [weather.md](http://weather.md)

│       │

│       ├── guardrails/

│       │   ├── **init**.py

│       │   ├── [pii.py](http://pii.py)              # strip/deny phone, NIC, location if needed

│       │   └── [content.py](http://content.py)          # block unsafe/off-topic content

│       │

│       ├── channels/

│       │   └── [whatsapp.py](http://whatsapp.py)         # WhatsApp wiring (AK integration)

│       │

│       ├── memory/

│       │   └── [session.py](http://session.py)          # session store config (farmer history)

│       │

│       └── schemas/

│           ├── **init**.py

│           └── [models.py](http://models.py)           # Pydantic request/response models

│

├── data/

│   ├── crop_diseases.json      # seed knowledge (offline fallback)

│   └── market_prices.sample.json

│

├── tests/

│   ├── test_orchestrator_[routing.py](http://routing.py)

│   ├── test_crop_disease_[agent.py](http://agent.py)

│   ├── test_market_price_[agent.py](http://agent.py)

│   ├── test_[guardrails.py](http://guardrails.py)

│   └── [conftest.py](http://conftest.py)

│

├── scripts/

│   ├── run_[cli.sh](http://cli.sh)              # local dev: run via CLI

│   └── run_[whatsapp.sh](http://whatsapp.sh)         # run with WhatsApp channel

│

└── docs/

├── [architecture.md](http://architecture.md)         # diagrams + agent handoff flow

└── [demo-script.md](http://demo-script.md)          # 5-min demo walkthrough for judges

```

## 5. Files Claude Code Should Create — priority order

**Phase 1 — Skeleton & config**
1. `config.yaml`, `.env.example`, `.gitignore`, `pyproject.toml`
2. `src/farmer_advisor/settings.py` (load + validate config/env)
3. `src/farmer_advisor/schemas/models.py`

**Phase 2 — Core agents (CORE SCOPE)**
4. `prompts/orchestrator.md`, `prompts/crop_disease.md`, `prompts/market_price.md`
5. `tools/crop_disease_tools.py`, `tools/market_tools.py`
6. `agents/crop_disease.py`, `agents/market_price.py`, `agents/orchestrator.py`
7. `src/farmer_advisor/app.py` (wire agents + handoffs into AK module)
8. `main.py` (entrypoint via `CLI.main()`)

**Phase 3 — Compliance & interface**
9. `guardrails/pii.py`, `guardrails/content.py`
10. `channels/whatsapp.py`
11. `memory/session.py`

**Phase 4 — Bonus**
12. `tools/weather_tools.py`, `agents/weather.py`, `prompts/weather.md`
13. Photo-based diagnosis (Gemini vision) in `crop_disease` tool

**Phase 5 — Docs & tests**
14. All `tests/*`
15. `README.md`, `SPEC.md`, `AGENTS.md`, `docs/*`

## 6. Agent Design

### Orchestrator (routing)
- Instructions: classify farmer intent → hand off to the right specialist.
- Handoffs: `crop_disease`, `market_price`, `weather`.
- Never answers domain questions itself; only routes + small talk.

### Crop-Disease Agent
- Input: text symptoms and/or a photo.
- Tools: `diagnose_from_symptoms()`, `diagnose_from_image()` (Gemini vision, bonus),
  `get_treatment(disease_id)`.
- Output (Pydantic): `{ disease, confidence, treatment, prevention }`.

### Market-Price Agent
- Tools: `get_price(crop, market?)` — real API if available, else `data/*.json`.
- Output: `{ crop, market, price, unit, as_of }`.

### Weather Agent (bonus)
- Tools: `get_forecast(location)`, advice on spraying/irrigation windows.

## 7. Guardrails (30% + compliance)

- **Input guardrail**: block prompt-injection / off-topic / unsafe requests.
- **PII guardrail**: redact phone/NIC before logging; never echo secrets.
- Wire as pre/post execution hooks per `examples/cli/guardrail`.

## 8. Config & Secrets

`config.yaml`
```

app:

name: farmer-advisor

model:

provider: google-adk

name: gemini-2.0-flash

channel:

type: whatsapp

session:

store: memory        # switch to redis for production

guardrails:

pii: true

content: true

```

`.env.example`
```

GEMINI_API_KEY=

WHATSAPP_TOKEN=

WHATSAPP_PHONE_ID=

```

## 9. Testing (per DEVELOPER_GUIDE)

- `uv run pytest` from `ak-py` (or use-case root if isolated).
- Cover: orchestrator routes correctly, each agent returns valid schema,
  guardrails block bad input. Use AK fuzzy/semantic test modes.
- Run `make lint-check-all` / `make lint-all` (black + isort) before commits.

## 10. Definition of Done

- [ ] Core: orchestrator + crop_disease + market_price fully working
- [ ] WhatsApp channel responds end-to-end
- [ ] At least one guardrail active
- [ ] `config.yaml` present (no startup warning)
- [ ] Tests green, lint clean
- [ ] README (4 sections) + SPEC.md + AGENTS.md
- [ ] Demo video ≤5 min
- [ ] Submitted: fork link + all members' GitHub IDs


