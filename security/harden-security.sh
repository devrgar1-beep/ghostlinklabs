#!/bin/bash

# GhostLink Security Hardening Script
# Applies security hardening measures to production deployment

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root (for some operations)
check_privileges() {
    if [[ $EUID -eq 0 ]]; then
        print_warning "Running as root - some operations may be limited in containers"
    fi
}

# Generate strong passwords
generate_password() {
    openssl rand -base64 32 | tr -d "=+/" | cut -c1-24
}

# Secure environment file
secure_env_file() {
    print_status "Securing environment configuration..."

    if [ ! -f .env ]; then
        print_error ".env file not found. Please create it from .env.example"
        return 1
    fi

    # Set restrictive permissions
    chmod 600 .env

    # Check for default/weak passwords
    if grep -q "your-secret-key-here\|your-jwt-secret-here\|ghostlink2025" .env; then
        print_warning "⚠️  .env contains default values. Please update with strong secrets:"
        echo "   - SECRET_KEY"
        echo "   - JWT_SECRET"
        echo "   - GRAFANA_PASSWORD"
        echo ""
        echo "   Consider using: $(generate_password)"
    fi

    print_success "Environment file secured"
}

# Generate SSL certificates
generate_ssl_certs() {
    print_status "Generating SSL certificates..."

    if [ ! -f "./security/generate-ssl-certs.sh" ]; then
        print_error "SSL certificate generation script not found"
        return 1
    fi

    ./security/generate-ssl-certs.sh

    print_success "SSL certificates generated"
}

# Update Nginx configuration for HTTPS
update_nginx_ssl() {
    print_status "Updating Nginx configuration for SSL/TLS..."

    if [ ! -f "./nginx/ssl/ghostlink.crt" ] || [ ! -f "./nginx/ssl/ghostlink.key" ]; then
        print_warning "SSL certificates not found. Run SSL generation first."
        return 1
    fi

    # Create SSL-enabled nginx configuration
    cat > "./nginx/nginx-ssl.conf" << 'EOF'
events {
    worker_connections 1024;
}

http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;

    # SSL/TLS Configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES128-SHA256:ECDHE-RSA-AES256-SHA384;
    ssl_prefer_server_ciphers off;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;

    # HSTS (HTTP Strict Transport Security)
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

    # Logging
    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for"';

    access_log /var/log/nginx/access.log main;
    error_log /var/log/nginx/error.log;

    # Performance
    sendfile        on;
    tcp_nopush      on;
    tcp_nodelay     on;
    keepalive_timeout 65;
    types_hash_max_size 2048;
    client_max_body_size 100M;

    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_types
        text/plain
        text/css
        text/xml
        text/javascript
        application/json
        application/javascript
        application/xml+rss
        application/atom+xml
        image/svg+xml;

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
    limit_req_zone $binary_remote_addr zone=static:10m rate=100r/s;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;

    upstream ghostlink_api {
        server ghostlink-api-prod:3000;
    }

    upstream grafana {
        server grafana:3000;
    }

    # HTTP to HTTPS redirect
    server {
        listen 80;
        server_name localhost;
        return 301 https://$server_name$request_uri;
    }

    # HTTPS server
    server {
        listen 443 ssl http2;
        server_name localhost;

        # SSL certificate configuration
        ssl_certificate /etc/nginx/ssl/chain.pem;
        ssl_certificate_key /etc/nginx/ssl/ghostlink.key;
        ssl_dhparam /etc/nginx/ssl/dhparam.pem;

        # OCSP stapling
        ssl_stapling on;
        ssl_stapling_verify on;
        resolver 8.8.8.8 8.8.4.4 valid=300s;
        resolver_timeout 5s;

        # GhostLink API
        location /api/ {
            limit_req zone=api burst=20 nodelay;
            proxy_pass http://ghostlink_api/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_set_header X-Forwarded-Port $server_port;
        }

        # GhostLink Web Interface
        location / {
            limit_req zone=static burst=100 nodelay;
            proxy_pass http://ghostlink_api/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_set_header X-Forwarded-Port $server_port;
        }

        # Grafana Monitoring (HTTPS)
        location /monitoring/ {
            proxy_pass http://grafana/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_set_header X-Forwarded-Port $server_port;
            rewrite ^/monitoring/(.*) /$1 break;
        }

        # Static files caching
        location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
            expires 1y;
            add_header Cache-Control "public, immutable";
        }

        # Health check endpoint
        location /health {
            access_log off;
            return 200 "healthy\n";
            add_header Content-Type text/plain;
        }
    }
}
EOF

    print_success "SSL-enabled Nginx configuration created"
}

# Create security monitoring configuration
create_security_monitoring() {
    print_status "Creating security monitoring configuration..."

    # Create Prometheus alerting rules for security
    cat > "./monitoring/security-alerts.yml" << 'EOF'
groups:
  - name: security_alerts
    rules:
      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) / rate(http_requests_total[5m]) > 0.1
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High error rate detected"
          description: "Error rate is {{ $value }}% over the last 5 minutes"

      - alert: UnusualTrafficPattern
        expr: rate(http_requests_total[5m]) > 1000
        for: 2m
        labels:
          severity: warning
        annotations:
          summary: "Unusual traffic pattern detected"
          description: "Request rate is {{ $value }} req/s"

      - alert: SSLHandshakeFailures
        expr: rate(nginx_ssl_handshake_failures_total[5m]) > 0
        for: 1m
        labels:
          severity: warning
        annotations:
          summary: "SSL handshake failures detected"
          description: "SSL handshake failures: {{ $value }}"

      - alert: ContainerRestart
        expr: rate(container_restart_total[5m]) > 0
        for: 1m
        labels:
          severity: info
        annotations:
          summary: "Container restart detected"
          description: "Container {{ $labels.container }} restarted"
EOF

    print_success "Security monitoring configuration created"
}

# Create fail2ban-like configuration for Docker
create_intrusion_detection() {
    print_status "Creating intrusion detection configuration..."

    # Create a script to monitor and block suspicious IPs
    cat > "./security/monitor-threats.sh" << 'EOF'
#!/bin/bash

# GhostLink Threat Monitoring Script
# Monitors logs for suspicious activity and blocks IPs

LOG_FILE="./logs/access.log"
BLOCKLIST="./security/blocklist.txt"
WHITELIST="./security/whitelist.txt"

# Create files if they don't exist
touch "$BLOCKLIST" "$WHITELIST"

# Function to check if IP is whitelisted
is_whitelisted() {
    local ip=$1
    grep -q "^$ip$" "$WHITELIST"
}

# Function to block IP (log for now, implement blocking in production)
block_ip() {
    local ip=$1
    local reason=$2

    if ! is_whitelisted "$ip"; then
        echo "$(date): Blocking $ip - $reason" >> "./logs/security.log"
        echo "$ip" >> "$BLOCKLIST"
        # In production, implement actual blocking:
        # iptables -A INPUT -s $ip -j DROP
        # docker exec nginx iptables -A INPUT -s $ip -j DROP
    fi
}

# Monitor for suspicious patterns
monitor_logs() {
    if [ ! -f "$LOG_FILE" ]; then
        echo "Log file not found: $LOG_FILE"
        return
    fi

    # Check for brute force attempts (multiple 401s from same IP)
    awk '$9 == 401 {print $1}' "$LOG_FILE" | sort | uniq -c | while read count ip; do
        if [ "$count" -gt 5 ]; then
            block_ip "$ip" "Brute force attempt ($count failed auths)"
        fi
    done

    # Check for SQL injection attempts
    grep -i "union\|select\|insert\|drop\|update\|script" "$LOG_FILE" | awk '{print $1}' | sort | uniq | while read ip; do
        block_ip "$ip" "Potential SQL injection attempt"
    done

    # Check for XSS attempts
    grep -i "<script\|javascript:\|onload\|onerror" "$LOG_FILE" | awk '{print $1}' | sort | uniq | while read ip; do
        block_ip "$ip" "Potential XSS attempt"
    done

    # Check for directory traversal
    grep -i "\.\./\|\.\.\\\|etc/passwd\|/etc/shadow" "$LOG_FILE" | awk '{print $1}' | sort | uniq | while read ip; do
        block_ip "$ip" "Directory traversal attempt"
    done
}

# Clean old entries from blocklist (older than 24 hours)
clean_blocklist() {
    if [ -f "./logs/security.log" ]; then
        # Remove entries older than 24 hours
        awk -v cutoff="$(date -d '24 hours ago' +%s)" '
        {
            # Extract timestamp from log line
            split($0, parts, ": ")
            date_str = parts[1]
            if (date_str ~ /^[0-9]{4}-[0-9]{2}-[0-9]{2}/) {
                cmd = "date -d \"" date_str "\" +%s"
                cmd | getline timestamp
                close(cmd)
                if (timestamp > cutoff) print
            }
        }' "./logs/security.log" > "./logs/security.log.tmp" && mv "./logs/security.log.tmp" "./logs/security.log"
    fi
}

# Main monitoring function
main() {
    mkdir -p "./logs" "./security"

    while true; do
        monitor_logs
        clean_blocklist
        sleep 300  # Check every 5 minutes
    done
}

# Run main function if script is called directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
EOF

    chmod +x "./security/monitor-threats.sh"

    print_success "Intrusion detection configuration created"
}

# Create backup encryption
create_backup_encryption() {
    print_status "Setting up backup encryption..."

    cat > "./security/encrypt-backup.sh" << 'EOF'
#!/bin/bash

# Backup Encryption Script
# Encrypts backups using AES-256

set -e

BACKUP_FILE=$1
ENCRYPTED_FILE="${BACKUP_FILE}.enc"

if [ -z "$BACKUP_FILE" ]; then
    echo "Usage: $0 <backup-file>"
    exit 1
fi

if [ ! -f "$BACKUP_FILE" ]; then
    echo "Backup file not found: $BACKUP_FILE"
    exit 1
fi

# Generate encryption key if it doesn't exist
KEY_FILE="./security/backup.key"
if [ ! -f "$KEY_FILE" ]; then
    openssl rand -hex 32 > "$KEY_FILE"
    chmod 600 "$KEY_FILE"
    echo "Generated new encryption key: $KEY_FILE"
fi

# Encrypt the backup
openssl enc -aes-256-cbc -salt -in "$BACKUP_FILE" -out "$ENCRYPTED_FILE" -kfile "$KEY_FILE"

# Verify encryption
if openssl enc -aes-256-cbc -d -in "$ENCRYPTED_FILE" -out /dev/null -kfile "$KEY_FILE" 2>/dev/null; then
    echo "Backup encrypted successfully: $ENCRYPTED_FILE"

    # Remove unencrypted backup
    rm "$BACKUP_FILE"
    echo "Original backup file removed for security"
else
    echo "Encryption verification failed!"
    rm "$ENCRYPTED_FILE"
    exit 1
fi
EOF

    chmod +x "./security/encrypt-backup.sh"

    print_success "Backup encryption setup created"
}

# Update backup script to use encryption
update_backup_script() {
    print_status "Updating backup script for encryption..."

    # Add encryption to the backup script
    sed -i.bak '/compress_backup()/a\
    encrypt_backup' "./backup-production.sh"

    cat >> "./backup-production.sh" << 'EOF'

# Encrypt backup
encrypt_backup() {
    print_status "Encrypting backup..."

    if [ -f "./security/encrypt-backup.sh" ]; then
        ./security/encrypt-backup.sh "$FULL_BACKUP_PATH.tar.gz"
        print_success "Backup encrypted"
    else
        print_warning "Encryption script not found, skipping encryption"
    fi
}
EOF

    print_success "Backup script updated with encryption"
}

# Create security audit script
create_security_audit() {
    print_status "Creating security audit script..."

    cat > "./security/security-audit.sh" << 'EOF'
#!/bin/bash

# GhostLink Security Audit Script
# Performs comprehensive security checks

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_header() {
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}"
}

check_ssl_certificates() {
    print_header "SSL Certificate Check"

    if [ -f "./nginx/ssl/ghostlink.crt" ]; then
        echo -e "${GREEN}✓${NC} SSL certificate found"

        # Check expiration
        if openssl x509 -checkend 86400 -noout -in "./nginx/ssl/ghostlink.crt" 2>/dev/null; then
            echo -e "${GREEN}✓${NC} Certificate is valid (not expiring within 24 hours)"
        else
            echo -e "${RED}✗${NC} Certificate is expiring within 24 hours or already expired"
        fi

        # Check if self-signed
        if openssl x509 -in "./nginx/ssl/ghostlink.crt" -text -noout | grep -q "Issuer.*CN.*ghostlink"; then
            echo -e "${YELLOW}⚠${NC} Self-signed certificate detected (consider using CA-signed certificate)"
        else
            echo -e "${GREEN}✓${NC} CA-signed certificate detected"
        fi
    else
        echo -e "${RED}✗${NC} SSL certificate not found"
    fi
}

check_file_permissions() {
    print_header "File Permissions Check"

    # Check .env file
    if [ -f ".env" ]; then
        perms=$(stat -c "%a" .env 2>/dev/null || stat -f "%A" .env 2>/dev/null)
        if [ "$perms" = "600" ]; then
            echo -e "${GREEN}✓${NC} .env file has secure permissions (600)"
        else
            echo -e "${RED}✗${NC} .env file has insecure permissions: $perms (should be 600)"
        fi
    fi

    # Check SSL private key
    if [ -f "./nginx/ssl/ghostlink.key" ]; then
        perms=$(stat -c "%a" ./nginx/ssl/ghostlink.key 2>/dev/null || stat -f "%A" ./nginx/ssl/ghostlink.key 2>/dev/null)
        if [ "$perms" = "600" ]; then
            echo -e "${GREEN}✓${NC} SSL private key has secure permissions (600)"
        else
            echo -e "${RED}✗${NC} SSL private key has insecure permissions: $perms (should be 600)"
        fi
    fi
}

check_environment_security() {
    print_header "Environment Security Check"

    if [ -f ".env" ]; then
        # Check for default passwords
        if grep -q "your-secret-key-here\|your-jwt-secret-here\|ghostlink2025" .env; then
            echo -e "${RED}✗${NC} .env contains default or placeholder values"
        else
            echo -e "${GREEN}✓${NC} .env does not contain obvious default values"
        fi

        # Check for exposed secrets
        if grep -q "password\|secret\|key" .env | grep -v "GRAFANA_PASSWORD\|SECRET_KEY\|JWT_SECRET"; then
            echo -e "${YELLOW}⚠${NC} Potential exposed secrets found in .env"
        fi
    else
        echo -e "${RED}✗${NC} .env file not found"
    fi
}

check_container_security() {
    print_header "Container Security Check"

    # Check if services are running as non-root
    if command -v docker &> /dev/null; then
        containers=$(docker ps --format "table {{.Names}}" | grep ghostlink)
        if [ -n "$containers" ]; then
            echo -e "${GREEN}✓${NC} GhostLink containers are running"

            # Check user for each container
            for container in $containers; do
                user=$(docker exec "$container" whoami 2>/dev/null || echo "unknown")
                if [ "$user" != "root" ]; then
                    echo -e "${GREEN}✓${NC} $container runs as non-root user: $user"
                else
                    echo -e "${RED}✗${NC} $container runs as root user"
                fi
            done
        else
            echo -e "${YELLOW}⚠${NC} No GhostLink containers currently running"
        fi
    else
        echo -e "${YELLOW}⚠${NC} Docker not available for container checks"
    fi
}

check_network_security() {
    print_header "Network Security Check"

    # Check if HTTPS is configured
    if curl -s -I https://localhost 2>/dev/null | grep -q "HTTP/2 200\|HTTP/1.1 200"; then
        echo -e "${GREEN}✓${NC} HTTPS is accessible"
    else
        echo -e "${YELLOW}⚠${NC} HTTPS not accessible (may not be running or configured)"
    fi

    # Check security headers
    headers=$(curl -s -I https://localhost 2>/dev/null || curl -s -I http://localhost 2>/dev/null)
    if echo "$headers" | grep -q "Strict-Transport-Security"; then
        echo -e "${GREEN}✓${NC} HSTS header present"
    else
        echo -e "${YELLOW}⚠${NC} HSTS header not found"
    fi

    if echo "$headers" | grep -q "X-Frame-Options"; then
        echo -e "${GREEN}✓${NC} X-Frame-Options header present"
    else
        echo -e "${YELLOW}⚠${NC} X-Frame-Options header not found"
    fi
}

generate_report() {
    print_header "Security Audit Report"
    echo "Audit completed on: $(date)"
    echo "System: $(uname -a)"
    echo ""
    echo "Summary of checks performed:"
    echo "- SSL certificate validation"
    echo "- File permissions security"
    echo "- Environment variable security"
    echo "- Container security configuration"
    echo "- Network security headers"
    echo ""
    echo "Recommendations:"
    echo "1. Use CA-signed certificates for production"
    echo "2. Regularly rotate encryption keys and passwords"
    echo "3. Monitor logs for suspicious activity"
    echo "4. Keep dependencies and base images updated"
    echo "5. Implement regular security audits"
}

main() {
    echo "🔒 GhostLink Security Audit"
    echo "=========================="

    check_ssl_certificates
    echo ""
    check_file_permissions
    echo ""
    check_environment_security
    echo ""
    check_container_security
    echo ""
    check_network_security
    echo ""
    generate_report
}

main "$@"
EOF

    chmod +x "./security/security-audit.sh"

    print_success "Security audit script created"
}

# Main security hardening function
main() {
    echo "🔒 GhostLink Security Hardening"
    echo "==============================="

    check_privileges

    secure_env_file
    generate_ssl_certs
    update_nginx_ssl
    create_security_monitoring
    create_intrusion_detection
    create_backup_encryption
    update_backup_script
    create_security_audit

    print_success "🎉 Security hardening completed!"
    print_status "📋 Next steps:"
    echo "   1. Review and update .env with strong secrets"
    echo "   2. Run security audit: ./security/security-audit.sh"
    echo "   3. Start threat monitoring: ./security/monitor-threats.sh"
    echo "   4. Deploy with SSL: update docker-compose.yml to use nginx-ssl.conf"
}

# Run main function
main "$@"
EOF

    chmod +x "./security/harden-security.sh"

    print_success "Security hardening script created"
}

# Main security hardening function
main() {
    echo "🔒 GhostLink Security Hardening"
    echo "==============================="

    check_privileges

    secure_env_file
    generate_ssl_certs
    update_nginx_ssl
    create_security_monitoring
    create_intrusion_detection
    create_backup_encryption
    update_backup_script
    create_security_audit

    print_success "🎉 Security hardening completed!"
    print_status "📋 Next steps:"
    echo "   1. Review and update .env with strong secrets"
    echo "   2. Run security audit: ./security/security-audit.sh"
    echo "   3. Start threat monitoring: ./security/monitor-threats.sh"
    echo "   4. Deploy with SSL: update docker-compose.yml to use nginx-ssl.conf"
}

# Run main function
main "$@"