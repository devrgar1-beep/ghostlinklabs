FROM ubuntu:22.04

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    git \
    curl \
    wget \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Wolfram Engine (if available) or Mathematica
# Note: Wolfram Engine requires license, using free WolframScript for now
RUN wget -q https://account.wolfram.com/download/public/wolfram-engine/desktop/LINUX && \
    chmod +x LINUX && \
    ./LINUX --noexec --target wolfram-engine && \
    cd wolfram-engine && \
    ./install.sh --no-license --no-gui && \
    cd .. && rm -rf wolfram-engine LINUX

# Set up Python environment
WORKDIR /app
COPY requirements*.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Make scripts executable
RUN chmod +x *.py

# Expose ports
EXPOSE 8000 7420

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Default command
CMD ["python3", "core-runtime/main.py"]
