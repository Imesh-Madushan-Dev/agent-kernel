# Farmer Advisor Specification

## 1. Goal

Build and maintain Farmer Advisor, a multi-agent assistant for Sri Lankan smallholder farmers. The application supports SDG 2 (Zero Hunger) by providing accessible guidance about crop diseases, market prices, and weather-dependent farm decisions.

The project must remain self-contained in `use-cases/farmer-advisor/`. Do not modify Agent Kernel framework code in `ak-py/` for this use case.

## 2. User Problems

Farmers need timely, practical answers to questions such as:

- What disease may be affecting a crop, and what treatment or prevention is appropriate?
- What is the available price for a crop at a selected market?
- Is the weather suitable for spraying or irrigation?

The solution must give clear, actionable answers while protecting personal information and rejecting prompt-injection or unrelated requests.

## 3. Solution Architecture

The application uses Agent Kernel with Google ADK and Gemini. `main.py` creates one `GoogleADKModule`, registers all agents, and attaches the same pre-execution guardrails to each agent.

```text
Farmer message
    -> PIIRedactHook + ContentFilterHook
    -> orchestrator
    -> crop_disease | market_price | weather
    -> response through CLI, REST/web UI, WhatsApp, or Telegram
```

## 4. Agents

| Agent | Responsibility | Tools |
| --- | --- | --- |
| `orchestrator` | Identify the farmer's intent and transfer the request to a specialist. It must not give specialist advice itself. | ADK agent handoffs |
| `crop_disease` | Diagnose symptoms or an uploaded crop image; provide treatment and prevention. | `diagnose_from_symptoms`, `get_treatment` |
| `market_price` | Return sample market prices for a crop and optional market. | `get_price` |
| `weather` | Return a three-day forecast and advice for spraying or irrigation. | `get_forecast` |

All agents use `gemini-3.1-flash-lite` and are exported from `farmer_advisor/agents/`.

## 5. Guardrails and Session Behavior

- `PIIRedactHook` redacts Sri Lankan phone numbers and NIC values before requests reach an agent or logs.
- `ContentFilterHook` blocks prompt-injection attempts, unsafe requests, and off-topic requests.
- The default Agent Kernel session store is in-memory. `config.yaml` can be changed to a production-ready store such as Redis when required.
- REST chat is configured for token streaming. The CLI and messaging channels continue to use their appropriate request flow.

## 6. Interfaces

- **CLI:** Default local development interface, started through `uv run python main.py`.
- **Web and REST API:** `uv run python main.py serve`; the browser UI is served at `/`.
- **WhatsApp:** Agent Kernel WhatsApp handler, configured with `AK_WHATSAPP__*` environment variables and routed to `orchestrator`.
- **Telegram:** Agent Kernel Telegram handler, configured with `AK_TELEGRAM__*` environment variables and routed to `orchestrator`.

## 7. Project Structure

```text
farmer-advisor/
├── main.py
├── config.yaml
├── .env.example
├── README.md
├── AGENTS.md
├── SPEC.md
├── farmer_advisor/
│   ├── agents/                # Agent definitions and handoffs
│   ├── api/routes.py          # Web UI route
│   ├── data/                  # Offline disease data and sample prices
│   ├── hooks/guardrails.py    # PII and content guardrails
│   ├── tools/                 # Testable domain functions
│   └── cli.py                 # Terminal interface
├── web/index.html             # Existing browser UI
└── tests/                     # Tool and guardrail tests
```

## 8. Data and Configuration

- `farmer_advisor/data/crop_diseases.json` is the offline disease knowledge base.
- `farmer_advisor/data/market_prices.sample.json` is a sample market-price feed; it may be replaced by a real data source without changing the agent contract.
- `.env.example` documents all secrets. `.env` must remain untracked.
- `GOOGLE_API_KEY` is required for Gemini-powered conversations.
- WhatsApp and Telegram credentials are optional unless those channels are enabled.

## 9. Non-Functional Requirements

- Preserve the current CLI and web UI layout unless a task explicitly requests a UI change.
- Keep domain behavior in `farmer_advisor/tools/` and keep agents focused on orchestration and presentation.
- Use type hints and keep Python formatting compliant with Black and isort.
- Do not commit API keys, tokens, or webhook secrets.
- Add or update tests when changing tools or guardrails.

## 10. Validation and Definition of Done

The implementation is complete when:

1. Farmer questions are routed to the relevant specialist.
2. Disease, market-price, and weather tools return useful or graceful error responses.
3. PII and prompt-injection guardrails remain active for every agent.
4. The CLI and `serve` entry points remain runnable.
5. `uv run pytest`, `uv run black --check .`, and `uv run isort --check-only .` pass.
6. `README.md` contains the problem statement, solution overview, setup instructions, and run instructions.
