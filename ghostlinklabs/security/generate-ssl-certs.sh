#!/bin/bash

# GhostLink SSL Certificate Generation Script
# Generates self-signed certificates for development and testing

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
CERT_DIR="./nginx/ssl"
DAYS_VALID=365
COUNTRY="US"
STATE="California"
CITY="San Francisco"
ORGANIZATION="GhostLink Labs"
UNIT="AI Systems"
COMMON_NAME="ghostlink.local"
EMAIL="admin@ghostlink.local"

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

# Create certificate directory
create_cert_dir() {
    print_status "Creating SSL certificate directory..."
    mkdir -p "$CERT_DIR"
    chmod 700 "$CERT_DIR"
    print_success "Certificate directory created: $CERT_DIR"
}

# Generate private key
generate_private_key() {
    print_status "Generating private key..."
    openssl genrsa -out "$CERT_DIR/ghostlink.key" 2048
    chmod 600 "$CERT_DIR/ghostlink.key"
    print_success "Private key generated"
}

# Generate certificate signing request
generate_csr() {
    print_status "Generating certificate signing request..."

    # Create OpenSSL configuration for SAN
    cat > "$CERT_DIR/ghostlink.cnf" << EOF
[req]
distinguished_name = req_distinguished_name
req_extensions = v3_req
prompt = no

[req_distinguished_name]
C = $COUNTRY
ST = $STATE
L = $CITY
O = $ORGANIZATION
OU = $UNIT
CN = $COMMON_NAME
emailAddress = $EMAIL

[v3_req]
keyUsage = keyEncipherment, dataEncipherment
extendedKeyUsage = serverAuth
subjectAltName = @alt_names

[alt_names]
DNS.1 = $COMMON_NAME
DNS.2 = localhost
DNS.3 = ghostlink.local
IP.1 = 127.0.0.1
IP.2 = 0.0.0.0
EOF

    openssl req -new -key "$CERT_DIR/ghostlink.key" \
                -out "$CERT_DIR/ghostlink.csr" \
                -config "$CERT_DIR/ghostlink.cnf"

    print_success "CSR generated"
}

# Generate self-signed certificate
generate_certificate() {
    print_status "Generating self-signed certificate..."

    openssl x509 -req -days $DAYS_VALID \
                 -in "$CERT_DIR/ghostlink.csr" \
                 -signkey "$CERT_DIR/ghostlink.key" \
                 -out "$CERT_DIR/ghostlink.crt" \
                 -extensions v3_req \
                 -extfile "$CERT_DIR/ghostlink.cnf"

    print_success "Certificate generated (valid for $DAYS_VALID days)"
}

# Generate Diffie-Hellman parameters
generate_dhparam() {
    print_status "Generating Diffie-Hellman parameters..."
    openssl dhparam -out "$CERT_DIR/dhparam.pem" 2048
    print_success "DH parameters generated"
}

# Create certificate chain
create_chain() {
    print_status "Creating certificate chain..."
    cat "$CERT_DIR/ghostlink.crt" > "$CERT_DIR/chain.pem"
    print_success "Certificate chain created"
}

# Display certificate information
show_cert_info() {
    print_status "Certificate information:"
    echo "Subject: $(openssl x509 -in "$CERT_DIR/ghostlink.crt" -subject -noout)"
    echo "Issuer: $(openssl x509 -in "$CERT_DIR/ghostlink.crt" -issuer -noout)"
    echo "Valid from: $(openssl x509 -in "$CERT_DIR/ghostlink.crt" -startdate -noout)"
    echo "Valid until: $(openssl x509 -in "$CERT_DIR/ghostlink.crt" -enddate -noout)"
    echo "Serial: $(openssl x509 -in "$CERT_DIR/ghostlink.crt" -serial -noout)"
    echo "SHA256: $(openssl x509 -in "$CERT_DIR/ghostlink.crt" -fingerprint -sha256 -noout)"
}

# Verify certificate
verify_certificate() {
    print_status "Verifying certificate..."
    openssl verify -CAfile "$CERT_DIR/ghostlink.crt" "$CERT_DIR/ghostlink.crt"
    print_success "Certificate verification successful"
}

# Create README for certificates
create_readme() {
    cat > "$CERT_DIR/README.md" << EOF
# GhostLink SSL Certificates

This directory contains SSL/TLS certificates for GhostLink production deployment.

## Files

- \`ghostlink.key\` - Private key (keep secure!)
- \`ghostlink.crt\` - SSL certificate
- \`ghostlink.csr\` - Certificate signing request
- \`ghostlink.cnf\` - OpenSSL configuration
- \`dhparam.pem\` - Diffie-Hellman parameters
- \`chain.pem\` - Certificate chain

## Security Notes

- The private key (\`ghostlink.key\`) should never be shared
- These are self-signed certificates for development/testing
- For production, obtain certificates from a trusted CA
- Regularly rotate certificates before expiration

## Certificate Details

$(openssl x509 -in "$CERT_DIR/ghostlink.crt" -text -noout | grep -E "(Subject:|Issuer:|Not Before|Not After|Serial Number)")

## Usage

These certificates are automatically used by the Nginx reverse proxy in production deployment.

For custom certificate installation:
1. Replace \`ghostlink.crt\` with your certificate
2. Replace \`ghostlink.key\` with your private key
3. Update \`chain.pem\` if using intermediate certificates
4. Restart the nginx service: \`docker-compose restart nginx\`

Generated on: $(date)
EOF

    print_success "Certificate README created"
}

# Main certificate generation function
main() {
    echo "🔐 GhostLink SSL Certificate Generation"
    echo "====================================="

    create_cert_dir
    generate_private_key
    generate_csr
    generate_certificate
    generate_dhparam
    create_chain
    verify_certificate
    show_cert_info
    create_readme

    print_success "🎉 SSL certificates generated successfully!"
    print_warning "⚠️  These are self-signed certificates for development/testing only"
    print_status "📁 Certificates saved in: $CERT_DIR"
    print_status "🔄 For production, obtain certificates from a trusted Certificate Authority"
}

# Run main function
main "$@"