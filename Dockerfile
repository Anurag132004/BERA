FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ src/
COPY tests/ tests/

# Set User to non-root for security (best practice)
RUN useradd -m appuser
USER appuser

# Entry point
# We default to running the analysis.
# USERS MUST MOUNT their extensions directory to /data/extensions for this to work.
# Example: -v /path/to/extensions:/data/extensions:ro

# We will pass arguments to the script via CMD
CMD ["python", "src/main.py", "--output", "/app/output/report.json"]
