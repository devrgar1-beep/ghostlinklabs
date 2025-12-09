#!/bin/bash
# Container integration for GhostLink

# Create Dockerfile
cat > Dockerfile.ghostlink << 'DOCKER_EOF'
FROM python:3.11-slim
RUN apt-get update && apt-get install -y curl
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8080
CMD ["python", "ghostlink_api_server.py"]
DOCKER_EOF

# Create docker-compose
cat > docker-compose.ghostlink.yml << 'COMPOSE_EOF'
version: '3.8'
services:
  ghostlink-api:
    build: .
    ports:
      - "8080:8080"
    restart: unless-stopped
COMPOSE_EOF

# Create container scripts
cat > build-container.sh << 'BUILD_EOF'
#!/bin/bash
docker build -f Dockerfile.ghostlink -t ghostlink-ai .
BUILD_EOF

cat > start-container.sh << 'START_EOF'
#!/bin/bash
docker run -d --name ghostlink-ai -p 8080:8080 ghostlink-ai
START_EOF

chmod +x build-container.sh start-container.sh

echo "✅ Container integration complete!"
