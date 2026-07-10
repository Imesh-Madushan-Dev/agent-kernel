# Agent Kernel Mini Competition — Farmer Advisor Plan

<aside>
🎯

Build a **WhatsApp multi-agent Farmer Advisor** using Agent Kernel. Target SDG 2 (Zero Hunger). All code lives in `use_cases/farmer-advisor/` inside your fork.

</aside>

## 1. The Idea

A WhatsApp assistant that helps smallholder farmers with everyday decisions.

- **Crop-disease agent** — farmer sends a photo/description → identifies likely disease + treatment.
- **Weather agent** — local forecast + spraying/irrigation advice.
- **Market-price agent** — current market prices for their crop.
- **Orchestrator** — routes each question to the right agent (multi-agent handoff).

**SDG:** SDG 2 – Zero Hunger (also touches SDG 1 & SDG 8 — farmer income).

## 2. How it maps to the marking criteria

| Bucket | % | How we win it |
| --- | --- | --- |
| Idea / Use Case Value | 40% | Real Sri Lankan problem, creative, clear farmer value |
| Agent Kernel Usage | 30% | Multi-agent + handoffs + WhatsApp channel + guardrails |
| End Product | 20% | Runnable demo: ask a question → get an answer |
| Documentation | 10% | Clear README (4 sections) + [SPEC.md](http://SPEC.md) |

## 3. Where to build inside the repo

The big repo is the framework. **Your project is a self-contained folder** — do NOT edit the framework core.

```
agent-kernel/            <- the cloned repo (your fork)
├─ ak-py/                <- framework code (don't touch)
├─ examples/             <- reference only (adk, multi, guardrail...)
└─ use_cases/            <- CREATE THIS
   └─ farmer-advisor/    <- YOUR PROJECT LIVES HERE
      ├─ agents/         <- crop, weather, market, orchestrator
      ├─ README.md       <- 4 required sections
      ├─ SPEC.md         <- spec for coding agents
      ├─ AGENTS.md       <- optional, agent-readable docs
      └─ config.yaml     <- settings (fixes the earlier warning)
```

<aside>
⚠️

The competition PDF says `use_cases` (underscore); the Developer Guide says `use-cases` (hyphen). Confirm the exact name on Discord, then match it exactly so judges can run it.

</aside>

## 4. Branch to use

Never work on `develop`. Create a feature branch:

```bash
git checkout -b feature/farmer-advisor
```

Commit with conventional messages: `feat:`, `fix:`, `docs:`.

## 5. Checklist — after cloning & environment setup

- [x]  Clone the repo
- [x]  `uv sync` inside `ak-py` (venv ready)
- [x]  `import agentkernel` works
- [ ]  Star the official repo (every team member) ⭐
- [ ]  Fork the official repo (one member) — work in your fork
- [ ]  Join the Discord
- [ ]  `git remote add upstream https://github.com/yaalalabs/agent-kernel.git`
- [ ]  `git checkout -b feature/farmer-advisor`
- [ ]  Read `examples/cli/adk` (Gemini) and `examples/cli/multi` (multi-agent)
- [ ]  Create `use_cases/farmer-advisor/`
- [ ]  Add a `config.yaml` + `.env` with `GEMINI_API_KEY`
- [ ]  Build the 4 agents (crop, weather, market, orchestrator)
- [ ]  Wire WhatsApp as the interface
- [ ]  Add guardrails (PII / content)
- [ ]  Write [README.md](http://README.md) (4 sections) + [SPEC.md](http://SPEC.md)
- [ ]  Test: `uv run pytest`
- [ ]  Record demo video (≤5 min, voice-over)
- [ ]  Submit fork link + all members' GitHub IDs

## 6. [README.md](http://README.md) — required 4 sections

1. **Problem statement** — smallholder farmers lack instant, local crop/weather/market advice.
2. **Solution overview** — WhatsApp multi-agent advisor built on Agent Kernel.
3. **Setup instructions** — clone, `uv sync`, add API keys, config.
4. **How to run** — start command + example WhatsApp conversation.

## 7. [SPEC.md](http://SPEC.md) skeleton

```markdown
# Farmer Advisor — SPEC

## Goal
WhatsApp assistant for smallholder farmers (SDG 2).

## Agents
- orchestrator: routes to the right specialist
- crop_disease: diagnose from text/photo, suggest treatment
- weather: local forecast + spray/irrigation advice
- market_price: current crop prices

## Framework
Google ADK (Gemini) via Agent Kernel.

## Interface
WhatsApp (Agent Kernel channel).

## Capabilities
Multi-agent handoffs, guardrails, session memory.

## Success criteria
Farmer asks a question on WhatsApp → correct specialist answers.
```