#!/bin/bash

# GhostLink Production Backup Script
# This script creates backups of production data and configurations

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
BACKUP_DIR="./backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_NAME="ghostlink_backup_${TIMESTAMP}"
FULL_BACKUP_PATH="${BACKUP_DIR}/${BACKUP_NAME}"

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

# Create backup directory
create_backup_dir() {
    mkdir -p "$FULL_BACKUP_PATH"
    print_success "Backup directory created: $FULL_BACKUP_PATH"
}

# Backup application data
backup_data() {
    print_status "Backing up application data..."

    # Create data directory if it doesn't exist
    mkdir -p data

    # Copy data directory
    if [ -d "data" ]; then
        cp -r data "${FULL_BACKUP_PATH}/"
        print_success "Application data backed up"
    else
        print_warning "No application data directory found"
    fi
}

# Backup logs
backup_logs() {
    print_status "Backing up logs..."

    # Create logs directory if it doesn't exist
    mkdir -p logs

    # Copy logs directory
    if [ -d "logs" ]; then
        cp -r logs "${FULL_BACKUP_PATH}/"
        print_success "Logs backed up"
    else
        print_warning "No logs directory found"
    fi
}

# Backup configurations
backup_configs() {
    print_status "Backing up configurations..."

    local config_files=(".env" "docker-compose.yml" "Dockerfile" "requirements.txt")

    for config_file in "${config_files[@]}"; do
        if [ -f "$config_file" ]; then
            cp "$config_file" "${FULL_BACKUP_PATH}/"
            print_success "$config_file backed up"
        else
            print_warning "$config_file not found"
        fi
    done

    # Backup monitoring configurations
    if [ -d "monitoring" ]; then
        cp -r monitoring "${FULL_BACKUP_PATH}/"
        print_success "Monitoring configurations backed up"
    fi

    # Backup nginx configurations
    if [ -d "nginx" ]; then
        cp -r nginx "${FULL_BACKUP_PATH}/"
        print_success "Nginx configurations backed up"
    fi
}

# Backup Docker volumes (if running)
backup_docker_volumes() {
    print_status "Backing up Docker volumes..."

    # Check if services are running
    if docker-compose ps | grep -q "Up"; then
        print_status "Services are running, backing up volumes..."

        # Backup Grafana data
        docker run --rm -v ghostlink_grafana_data:/source -v "${FULL_BACKUP_PATH}":/backup alpine tar czf /backup/grafana_data.tar.gz -C /source .
        print_success "Grafana data backed up"

        # Backup Prometheus data
        docker run --rm -v ghostlink_prometheus_data:/source -v "${FULL_BACKUP_PATH}":/backup alpine tar czf /backup/prometheus_data.tar.gz -C /source .
        print_success "Prometheus data backed up"
    else
        print_warning "Services are not running, skipping Docker volume backup"
    fi
}

# Create backup manifest
create_manifest() {
    print_status "Creating backup manifest..."

    local manifest_file="${FULL_BACKUP_PATH}/BACKUP_MANIFEST.txt"

    cat > "$manifest_file" << EOF
GhostLink Production Backup Manifest
===================================

Backup Date: $(date)
Backup Name: ${BACKUP_NAME}
Backup Location: ${FULL_BACKUP_PATH}

Included in this backup:
- Application data (./data/)
- Log files (./logs/)
- Configuration files (.env, docker-compose.yml, etc.)
- Monitoring configurations (./monitoring/)
- Nginx configurations (./nginx/)
- Docker volumes (Grafana and Prometheus data)

To restore this backup:
1. Stop all services: docker-compose down
2. Extract backup files to project root
3. Restore Docker volumes if needed
4. Start services: docker-compose up -d

Backup created by: $(whoami)
System: $(uname -a)
EOF

    print_success "Backup manifest created"
}

# Compress backup
compress_backup() {
    print_status "Compressing backup..."

    local archive_name="${BACKUP_NAME}.tar.gz"
    local archive_path="${BACKUP_DIR}/${archive_name}"

    cd "$BACKUP_DIR"
    tar czf "$archive_name" "$BACKUP_NAME"

    # Remove uncompressed backup
    rm -rf "$BACKUP_NAME"

    print_success "Backup compressed: $archive_path"

    # Calculate and display backup size
    local backup_size=$(du -sh "$archive_path" | cut -f1)
    print_success "Backup size: $backup_size"
}

# Cleanup old backups
cleanup_old_backups() {
    print_status "Cleaning up old backups..."

    # Keep only the last 7 backups
    local backup_count=$(ls -1 "${BACKUP_DIR}"/*.tar.gz 2>/dev/null | wc -l)
    if [ "$backup_count" -gt 7 ]; then
        ls -1t "${BACKUP_DIR}"/*.tar.gz | tail -n +8 | xargs rm -f
        print_success "Old backups cleaned up (keeping last 7)"
    else
        print_success "No old backups to clean up"
    fi
}

# Main backup function
main() {
    echo "💾 GhostLink Production Backup Script"
    echo "===================================="

    create_backup_dir
    backup_data
    backup_logs
    backup_configs
    backup_docker_volumes
    create_manifest
    compress_backup
    cleanup_old_backups

    print_success "🎉 Backup completed successfully!"
    print_status "Backup location: ${BACKUP_DIR}/${BACKUP_NAME}.tar.gz"
}

# Run main function
main "$@"