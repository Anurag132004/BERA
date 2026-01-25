# 🛡️ BERA - Browser Extension Risk Assessment Agent

[![CI/CD](https://github.com/Anurag132004/BERA/actions/workflows/ci.yml/badge.svg)](https://github.com/Anurag132004/BERA/actions)
[![Docker](https://img.shields.io/docker/pulls/docker0doc0anurag/bera)](https://hub.docker.com/r/docker0doc0anurag/bera)

**BERA** is a CLI-based security tool that automatically scans your browser extensions and tells you if any of them are risky. It uses AI to analyze permissions, embedded URLs, and other indicators to give you a risk score.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🔍 **Auto-Discovery** | Automatically finds all extensions installed in Chrome and Edge |
| 🧠 **AI-Powered Analysis** | Uses Groq's LLaMA 3.3 70B model to assess risk intelligently |
| 🌐 **URL/IP Extraction** | Scans extension code for suspicious network endpoints |
| 📊 **JSON Reports** | Generates detailed reports with risk scores for each extension |
| 🐳 **Docker Ready** | Run it anywhere without installing Python |
| 🔄 **Unique Run IDs** | Each scan gets a unique ID so you never overwrite old reports |

---

## 🚀 Quick Start (Docker - Recommended)

No Python installation needed! Just Docker.

### Step 1: Get a Free Groq API Key

1. Go to [https://console.groq.com](https://console.groq.com)
2. Sign up / Log in with Google or GitHub
3. Click **"API Keys"** in the sidebar
4. Click **"Create API Key"**
5. Copy the key (starts with `gsk_...`)

### Step 2: Find Your Browser Extensions Folder

**Chrome (Windows):**
```
C:\Users\<YourUsername>\AppData\Local\Google\Chrome\User Data\Default\Extensions
```

**Edge (Windows):**
```
C:\Users\<YourUsername>\AppData\Local\Microsoft\Edge\User Data\Default\Extensions
```

**Chrome (macOS):**
```
~/Library/Application Support/Google/Chrome/Default/Extensions
```

**Chrome (Linux):**
```
~/.config/google-chrome/Default/Extensions
```

> 💡 **Tip:** In Windows, type `%LOCALAPPDATA%` in File Explorer to quickly navigate to AppData\Local

### Step 3: Run the Scanner

**Windows (PowerShell):**
```powershell
docker run --rm `
  -e GROQ_API_KEY="gsk_YOUR_KEY_HERE" `
  -v "$env:LOCALAPPDATA\Google\Chrome\User Data\Default\Extensions:/data/extensions:ro" `
  -v "${PWD}:/app/output" `
  docker0doc0anurag/bera:latest
```

**macOS / Linux:**
```bash
docker run --rm \
  -e GROQ_API_KEY="gsk_YOUR_KEY_HERE" \
  -v "$HOME/Library/Application Support/Google/Chrome/Default/Extensions:/data/extensions:ro" \
  -v "$(pwd):/app/output" \
  docker0doc0anurag/bera:latest
```

### Step 4: Check Your Report

After the scan completes, you'll find a file like `report_a1b2c3d4.json` in your current directory!

---

## 📋 Command Breakdown

| Part | What it does |
|------|--------------|
| `docker run --rm` | Run container and delete it when done |
| `-e GROQ_API_KEY="..."` | Pass your API key to the container |
| `-v ".../Extensions:/data/extensions:ro"` | Mount your extensions folder (read-only) |
| `-v "${PWD}:/app/output"` | Mount current directory for the output report |
| `docker0doc0anurag/bera:latest` | The Docker image to run |

---

## 📊 Sample Output

```json
{
  "run_id": "a1b2c3d4",
  "timestamp": "2026-01-26T00:10:00",
  "total": 5,
  "extensions": [
    {
      "id": "eimadpbcbfnmbkopoojfekhnkhdbieeh",
      "name": "Dark Reader",
      "version": "4.9.118",
      "permissions": ["tabs", "storage"],
      "risk_score": "Low",
      "risk_summary": "Risk: Low\nReason: Well-known extension with minimal permissions..."
    }
  ]
}
```

---

## 🖥️ Run Locally (Without Docker)

If you prefer running directly with Python:

### Prerequisites
- Python 3.11+
- pip

### Installation
```bash
git clone https://github.com/Anurag132004/BERA.git
cd BERA
pip install -r requirements.txt
```

### Usage
**Windows:**
```powershell
$env:GROQ_API_KEY = "gsk_YOUR_KEY_HERE"
python src/main.py --output report.json
```

**macOS / Linux:**
```bash
export GROQ_API_KEY="gsk_YOUR_KEY_HERE"
python src/main.py --output report.json
```

---

## 🔑 Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `GROQ_API_KEY` | Yes* | Your Groq API key for AI analysis |
| `OPENAI_API_KEY` | No | Alternative: Use OpenAI instead of Groq |

*If neither key is provided, the tool will still scan but skip AI analysis.

---

## 🏗️ Project Structure

```
BERA/
├── src/
│   ├── main.py              # Entry point
│   ├── models.py            # Data structures
│   ├── discovery/           # Finds extensions on disk
│   ├── enrichment/          # Gets extra info from web stores
│   ├── threat_intel/        # Scans for suspicious URLs/IPs
│   └── llm/                  # AI risk assessment
├── tests/                    # Unit tests
├── Dockerfile               # Container definition
└── requirements.txt         # Python dependencies
```

---

## 🤝 Contributing

Feel free to open issues or submit PRs! This is my first security tool project and I'm learning as I go.

---

## 📜 License

MIT License - feel free to use this however you want!

---

## 🙋 FAQ

**Q: Is this safe to run on my computer?**  
A: Yes! BERA only reads extension files - it doesn't modify anything. The Docker container runs as a non-root user for extra safety.

**Q: Does it send my extension data anywhere?**  
A: Only to Groq/OpenAI for AI analysis. Your actual extension files stay on your machine.

**Q: Why Groq instead of OpenAI?**  
A: Groq has a generous free tier so you can use this tool without paying anything!

**Q: Can I scan Firefox extensions?**  
A: Not yet, but it's on my TODO list!

---

Made with ❤️ by [Anurag](https://github.com/Anurag132004)
