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
# We default to running the analysis, but we need to mount volumes for it to work on host files
CMD ["python", "src/main.py"]
