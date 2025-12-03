#!/bin/bash
# GhostLink Network Setup Script
# Run this when connected to your Eero 7 network at home

echo "🔗 Setting up GhostLink Sovereign Network..."
echo "=========================================="

# Check current network
echo "Current network configuration:"
ip route show
echo ""

# Test connectivity to Eero gateway
echo "Testing Eero connectivity..."
ping -c 3 192.168.1.1

# Update Docker network configuration for Eero
echo "Updating Docker network configuration..."
cat > docker-compose.network.yml << 'EOF'
version: '3.8'

# Network configuration for Eero 7 mesh
networks:
  ghostlink-network:
    driver: bridge
    ipam:
      config:
        - subnet: 192.168.1.0/24
          gateway: 192.168.1.1
    driver_opts:
      com.docker.network.bridge.name: ghostlink-br0

# Service IP assignments
services:
  ghostlink:
    networks:
      ghostlink-network:
        ipv4_address: 192.168.1.100

  redis:
    networks:
      ghostlink-network:
        ipv4_address: 192.168.1.101

  postgres:
    networks:
      ghostlink-network:
        ipv4_address: 192.168.1.102

  ollama:
    networks:
      ghostlink-network:
        ipv4_address: 192.168.1.103

  prometheus:
    networks:
      ghostlink-network:
        ipv4_address: 192.168.1.104

  grafana:
    networks:
      ghostlink-network:
        ipv4_address: 192.168.1.105
EOF

echo "✅ Network configuration created"
echo ""
echo "🚀 Next steps:"
echo "1. Connect all devices to Eero 7 WiFi"
echo "2. Set static IP for main server: 192.168.1.100"
echo "3. Run: docker-compose -f docker-compose.yml -f docker-compose.network.yml up -d"
echo "4. Access GhostLink at: http://192.168.1.100:8000"
echo "5. Access Grafana at: http://192.168.1.105:3000"
echo ""
echo "🔒 Security recommendations:"
echo "- Enable WPA3 on Eero"
echo "- Set up device access controls"
echo "- Configure port forwarding only for needed services"
echo "- Enable firewall rules for internal communication"