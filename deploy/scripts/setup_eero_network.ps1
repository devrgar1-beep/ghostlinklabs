# GhostLink Eero 7 Network Setup
# PowerShell script for Windows network configuration

Write-Host "🔗 Setting up GhostLink Sovereign Network..." -ForegroundColor Cyan
Write-Host "=" * 50 -ForegroundColor Yellow

# Check current network
Write-Host "Current network configuration:" -ForegroundColor Green
Get-NetIPConfiguration | Select-Object InterfaceAlias, IPv4Address, IPv4DefaultGateway
Write-Host ""

# Test Eero connectivity
Write-Host "Testing Eero connectivity..." -ForegroundColor Green
Test-Connection -ComputerName 192.168.1.1 -Count 3 -Quiet
if ($?) {
    Write-Host "✅ Eero gateway reachable" -ForegroundColor Green
} else {
    Write-Host "❌ Cannot reach Eero gateway" -ForegroundColor Red
}
Write-Host ""

# Create Docker network configuration
Write-Host "Creating Docker network configuration..." -ForegroundColor Green

$networkConfig = @"
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

# Service IP assignments for Eero network
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
"@

$networkConfig | Out-File -FilePath "docker-compose.eero.yml" -Encoding UTF8

Write-Host "✅ Network configuration created: docker-compose.eero.yml" -ForegroundColor Green
Write-Host ""

# Eero setup instructions
Write-Host "🚀 Eero 7 Setup Instructions:" -ForegroundColor Cyan
Write-Host "1. Connect to Eero 7 WiFi network" -ForegroundColor White
Write-Host "2. Open Eero app and go to Settings > Network Settings" -ForegroundColor White
Write-Host "3. Set up static IP reservations:" -ForegroundColor White
Write-Host "   - GhostLink Server: 192.168.1.100" -ForegroundColor Yellow
Write-Host "   - AI Workstation: 192.168.1.101" -ForegroundColor Yellow
Write-Host "4. Enable port forwarding:" -ForegroundColor White
Write-Host "   - 8000 (GhostLink API)" -ForegroundColor Yellow
Write-Host "   - 3000 (Grafana)" -ForegroundColor Yellow
Write-Host "   - 9090 (Prometheus)" -ForegroundColor Yellow
Write-Host ""

Write-Host "🔧 Deployment Commands:" -ForegroundColor Cyan
Write-Host "docker-compose -f docker-compose.yml -f docker-compose.eero.yml up -d" -ForegroundColor Yellow
Write-Host ""

Write-Host "🌐 Access URLs:" -ForegroundColor Cyan
Write-Host "GhostLink API:    http://192.168.1.100:8000" -ForegroundColor Yellow
Write-Host "Grafana:          http://192.168.1.105:3000" -ForegroundColor Yellow
Write-Host "Prometheus:       http://192.168.1.104:9090" -ForegroundColor Yellow
Write-Host ""

Write-Host "🔒 Security Setup:" -ForegroundColor Cyan
Write-Host "- Enable WPA3 encryption" -ForegroundColor White
Write-Host "- Set up device access controls" -ForegroundColor White
Write-Host "- Create separate guest network" -ForegroundColor White
Write-Host "- Enable firewall rules" -ForegroundColor White
Write-Host "- Set up QoS for AI traffic" -ForegroundColor White

Write-Host ""
Write-Host "🎯 Sovereign AI Network Ready!" -ForegroundColor Green
Write-Host "Your Eero 7 will now serve as the backbone of your independent AI infrastructure." -ForegroundColor Cyan