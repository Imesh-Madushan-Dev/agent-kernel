# Farmer Advisor - Project Guide

මේ guide එකෙන් කියන්නේ අපේ මුළු repository එකේ තියෙන folders මොනවද, ඒවා මොකටද තියෙන්නේ, කොහොමද වැඩ කරන්නේ සහ අපිට ඒවගෙන් ඇති වැඩේ මොකක්ද කියලා.

---

## 📂 Repository Folder Structure Overview

මේක තමයි අපේ project එකේ main folders ටික:

```text
agent-kernel/
├── ak-py/               <- Framework core code (අත තියන්න එපා!)
├── examples/            <- Reference code සහ examples (බලලා copy-paste කරන්න විතරයි)
└── use-cases/           <- අපේ වැඩ ටික කරන්න තියෙන තැන
    └── farmer-advisor/  <- අපේ මුළු project එකම දුවන්නේ මෙතන
        ├── agents/      <- අපේ custom agents ලියන තැන
        └── member-guide/<- මේ guide එක සහ setup guides තියෙන තැන
```

---

## 🔍 Folders එකින් එක විස්තර ඇතිව

### 1. `ak-py/`
* **මොකක්ද මේ?** 
  * මේක තමයි Agent Kernel framework එකේ core Python කේතය (engine එක).
* **ඇයි මේක ඕනේ?**
  * Agents ලා අතර communication (handoffs), tools run කරන එක, memory (session) සහ WhatsApp integration වගේ හැම බර වැඩක්ම framework එකෙන් handle කරනවා.
* **කොහොමද වැඩ කරන්නේ?**
  * මේක ඇතුලේ තියෙන code එක backend එකේ දුවනවා. අපි ලියන agents ලාව framework එකට register කරලා තමයි වැඩ ගන්නේ.
* **අපි මෙතන කරන්න ඕන දේ:**
  * **කිසිම දෙයක් කරන්න එපා (Do NOT edit any file here!).** හැබැයි terminal එකෙන් tests run කරන්නෙත්, packages install කරන්නෙත් මේ folder එක ඇතුලට ගිහින් තමයි.

### 2. `examples/`
* **මොකක්ද මේ?**
  * Framework එක පාවිච්චි කරලා ලියපු සරල codes සහ templates තියෙන තැනක්.
* **ඇයි මේක ඕනේ?**
  * අපිට custom agents ලියද්දි, guardrails දාද්දි code එක ලියාගන්නේ කොහොමද කියලා බලාගන්න තියෙන හොඳම cheat sheet එක මේක තමයි.
* **කොහොමද වැඩ කරන්නේ?**
  * මේකේ තියෙනවා `cli/adk` (Gemini model එක පාවිච්චි කරන හැටි) සහ `cli/multi` (multi-agent setup එකක් හදන හැටි) වගේ දේවල්.
* **අපි මෙතන කරන්න ඕන දේ:**
  * මේ කෝඩ් බලලා, අපේ agents ලියද්දි syntax සහ design patterns කොපි කරලා පාවිච්චි කරන්න පුළුවන්.

### 3. `use-cases/farmer-advisor/`
* **මොකක්ද මේ?**
  * අපේ මුළු mini-competition project එකම (Farmer Advisor) තියෙන main folder එක.
* **ඇයි මේක ඕනේ?**
  * තරඟ විනිශ්චය මණ්ඩලය (Judges) අපේ project එක run කරලා බලන්නේ මේ folder එකට ඇවිල්ලා. ඒක නිසා මේක self-contained (වෙනමම දුවන්න පුළුවන් එකක්) වෙන්න ඕනේ.
* **අපි මෙතන කරන්න ඕන දේ:**
  * අපේ codes හැමදේම මෙතන තමයි ලියන්නේ.
  * `config.yaml` එකක් හදලා settings දාන්න ඕනේ.
  * `README.md` සහ `SPEC.md` ලියන්න ඕනේ.

### 4. `use-cases/farmer-advisor/agents/`
* **මොකක්ද මේ?**
  * අපේ ප්‍රධාන agents ලා හතරදෙනාගේ (Orchestrator, Crop Disease, Weather, Market Price) Python codes තියෙන තැන.
* **ඇයි මේක ඕනේ?**
  * හැම agent කෙනෙක්ගේම instructions, tools සහ functions වෙන වෙනම ලියන්නේ මෙතන.
* **කොහොමද වැඩ කරන්නේ?**
  * Orchestrator agent එකට user message එකක් ආවම, එයා ඒක කියවලා අදාළ specialist agent (උදා: කාලගුණය ගැන නම් Weather agent) වෙත handoff (transfer) කරනවා.
* **අපි මෙතන කරන්න ඕන දේ:**
  * Python files හදලා (e.g., `orchestrator.py`, `weather.py`, `crop_disease.py`, `market_price.py`) code එක ලියන්න ඕනේ.
