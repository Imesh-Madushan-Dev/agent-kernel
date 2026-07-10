# Farmer Advisor - PC Setup Guide (Windows & PowerShell)

මේ guide එකෙන් කියන්නේ අපේ team එකේ කට්ටියට තමන්ගේ Windows PC එකේ මේ project එක run කරන්න environment එක ලේසියෙන්ම setup කරගන්න විදිහ.

---

### Step 1: Python 3.12+ install කරගන්න
1. ඔයාගේ PC එකේ Python 3.12 හෝ ඊට අලුත් version එකක් තියෙන්න ඕනේ.
2. [Python Official Website](https://www.python.org/downloads/) එකෙන් download කරලා install කරගන්න.
3. **වැදගත්:** Install කරද්දි **"Add Python to PATH"** කියන checkbox එකට tick එකක් දාන්න අමතක කරන්න එපා.

### Step 2: `uv` package manager එක install කරගන්න
මේ project එකේ dependencies handle කරන්නෙ `uv` එකෙන්. PowerShell එක open කරලා මේ command එක run කරන්න:
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```
Install වුනාට පස්සේ PowerShell එක restart කරලා `uv --version` ගහලා වැඩද කියලා check කරගන්න.

### Step 3: Project එක Clone කරලා Branch එකට මාරු වෙන්න
ඔයාගේ PowerShell එකේ project එක කරන folder එකට ගිහින් මෙහෙම run කරන්න:
```powershell
# Clone the repository
git clone https://github.com/Imesh-Madushan-Dev/agent-kernel.git
cd agent-kernel

# Upstream link කරගන්න
git remote add upstream https://github.com/yaalalabs/agent-kernel.git

# අපේ branch එකට මාරු වෙන්න
git checkout feature/farmer-advisor
```

### Step 4: Project Dependencies install කරගන්න
අපේ project එක **self-contained** - ඒ නිසා `ak-py` එකට යන්න ඕන නෑ, කෙලින්ම අපේ folder එකට ගිහින්:
```powershell
cd use-cases\farmer-advisor

# Dependencies ඔක්කොම install වෙනවා (.venv එකත් auto හැදෙනවා)
uv sync
```

### Step 5: API Keys ටික දාගන්න (.env)
```powershell
# Template එක copy කරගන්න
copy .env.example .env
```
ඊට පස්සේ `.env` file එක open කරලා මේවා fill කරන්න:

| Key | කොහෙන්ද ගන්නේ | ඕනේම ද? |
| --- | --- | --- |
| `GOOGLE_API_KEY` | [Google AI Studio](https://aistudio.google.com/apikey) → Create API Key | ✅ ඕනේමයි |
| `AK_TELEGRAM__BOT_TOKEN` | Telegram [@BotFather](https://t.me/botfather) → `/newbot` | Telegram demo එකට විතරයි |
| `AK_WHATSAPP__*` | Meta Developer Portal (WhatsApp Cloud API) | WhatsApp demo එකට විතරයි |

> ⚠️ **`.env` file එක කවදාවත් git commit කරන්න එපා!** (ඒක `.gitignore` වෙලා තියෙනවා). Token එකක් accidentally leak වුනොත් වහාම revoke කරලා අලුත් එකක් ගන්න.

> 💡 Model එක: අලුත් free-tier API keys වලට `gemini-3.1-flash-lite` විතරයි වැඩ කරන්නේ (පරණ 2.0/2.5 models වලට quota නෑ). ඒක දැනටමත් code එකේ set කරලා තියෙනවා.

### Step 6: Run කරලා බලන්න
```powershell
# 1. Tests (LLM key ඕන නෑ - offline run වෙනවා)
uv run pytest

# 2. Terminal chat UI එක
uv run python main.py

# 3. Web UI + API server එක
uv run python main.py serve
# ↳ browser එකෙන් http://localhost:8000/ ට යන්න
```

Tests ටික pass වෙලා, terminal එකේ chat කරන්න පුළුවන් නම් වැඩේ ගොඩ! 🚀

### Step 7 (Optional): Telegram / WhatsApp හයි කරන්න
1. `uv run python main.py serve` දාලා තියෙද්දි වෙන PowerShell එකක [ngrok](https://ngrok.com/) run කරන්න: `ngrok http 8000`
2. **Telegram:** browser එකේ මේක open කරන්න (ඔයාගේ token + ngrok URL එක දාලා):
   `https://api.telegram.org/bot<TOKEN>/setWebhook?url=https://<ngrok-url>/telegram/webhook`
3. **WhatsApp:** Meta developer portal එකේ webhook URL එක `https://<ngrok-url>/whatsapp/webhook` ට set කරලා, `messages` field එකට subscribe වෙන්න.

---

### 💡 Quick Tips:
- වැඩ කරද්දි හැමතිස්සෙම `use-cases\farmer-advisor` folder එක ඇතුලෙ ඉන්න (`ak-py` නෙමෙයි!).
- `uv run ...` පාවිච්චි කරනවා නම් venv activate කරන්න ඕන නෑ - uv එකෙන් auto handle කරනවා.
- Code formatting: `uv run black .` සහ `uv run isort .`
- සිංහල terminal එකේ කැත වුනාට web UI එකේ (localhost:8000) ලස්සනට පේනවා - demo එකට ඒක පාවිච්චි කරන්න.
- Commits: conventional messages (`feat:`, `fix:`, `docs:`, `test:`) - branch: `feature/farmer-advisor`.
