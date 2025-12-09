FROM python:3.9-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app
ENV GHOSTLINK_ENV=production

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd --create-home --shell /bin/bash ghostlink
RUN chown -R ghostlink:ghostlink /app
USER ghostlink

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:3000/health || exit 1

# Expose ports
EXPOSE 3000

# Start the application
CMD ["python3", "ghostlink_api_server_enhanced.py", "--port", "3000"]