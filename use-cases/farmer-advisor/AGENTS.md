# Farmer Advisor: Agent Development Guide

This directory is a self-contained Agent Kernel use case. Make all project changes inside `use-cases/farmer-advisor/`; do not modify `ak-py/` for this application.

## Purpose

Farmer Advisor helps Sri Lankan smallholder farmers with crop disease symptoms, market prices, and weather-based spray or irrigation advice. It uses Google ADK agents through Agent Kernel.

## Actual Project Layout

```text
farmer-advisor/
├── main.py                    # CLI entry point; `serve` starts API, web UI, and channels
├── config.yaml                # Session, streaming, WhatsApp, and Telegram configuration
├── .env.example               # Required environment-variable template
├── farmer_advisor/
│   ├── agents/                # Orchestrator and domain specialists
│   ├── api/routes.py          # Serves the browser UI at /
│   ├── data/                  # Offline disease knowledge and sample market feed
│   ├── hooks/guardrails.py    # PII redaction and content-filter pre-hooks
│   ├── tools/                 # Deterministic domain logic
│   └── cli.py                 # Rich terminal chat interface
├── web/index.html             # Browser chat interface
├── tests/                     # Tests that do not require an LLM key
├── SPEC.md                    # Product and technical requirements
└── README.md                  # Judge-facing setup and run instructions
```

## Architecture Rules

- Keep agents thin: prompts, handoffs, and tool binding belong in `farmer_advisor/agents/`.
- Keep business logic in `farmer_advisor/tools/`; prefer deterministic, typed functions that can be tested without an LLM.
- `orchestrator` must only route requests to `crop_disease`, `market_price`, or `weather`; it must not provide specialist advice itself.
- Attach both `PIIRedactHook` and `ContentFilterHook` to every agent in `main.py`.
- Keep the package-root layout shown above. Do not introduce `src/` unless every import, test path, and runner configuration is migrated together.
- Do not change the existing web UI or CLI layout unless the task explicitly requires a UI change.
- Never commit `.env`, tokens, API keys, or webhook secrets.

## Local Development

```bash
uv sync
uv run pytest
uv run black --check .
uv run isort --check-only .
uv run python main.py
```

Use `uv run python main.py serve` to run the REST API and browser UI. `GOOGLE_API_KEY` is required for agent conversations; the tool and guardrail tests do not require it.

## Change Checklist

1. Keep all modifications under this use-case directory.
2. Add or update tests for changed tool or guardrail behavior.
3. Run the test and formatting commands above.
4. Update `README.md` whenever setup, configuration, or user-visible behavior changes.
