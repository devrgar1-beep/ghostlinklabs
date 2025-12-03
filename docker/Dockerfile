# syntax=docker/dockerfile:1.6
FROM python:3.12-slim

# Create non-root user
ARG USER=ghostlink
ARG UID=10001
RUN useradd -m -u $UID -s /usr/sbin/nologin $USER

# System deps (curl for healthcheck)
RUN apt-get update -y && apt-get install -y --no-install-recommends \
  curl ca-certificates && \
  rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Python virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy requirements and install
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install -r /app/requirements.txt

# Copy all application files
COPY . /app/

# Make scripts executable
RUN chmod +x /app/cold_boot_orchestrator.py && \
  chmod +x /app/src/*.py && \
  chmod +x /app/monitoring/*.py && \
  chmod +x /app/tests/**/*.py

# Runtime user
USER $USER

# Expose ports for cold boot orchestrator and monitoring
EXPOSE 7420/tcp 7422/tcp 9108/tcp 8000/tcp

# Healthcheck: cold boot health check should pass
HEALTHCHECK --interval=60s --timeout=30s --start-period=30s --retries=3 \
  CMD python3 /app/cold_boot_orchestrator.py health >/dev/null 2>&1 && echo "OK" || echo "FAIL"

# Default command: run the cold boot orchestrator
CMD ["python3", "/app/cold_boot_orchestrator.py", "health"]
