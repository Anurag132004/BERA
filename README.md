# BERA: Browser Extension Risk Assessment Agent

BERA is a containerized security agent that autonomously discovers, extracts, and assesses the risk of browser extensions installed on a host system.

## Features
- **Discovery**: Automatically finds extensions for Chrome, Edge, and Firefox (Module A).
- **Metadata Enrichment**: Fetches extension age and developer information (Module B).
- **Threat Intel**: Static scanning for embedded URLs and IPs (Module C).
- **AI Assessment**: Uses LLM (OpenAI) to generate a risk score and summary (Module D).
- **Containerized**: Runs in Docker with volume mounts.

## Setup

### Prerequisites
- Python 3.11+ (for local run)
- Docker
- OpenAI API Key (optional, for risk scoring)

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Anurag132004/BERA.git
   cd BERA
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Usage (Local)
To run the agent locally (scanning your own profile):
```bash
export OPENAI_API_KEY="sk-..."
python src/main.py --output report.json
```

### Usage (Docker)
To scan the host's Chrome extensions from Docker, you must mount the extension directory.

**Windows Example (Powershell):**
```powershell
docker build -t bera .
docker run --rm -e OPENAI_API_KEY="sk-..." `
  -v "$env:LOCALAPPDATA/Google/Chrome/User Data/Default/Extensions:/data/extensions:ro" `
  bera python src/main.py --output /app/report.json
```
*Note: You might need to adjust the discovery logic or mount point if running inside Docker, as the agent looks for standard Windows paths by default. In a production containerized agent, you'd map the volume to a known path and tell the agent to scan that specific path.*

## Architecture
- `src/discovery`: Logic to find extensions.
- `src/enrichment`: Scrapers/APIs for metadata.
- `src/threat_intel`: Static analysis.
- `src/llm`: AI Risk Assessment.
