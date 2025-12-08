#!/bin/bash

# GhostLink Firewall Configuration Script
# Sets up firewall rules for production deployment

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

# Check if running on supported system
check_system() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        if command -v ufw &> /dev/null; then
            FIREWALL_CMD="ufw"
        elif command -v firewall-cmd &> /dev/null; then
            FIREWALL_CMD="firewalld"
        elif command -v iptables &> /dev/null; then
            FIREWALL_CMD="iptables"
        else
            print_error "No supported firewall found (ufw, firewalld, or iptables)"
            exit 1
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS doesn't have built-in firewall management in the same way
        print_warning "macOS detected - firewall rules will be informational only"
        FIREWALL_CMD="macos"
    else
        print_error "Unsupported operating system: $OSTYPE"
        exit 1
    fi

    print_success "Detected firewall system: $FIREWALL_CMD"
}

# Setup UFW rules
setup_ufw() {
    print_status "Configuring UFW firewall rules..."

    # Enable UFW if not already enabled
    sudo ufw --force enable

    # Default policies
    sudo ufw default deny incoming
    sudo ufw default allow outgoing

    # Allow SSH (if needed for management)
    sudo ufw allow ssh

    # Allow HTTP and HTTPS
    sudo ufw allow 80/tcp
    sudo ufw allow 443/tcp

    # Allow GhostLink specific ports (if exposing directly)
    # sudo ufw allow 3000/tcp  # API Server
    # sudo ufw allow 9090/tcp  # Prometheus
    # sudo ufw allow 3001/tcp  # Grafana

    # Rate limiting for SSH
    sudo ufw limit ssh

    print_success "UFW rules configured"
}

# Setup firewalld rules
setup_firewalld() {
    print_status "Configuring firewalld rules..."

    # Add services
    sudo firewall-cmd --permanent --add-service=http
    sudo firewall-cmd --permanent --add-service=https

    # Add custom ports if needed
    # sudo firewall-cmd --permanent --add-port=3000/tcp
    # sudo firewall-cmd --permanent --add-port=9090/tcp
    # sudo firewall-cmd --permanent --add-port=3001/tcp

    # Reload firewall
    sudo firewall-cmd --reload

    print_success "firewalld rules configured"
}

# Setup iptables rules
setup_iptables() {
    print_status "Configuring iptables rules..."

    # Create backup of current rules
    sudo iptables-save > iptables.backup.$(date +%Y%m%d_%H%M%S)

    # Flush existing rules
    sudo iptables -F
    sudo iptables -X

    # Default policies
    sudo iptables -P INPUT DROP
    sudo iptables -P FORWARD DROP
    sudo iptables -P OUTPUT ACCEPT

    # Allow loopback
    sudo iptables -A INPUT -i lo -j ACCEPT
    sudo iptables -A OUTPUT -o lo -j ACCEPT

    # Allow established connections
    sudo iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT

    # Allow SSH with rate limiting
    sudo iptables -A INPUT -p tcp --dport 22 -m conntrack --ctstate NEW -m limit --limit 3/min --limit-burst 3 -j ACCEPT
    sudo iptables -A INPUT -p tcp --dport 22 -j DROP

    # Allow HTTP and HTTPS
    sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT
    sudo iptables -A INPUT -p tcp --dport 443 -j ACCEPT

    # Allow GhostLink ports (if exposing directly)
    # sudo iptables -A INPUT -p tcp --dport 3000 -j ACCEPT  # API Server
    # sudo iptables -A INPUT -p tcp --dport 9090 -j ACCEPT  # Prometheus
    # sudo iptables -A INPUT -p tcp --dport 3001 -j ACCEPT  # Grafana

    # Allow ICMP (ping)
    sudo iptables -A INPUT -p icmp --icmp-type echo-request -j ACCEPT

    # Log dropped packets (optional)
    sudo iptables -A INPUT -j LOG --log-prefix "IPTABLES-DROP: " --log-level 4

    # Save rules
    if command -v netfilter-persistent &> /dev/null; then
        sudo netfilter-persistent save
    elif command -v iptables-save &> /dev/null; then
        sudo iptables-save | sudo tee /etc/iptables/rules.v4 > /dev/null
    fi

    print_success "iptables rules configured"
}

# Setup macOS informational rules
setup_macos() {
    print_status "macOS detected - providing informational firewall rules..."

    cat << 'EOF'
macOS Firewall Configuration (Manual Setup Required):

1. Open System Preferences > Security & Privacy > Firewall
2. Enable Firewall
3. Configure Application Firewall:
   - Allow incoming connections for Docker Desktop
   - Block all other incoming connections

3. For advanced configuration, use pfctl or install third-party firewall

Recommended macOS Security Settings:
- Enable FileVault for disk encryption
- Enable Firewall with stealth mode
- Disable remote login (SSH) unless needed
- Enable Gatekeeper and XProtect
- Keep macOS and applications updated

Docker Desktop on macOS handles container networking internally.
External access is controlled through Docker port mappings.

EOF

    print_warning "Manual firewall configuration required on macOS"
}

# Create Docker network security
setup_docker_network() {
    print_status "Configuring Docker network security..."

    # Create isolated network if it doesn't exist
    if ! docker network ls --format "{{.Name}}" | grep -q "^ghostlink-secure$"; then
        docker network create --driver bridge --internal ghostlink-secure 2>/dev/null || true
        print_success "Isolated Docker network created"
    else
        print_success "Isolated Docker network already exists"
    fi

    # Note: In production docker-compose.yml, services should use this network
    print_status "Update docker-compose.yml to use 'ghostlink-secure' network for internal services"
}

# Create security policy documentation
create_security_policy() {
    print_status "Creating security policy documentation..."

    cat > "./security/SECURITY_POLICY.md" << 'EOF'
# GhostLink Security Policy

## Overview
This document outlines the security measures and policies for the GhostLink production deployment.

## Network Security

### Firewall Rules
- **Default Policy**: Deny all incoming traffic
- **Allowed Ports**:
  - 80/tcp (HTTP) - Redirect to HTTPS
  - 443/tcp (HTTPS) - Main application access
  - 22/tcp (SSH) - Administrative access (rate limited)

### Docker Networking
- **Internal Network**: `ghostlink-secure` - Isolated bridge network
- **External Access**: Only through Nginx reverse proxy
- **No Direct Port Exposure**: Internal services not exposed externally

## SSL/TLS Configuration

### Certificate Requirements
- **Algorithm**: RSA 2048-bit or ECDSA P-256
- **Key Exchange**: ECDHE with forward secrecy
- **Cipher Suites**: TLS 1.2/1.3 with strong ciphers
- **HSTS**: Enabled with 1 year max-age
- **OCSP Stapling**: Enabled for performance

### Certificate Management
- **Self-signed**: For development/testing only
- **CA-signed**: Required for production
- **Rotation**: Every 90 days or as needed
- **Backup**: Encrypted key backups in secure location

## Access Control

### Authentication
- **API Access**: JWT tokens with expiration
- **Admin Access**: Strong passwords, 2FA recommended
- **Monitoring**: Basic auth for Grafana

### Authorization
- **Role-based Access**: Admin, User, Read-only roles
- **API Rate Limiting**: 10 req/s per IP for API, 100 req/s for static
- **Session Management**: Secure cookies, CSRF protection

## Data Protection

### Encryption at Rest
- **Database**: Encrypted storage (if using external DB)
- **Backups**: AES-256 encrypted
- **Logs**: Sensitive data redacted

### Encryption in Transit
- **HTTPS Only**: All external communications
- **Internal**: TLS between services (recommended)

## Monitoring & Alerting

### Security Monitoring
- **Log Analysis**: Automated threat detection
- **Intrusion Detection**: Pattern-based blocking
- **SSL Monitoring**: Certificate expiration alerts

### Alert Rules
- High error rates (>10%)
- Unusual traffic patterns
- SSL handshake failures
- Container restarts
- Failed authentication attempts

## Compliance

### Data Protection
- **PII Handling**: Minimize collection and storage
- **Data Retention**: 90 days for logs, 1 year for backups
- **Access Logging**: All data access logged and monitored

### Security Standards
- **Container Security**: Non-root execution, minimal images
- **Dependency Scanning**: Regular vulnerability checks
- **Code Security**: Input validation, secure coding practices

## Incident Response

### Detection
- Automated monitoring and alerting
- Log analysis for suspicious activity
- Regular security audits

### Response
1. **Isolate**: Block suspicious IPs, quarantine affected systems
2. **Investigate**: Analyze logs and system state
3. **Remediate**: Apply fixes, rotate credentials
4. **Report**: Document incident and lessons learned

### Communication
- **Internal**: Security team notification
- **External**: User notification for data breaches (if applicable)

## Maintenance

### Regular Tasks
- **Security Updates**: Weekly patching schedule
- **Vulnerability Scans**: Monthly automated scans
- **Access Reviews**: Quarterly access permission audits
- **Backup Testing**: Monthly restore testing

### Emergency Procedures
- **Security Breach**: Immediate isolation and investigation
- **Data Loss**: Restore from encrypted backups
- **Service Disruption**: Failover to backup systems

## Contact

For security concerns or incidents:
- **Security Team**: security@ghostlink.local
- **Emergency**: +1-XXX-XXX-XXXX
- **PGP Key**: Available at security@ghostlink.local

## Version History

- v1.0: Initial security policy (December 2025)
EOF

    print_success "Security policy documentation created"
}

# Display firewall status
show_status() {
    print_status "Firewall configuration status:"

    case $FIREWALL_CMD in
        ufw)
            sudo ufw status verbose
            ;;
        firewalld)
            sudo firewall-cmd --list-all
            ;;
        iptables)
            sudo iptables -L -n -v
            ;;
        macos)
            echo "macOS Firewall Status:"
            /usr/libexec/ApplicationFirewall/socketfilterfw --getglobalstate
            ;;
    esac
}

# Main firewall setup function
main() {
    echo "🔥 GhostLink Firewall Configuration"
    echo "=================================="

    check_system

    case $FIREWALL_CMD in
        ufw)
            setup_ufw
            ;;
        firewalld)
            setup_firewalld
            ;;
        iptables)
            setup_iptables
            ;;
        macos)
            setup_macos
            ;;
    esac

    setup_docker_network
    create_security_policy
    show_status

    print_success "🎉 Firewall configuration completed!"
    print_status "📋 Important notes:"
    echo "   - Review firewall rules before deploying to production"
    echo "   - Test connectivity after applying rules"
    echo "   - Document any custom ports that need to be opened"
    echo "   - Consider implementing a WAF (Web Application Firewall) for additional protection"
}

# Run main function
main "$@"
EOF

    chmod +x "./security/setup-firewall.sh"

    print_success "Firewall configuration script created"
}

# Create compliance documentation
create_compliance_docs() {
    print_status "Creating compliance documentation..."

    cat > "./security/COMPLIANCE_CHECKLIST.md" << 'EOF'
# GhostLink Compliance Checklist

## GDPR Compliance (EU General Data Protection Regulation)

### Data Collection & Processing
- [ ] **Data Minimization**: Only collect necessary personal data
- [ ] **Purpose Limitation**: Clear purpose for data collection
- [ ] **Legal Basis**: Valid legal basis for processing
- [ ] **Data Subject Rights**: Implement access, rectification, erasure rights
- [ ] **Consent Management**: Clear consent mechanisms where required

### Security Measures
- [ ] **Data Protection**: Encryption at rest and in transit
- [ ] **Access Controls**: Role-based access with least privilege
- [ ] **Audit Logging**: Comprehensive logging of data access
- [ ] **Breach Notification**: 72-hour breach notification process
- [ ] **Data Portability**: Ability to export user data

### Technical Controls
- [ ] **SSL/TLS**: HTTPS-only with strong cipher suites
- [ ] **Input Validation**: Prevent injection attacks
- [ ] **Rate Limiting**: DDoS protection
- [ ] **Regular Backups**: Encrypted backup procedures
- [ ] **Vulnerability Management**: Regular security updates

## SOC 2 Compliance (Service Organization Control)

### Security (CC1.1, CC2.1, CC3.1, CC4.1, CC5.1)
- [ ] **Logical Access**: Multi-factor authentication for admin access
- [ ] **Network Security**: Firewall configuration and monitoring
- [ ] **Endpoint Protection**: Secure development practices
- [ ] **Change Management**: Version control and deployment procedures
- [ ] **Incident Response**: Documented incident response plan

### Availability (CC7.1)
- [ ] **Business Continuity**: Disaster recovery procedures
- [ ] **System Availability**: 99.9% uptime monitoring
- [ ] **Backup Procedures**: Regular backup testing
- [ ] **Capacity Planning**: Resource monitoring and scaling

### Confidentiality (CC6.1)
- [ ] **Data Classification**: Sensitive data identification
- [ ] **Encryption**: Data encryption standards
- [ ] **Access Monitoring**: Unauthorized access detection

## ISO 27001 Information Security Management

### Information Security Policies
- [ ] **Security Policy**: Comprehensive security policy document
- [ ] **Acceptable Use**: Clear acceptable use policies
- [ ] **Access Control Policy**: Authentication and authorization procedures
- [ ] **Incident Management**: Incident reporting and handling procedures

### Organization of Information Security
- [ ] **Roles & Responsibilities**: Clear security roles defined
- [ ] **Segregation of Duties**: Prevent single points of failure
- [ ] **Contact Points**: Security contact information documented

### Human Resources Security
- [ ] **Pre-employment**: Background checks for sensitive roles
- [ ] **During Employment**: Security awareness training
- [ ] **Termination**: Access revocation procedures

### Asset Management
- [ ] **Asset Inventory**: Complete inventory of information assets
- [ ] **Asset Ownership**: Clear ownership and responsibility
- [ ] **Acceptable Use**: Asset usage guidelines

### Access Control
- [ ] **Access Control Policy**: Comprehensive access control procedures
- [ ] **User Registration**: Secure user registration process
- [ ] **Privilege Management**: Least privilege principle implementation
- [ ] **Remote Access**: Secure remote access procedures

### Cryptography
- [ ] **Cryptographic Controls**: Encryption policy and procedures
- [ ] **Key Management**: Secure key generation and storage
- [ ] **Digital Signatures**: Digital signature procedures

### Physical & Environmental Security
- [ ] **Physical Access**: Secure physical access controls
- [ ] **Equipment Protection**: Equipment protection measures
- [ ] **Secure Disposal**: Secure data disposal procedures

## HIPAA Compliance (Health Information)

*Note: Only applicable if handling protected health information (PHI)*

### Technical Safeguards
- [ ] **Access Control**: Unique user identification and emergency access
- [ ] **Audit Controls**: Hardware/software for audit logging
- [ ] **Integrity**: Mechanisms to verify data integrity
- [ ] **Transmission Security**: Data transmission protection

### Administrative Safeguards
- [ ] **Security Management**: Risk analysis and management
- [ ] **Assigned Security**: Security responsibility assignment
- [ ] **Workforce Security**: Authorization and supervision
- [ ] **Information Access**: Access authorization and establishment

### Physical Safeguards
- [ ] **Facility Access**: Physical access controls
- [ ] **Workstation Security**: Workstation security measures
- [ ] **Device Security**: Device and media controls

## PCI DSS Compliance (Payment Card Industry)

*Note: Only applicable if processing payment card data*

### Build & Maintain Secure Network
- [ ] **Firewall Configuration**: Secure firewall configuration
- [ ] **System Passwords**: No vendor default passwords

### Protect Cardholder Data
- [ ] **Data Storage**: Secure storage of cardholder data
- [ ] **Data Transmission**: Secure transmission of cardholder data
- [ ] **Data Masking**: Mask PAN when displayed
- [ ] **Data Encryption**: Encrypt transmission of cardholder data

### Maintain Vulnerability Management Program
- [ ] **Antivirus Software**: Deploy antivirus software
- [ ] **Security Updates**: Regular security updates
- [ ] **Vulnerability Scans**: Regular vulnerability scans

## Regular Compliance Activities

### Monthly
- [ ] **Access Reviews**: Review user access permissions
- [ ] **Log Reviews**: Review security logs and events
- [ ] **Vulnerability Scans**: Perform vulnerability assessments
- [ ] **Patch Management**: Apply security patches

### Quarterly
- [ ] **Risk Assessments**: Conduct risk assessments
- [ ] **Policy Reviews**: Review security policies
- [ ] **Training**: Security awareness training
- [ ] **Backup Testing**: Test backup restoration procedures

### Annually
- [ ] **Compliance Audits**: Third-party compliance audits
- [ ] **Business Impact Analysis**: Update BIA and risk assessments
- [ ] **Disaster Recovery Testing**: Full disaster recovery testing
- [ ] **Penetration Testing**: External penetration testing

## Compliance Evidence Collection

### Documentation Required
- [ ] **Policies & Procedures**: Comprehensive security documentation
- [ ] **Risk Assessments**: Regular risk assessment reports
- [ ] **Audit Logs**: Security event logs and monitoring reports
- [ ] **Training Records**: Security training completion records
- [ ] **Incident Reports**: Security incident documentation

### Technical Evidence
- [ ] **Configuration Backups**: System configuration documentation
- [ ] **Vulnerability Scans**: Scan results and remediation plans
- [ ] **Access Control Lists**: User access permission lists
- [ ] **Change Records**: System change documentation

## Compliance Reporting

### Internal Reporting
- Monthly compliance status reports
- Quarterly risk assessment updates
- Annual compliance certification

### External Reporting
- Customer compliance inquiries
- Regulatory reporting requirements
- Third-party audit coordination

## Contact Information

- **Compliance Officer**: compliance@ghostlink.local
- **Security Team**: security@ghostlink.local
- **Legal Counsel**: legal@ghostlink.local

*Last Updated: December 2025*
EOF

    print_success "Compliance documentation created"
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