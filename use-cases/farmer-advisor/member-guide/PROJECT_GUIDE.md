# Farmer Advisor - Project Guide

මේ guide එකෙන් කියන්නේ අපේ මුළු repository එකේ තියෙන folders මොනවද, ඒවා මොකටද තියෙන්නේ, කොහොමද වැඩ කරන්නේ සහ අපිට ඒවගෙන් ඇති වැඩේ මොකක්ද කියලා.

---

## 📂 Repository Folder Structure Overview

මේක තමයි අපේ project එකේ main folders ටික (දැන් build කරලා ඉවරයි ✅):

```text
agent-kernel/
├── ak-py/               <- Framework core code (අත තියන්න එපා!)
├── examples/            <- Reference code සහ examples (බලලා copy-paste කරන්න විතරයි)
└── use-cases/
    └── farmer-advisor/  <- අපේ මුළු project එකම දුවන්නේ මෙතන
        ├── main.py          <- Entrypoint: CLI mode + serve mode
        ├── cli_ui.py        <- ලස්සන terminal chat UI එක (rich library)
        ├── tools.py         <- Agents ලා පාවිච්චි කරන business logic (fat tools)
        ├── guardrails.py    <- PII redaction + content filter hooks
        ├── config.yaml      <- AK settings (channels, session, logging)
        ├── .env             <- API keys (GIT-IGNORED - කවදාවත් commit කරන්න එපා!)
        ├── .env.example     <- .env එකේ template එක (මේක commit කරනවා)
        ├── agents/          <- අපේ custom agents 4 දෙනා
        │   ├── orchestrator.py
        │   ├── crop_disease.py
        │   ├── market_price.py
        │   └── weather.py
        ├── api/             <- Custom API routes (web UI serve කරන router)
        ├── web/             <- Browser chat UI (index.html - WhatsApp style)
        ├── data/            <- Disease knowledge base + sample prices (JSON)
        ├── tests/           <- pytest tests (tools + guardrails)
        └── member-guide/    <- මේ guide එක සහ setup guides තියෙන තැන
```

---

## 🔍 Folders එකින් එක විස්තර ඇතිව

### 1. `ak-py/`
* **මොකක්ද මේ?**
  * මේක තමයි Agent Kernel framework එකේ core Python කේතය (engine එක).
* **ඇයි මේක ඕනේ?**
  * Agents ලා අතර communication (handoffs), tools run කරන එක, memory (session), REST API, WhatsApp/Telegram integration වගේ හැම බර වැඩක්ම framework එකෙන් handle කරනවා.
* **අපි මෙතන කරන්න ඕන දේ:**
  * **කිසිම දෙයක් කරන්න එපා (Do NOT edit any file here!).**

### 2. `examples/`
* **මොකක්ද මේ?**
  * Framework එක පාවිච්චි කරලා ලියපු සරල codes සහ templates තියෙන තැනක්.
* **අපි මෙතන කරන්න ඕන දේ:**
  * අලුත් feature එකක් දාද්දි `cli/adk`, `cli/multi`, `cli/guardrail` බලලා patterns කොපි කරන්න.

### 3. `use-cases/farmer-advisor/agents/`
* **මොකක්ද මේ?**
  * අපේ ප්‍රධාන agents ලා හතරදෙනාගේ Python codes තියෙන තැන. Model එක: **gemini-3.1-flash-lite**.
* **කොහොමද වැඩ කරන්නේ?**
  * `orchestrator` ට user message එකක් ආවම, එයා ඒක කියවලා අදාළ specialist agent එකට ADK `transfer_to_agent` එකෙන් handoff කරනවා.
  * හැම agent කෙනෙක්ම English වගේම **සිංහලෙනුත්** reply කරනවා (farmer ලියන භාෂාවෙන්).
* **Agents ලා:**
  * `orchestrator` - routing විතරයි, domain ප්‍රශ්නවලට උත්තර දෙන්නේ නෑ
  * `crop_disease` - රෝග හඳුනාගැනීම + treatment + prevention (`tools.py` → `diagnose_from_symptoms`, `get_treatment`)
  * `market_price` - වෙළඳපොල මිල (`get_price` - Pettah, Dambulla, Kandy)
  * `weather` - **සැබෑ** weather data (Open-Meteo API, free) + spraying/irrigation advice (`get_forecast`)

### 4. `tools.py` සහ `guardrails.py`
* **Thin agents, fat tools** - logic එක prompts වල නෙමෙයි, `tools.py` වල pure functions විදිහට තියෙන්නේ. ඒ නිසා LLM එක නැතුව unit test කරන්න පුළුවන්.
* `guardrails.py` වල AK PreHooks දෙකක්:
  * `PIIRedactHook` - phone numbers / NIC numbers redact කරනවා
  * `ContentFilterHook` - prompt injection / off-topic block කරනවා
* මේවා `main.py` එකේදී agents හතරටම attach වෙනවා.

### 5. `api/` සහ `web/`
* `api/routes.py` - custom FastAPI routes (industrial pattern: routes වෙනම folder එකක). දැනට `GET /` එකෙන් web chat UI එක serve කරනවා.
* `web/index.html` - WhatsApp style browser chat UI එක. **සිංහල terminal එකේ හරියට පේන්නේ නැති නිසා browser UI එක තමයි demo එකට හොඳම.**
* Agent chat API එක (`POST /api/v1/chat`) framework එකෙන්ම එනවා - අපි ලියන්න ඕන නෑ.

### 6. `data/` සහ `tests/`
* `data/crop_diseases.json` - offline disease knowledge base (crops 5ක්)
* `data/market_prices.sample.json` - sample price data
* `tests/` - `uv run pytest` වලින් run කරන්න. Tools + guardrails cover වෙනවා (LLM key එක ඕන නෑ).

---

## 🚀 Run කරන විදිහ (TL;DR)

```powershell
cd use-cases\farmer-advisor

# Terminal chat UI එක
uv run python main.py

# Web UI + REST API + WhatsApp/Telegram webhooks
uv run python main.py serve
# ↳ browser එකෙන් http://localhost:8000/ ට යන්න

# Tests
uv run pytest
```

Setup කරන විදිහ දැනගන්න `SETUP_GUIDE.md` බලන්න.
