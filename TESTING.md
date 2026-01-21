# How to Test BERA Agent

## Required APIs
Currently, the **only** API key required is for **OpenAI** (ChatGPT). This is used by Module D to generate the risk score and summary.

**Variable Name:** `OPENAI_API_KEY`

If you do not provide this key, the agent will still run Discovery, Enrichment, and Static Scanning, but the Risk Score will be `UNKNOWN`.

## Testing Locally (Windows / PowerShell)

### 1. Set the API Key
You need to set the environment variable in your terminal session.
Replace `sk-...` with your actual OpenAI API Key.

```powershell
$env:OPENAI_API_KEY = "sk-placeholder-key-replace-me"
```

### 2. Run the Agent
Run the main script from the project root:

```powershell
python src/main.py --output my_report.json
```

### 3. Check the Result
Open `my_report.json` to see the findings.
```powershell
type my_report.json
```

## Running Tests
To verify the internal logic (Module A & C) matches expectations without running the full agent:
```powershell
python -m pytest
```

## Troubleshooting
- **No extensions found?** 
  - Ensure you have Chrome or Edge installed in the default location.
  - The agent looks in `%LOCALAPPDATA%\Google\Chrome\User Data\Default\Extensions`
- **OpenAI Error?**
  - Check your quota or if the key is valid.
  - Ensure `pip install openai` was successful.
