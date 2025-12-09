#!/bin/bash
# System-level GhostLink integration

set -e

# Install dependencies
install_dependencies() {
    echo "Installing system dependencies..."
    if command -v apt-get &> /dev/null; then
        sudo apt-get update
        sudo apt-get install -y htop iotop sysstat curl wget jq
    elif command -v yum &> /dev/null; then
        sudo yum install -y htop iotop sysstat curl wget jq
    elif command -v brew &> /dev/null; then
        brew install htop wget jq
    fi
}

# Create directories
create_directories() {
    sudo mkdir -p /opt/ghostlink
    sudo mkdir -p /etc/ghostlink
    sudo mkdir -p /var/log/ghostlink
    sudo chown -R $USER:staff /opt/ghostlink /etc/ghostlink /var/log/ghostlink
}

# Create monitoring script
create_monitoring_script() {
    cat > /opt/ghostlink/ghostlink-monitor.sh << 'MONITOR_EOF'
#!/bin/bash
# GhostLink system monitoring

while true; do
    # Collect system metrics
    CPU_USAGE=$(top -bn1 | grep "Cpu(s)" | sed "s/.*, *\([0-9.]*\)%* id.*/\1/" | awk '{print 100 - $1}')
    MEM_USAGE=$(free | grep Mem | awk '{printf "%.0f", $3/$2 * 100.0}')
    DISK_USAGE=$(df / | tail -1 | awk '{print $5}' | sed 's/%//')

    # Send to GhostLink API
    curl -s -X POST http://localhost:8080/metrics \
        -H "Content-Type: application/json" \
        -d "{\"cpu\": $CPU_USAGE, \"memory\": $MEM_USAGE, \"disk\": $DISK_USAGE}" || true

    sleep 30
done
MONITOR_EOF

    chmod +x /opt/ghostlink/ghostlink-monitor.sh
}

# Create automation script
create_automation_script() {
    cat > /opt/ghostlink/ghostlink-automation.sh << 'AUTO_EOF'
#!/bin/bash
# GhostLink automation tasks

TASK=$1

case $TASK in
    "backup")
        echo "Running backup task..."
        # Add backup logic here
        ;;
    "cleanup")
        echo "Running cleanup task..."
        # Add cleanup logic here
        ;;
    "health-check")
        echo "Running health check..."
        curl -s http://localhost:8080/health
        ;;
    *)
        echo "Unknown task: $TASK"
        exit 1
        ;;
esac
AUTO_EOF

    chmod +x /opt/ghostlink/ghostlink-automation.sh
}

# Setup launch agent (macOS)
setup_launch_agent() {
    if [[ "$OSTYPE" == "darwin"* ]]; then
        mkdir -p ~/Library/LaunchAgents
        cat > ~/Library/LaunchAgents/com.ghostlink.monitor.plist << LAUNCH_EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.ghostlink.monitor</string>
    <key>ProgramArguments</key>
    <array>
        <string>/opt/ghostlink/ghostlink-monitor.sh</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/var/log/ghostlink/monitor.log</string>
    <key>StandardErrorPath</key>
    <string>/var/log/ghostlink/monitor.err</string>
</dict>
</plist>
LAUNCH_EOF

        launchctl load ~/Library/LaunchAgents/com.ghostlink.monitor.plist
    fi
}

# Setup systemd service (Linux)
setup_systemd_service() {
    if command -v systemctl &> /dev/null; then
        cat > /etc/systemd/system/ghostlink-monitor.service << SYSTEMD_EOF
[Unit]
Description=GhostLink System Monitor
After=network.target

[Service]
Type=simple
User=$USER
ExecStart=/opt/ghostlink/ghostlink-monitor.sh
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
SYSTEMD_EOF

        sudo systemctl daemon-reload
        sudo systemctl enable ghostlink-monitor
        sudo systemctl start ghostlink-monitor
    fi
}

# Create shell integration
create_shell_integration() {
    # Add to .bashrc or .zshrc
    SHELL_RC="$HOME/.bashrc"
    if [[ "$SHELL" == *"zsh"* ]]; then
        SHELL_RC="$HOME/.zshrc"
    fi

    cat >> "$SHELL_RC" << 'SHELL_EOF'

# GhostLink Shell Integration
gl-status() {
    curl -s http://localhost:8080/health | jq .status
}

gl-exec() {
    /opt/ghostlink/ghostlink-automation.sh "$1"
}

gl-logs() {
    tail -f /var/log/ghostlink/monitor.log
}
SHELL_EOF
}

# Main installation
main() {
    echo "🔧 Installing GhostLink system integration..."

    install_dependencies
    create_directories
    create_monitoring_script
    create_automation_script
    setup_launch_agent
    setup_systemd_service
    create_shell_integration

    echo "✅ System integration complete!"
    echo "Run 'gl-status' to check GhostLink status"
    echo "Run 'gl-exec <task>' to execute automation tasks"
}

main "$@"
