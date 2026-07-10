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

### Step 4: Python Environment එක Setup කරගන්න
කෝඩ් run කරන්න කලින් dependencies ටික install කරගන්න ඕනේ:
```powershell
# ak-py folder එකට යන්න
cd ak-py

# Virtual Environment එකක් හදාගන්න
uv venv

# Virtual Environment එක activate කරන්න
.venv\Scripts\Activate.ps1

# Dependencies සහ Dev Tools ඔක්කොම install කරගන්න
uv sync --all-extras
uv pip install --group dev
```

### Step 5: Setup එක වැඩද කියලා check කරන්න
හැමදේම හරිද බලන්න tests run කරලා බලමු:
```powershell
uv run pytest
```
Tests ටික pass වෙනවා නම් වැඩේ ගොඩ! 🚀

---

### 💡 Quick Tips:
- වැඩ කරද්දි හැමතිස්සෙම `ak-py` folder එක ඇතුලෙ ඉන්න.
- Environment එක activate කරලා තියාගන්න (`.venv\Scripts\Activate.ps1`).
- Code වල formatting ප්‍රශ්න එනවා නම් `uv run black .` සහ `uv run isort .` run කරන්න.
