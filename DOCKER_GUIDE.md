# How to Run BERA in Docker

BERA is containerized and ready to scan extensions on any machine. Because BERA runs inside a container, it cannot see your browser extensions unless you "mount" the folder where they live.

## 1. Prerequisites
- Docker installed
- A Groq or OpenAI API Key

## 2. Build the Image
```bash
docker build -t bera .
```

## 3. Run the Container
You need to map your local extension folder to `/data/extensions` inside the container.

### Windows (PowerShell)
**Chrome:**
```powershell
docker run --rm `
  -e GROQ_API_KEY="your_key_here" `
  -v "$env:LOCALAPPDATA/Google/Chrome/User Data/Default/Extensions:/data/extensions:ro" `
  -v "${PWD}/output:/app/output" `
  bera
```

**Edge:**
```powershell
docker run --rm `
  -e GROQ_API_KEY="your_key_here" `
  -v "$env:LOCALAPPDATA/Microsoft/Edge/User Data/Default/Extensions:/data/extensions:ro" `
  -v "${PWD}/output:/app/output" `
  bera
```

### macOS
**Chrome:**
```bash
docker run --rm \
  -e GROQ_API_KEY="your_key_here" \
  -v "$HOME/Library/Application Support/Google/Chrome/Default/Extensions:/data/extensions:ro" \
  -v "$(pwd)/output:/app/output" \
  bera
```

## 4. Get the Report
The container will run, scan the mounted folder, and save `report.json` to the `./output` directory on your host machine.
