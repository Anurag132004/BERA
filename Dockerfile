# I'm using Python 3.11 slim image because it's lightweight
FROM python:3.11-slim

# This is where my app lives inside the container
WORKDIR /app

# First I copy and install dependencies so Docker can cache this layer
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Now I copy my actual code
COPY src/ src/
COPY tests/ tests/

# Creating a non-root user because I read it's safer this way
RUN useradd -m appuser
USER appuser

# When someone runs this container, it will automatically start my scanner
# They need to mount their browser extensions folder to /data/extensions
# Like this: docker run -v "path/to/extensions:/data/extensions:ro" bera
CMD ["python", "src/main.py", "--output", "/app/output/report.json"]
