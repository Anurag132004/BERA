# How to Test BERA Agent

## Required APIs
You can use **OpenAI** OR **Groq** for the risk assessment.

**Option A: Groq (Free / Fast)**
Variable: `GROQ_API_KEY`
Model: `llama3-70b-8192`

**Option B: OpenAI**
Variable: `OPENAI_API_KEY`
Model: `gpt-4`

## Testing Locally (Windows / PowerShell)

### 1. Set the API Key
Set your Groq API key (provided by you):

```powershell
$env:GROQ_API_KEY = "gsk_YOUR_KEY_HERE"
```

### 2. Run the Agent
Run the main script from the project root. This will scan your **local Chrome and Edge extensions** automatically.

```powershell
python src/main.py --output my_report.json
```

### 3. Check the Result
Open `my_report.json` to see the findings.
```powershell
type my_report.json
```

## Troubleshooting
- **No extensions found?** 
  - The agent looks in standard Windows paths:
    - Chrome: `%LOCALAPPDATA%\Google\Chrome\User Data\Default\Extensions`
    - Edge: `%LOCALAPPDATA%\Microsoft\Edge\User Data\Default\Extensions`
  - If you use a custom profile, you might need to edit `src/discovery/chrome.py` temporarily.
