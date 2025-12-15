FROM python:3.11-slim

WORKDIR /app

# Install system packages
RUN apt-get update && apt-get install -y curl build-essential && rm -rf /var/lib/apt/lists/*

# Copy only what we need from repository root
COPY src /app/src
COPY requirements/api.txt /app/requirements-api.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r /app/requirements-api.txt

ENV PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["uvicorn", "src.api.server:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
