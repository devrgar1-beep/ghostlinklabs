#!/bin/bash

# GhostLink Performance Optimization Manager
# Manages caching, connection pooling, and performance optimizations

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check system performance
check_performance() {
    print_status "Checking current system performance..."

    # CPU usage
    cpu_usage=$(top -bn1 | grep "Cpu(s)" | sed "s/.*, *\([0-9.]*\)%* id.*/\1/" | awk '{print 100 - $1}')
    echo "CPU Usage: ${cpu_usage}%"

    # Memory usage
    mem_usage=$(free | grep Mem | awk '{printf "%.2f", $3/$2 * 100.0}')
    echo "Memory Usage: ${mem_usage}%"

    # Disk usage
    disk_usage=$(df / | tail -1 | awk '{print $5}' | sed 's/%//')
    echo "Disk Usage: ${disk_usage}%"

    # Network connections
    net_connections=$(netstat -tun | grep ESTABLISHED | wc -l)
    echo "Network Connections: ${net_connections}"

    # Check if services are running
    if command -v docker &> /dev/null && docker ps | grep -q ghostlink; then
        echo "Docker Services: Running"
    else
        echo "Docker Services: Not running or not accessible"
    fi

    if pgrep -f "redis-server" > /dev/null; then
        echo "Redis: Running"
    else
        echo "Redis: Not running"
    fi
}

# Optimize system settings
optimize_system() {
    print_status "Optimizing system settings..."

    # Increase file descriptors
    if [ "$(ulimit -n)" -lt 65536 ]; then
        ulimit -n 65536 2>/dev/null || print_warning "Could not increase file descriptors (need root)"
    fi

    # Optimize kernel parameters (requires root)
    if [ "$EUID" -eq 0 ]; then
        # Network optimizations
        sysctl -w net.core.somaxconn=65536 >/dev/null 2>&1
        sysctl -w net.ipv4.tcp_max_syn_backlog=65536 >/dev/null 2>&1
        sysctl -w net.ipv4.ip_local_port_range="1024 65535" >/dev/null 2>&1

        # Memory optimizations
        sysctl -w vm.swappiness=10 >/dev/null 2>&1
        sysctl -w vm.dirty_ratio=60 >/dev/null 2>&1
        sysctl -w vm.dirty_background_ratio=2 >/dev/null 2>&1

        print_success "System optimizations applied"
    else
        print_warning "System optimizations require root privileges"
    fi
}

# Clear caches
clear_caches() {
    print_status "Clearing performance caches..."

    # Clear system cache (requires root)
    if [ "$EUID" -eq 0 ]; then
        sync
        echo 3 > /proc/sys/vm/drop_caches
        print_success "System caches cleared"
    else
        print_warning "System cache clearing requires root privileges"
    fi

    # Clear Redis cache
    if command -v redis-cli &> /dev/null; then
        redis-cli FLUSHALL >/dev/null 2>&1 && print_success "Redis cache cleared" || print_warning "Could not clear Redis cache"
    fi

    # Clear Nginx cache
    if [ -d "./cache/nginx" ]; then
        rm -rf ./cache/nginx/* && print_success "Nginx cache cleared" || print_warning "Could not clear Nginx cache"
    fi
}

# Monitor performance in real-time
monitor_performance() {
    print_status "Starting real-time performance monitoring (Ctrl+C to stop)..."

    while true; do
        echo "=== Performance Snapshot $(date) ==="
        echo "CPU: $(top -bn1 | grep "Cpu(s)" | sed "s/.*, *\([0-9.]*\)%* id.*/\1/" | awk '{print 100 - $1}')%"
        echo "Memory: $(free | grep Mem | awk '{printf "%.1f", $3/$2 * 100.0}')%"
        echo "Load: $(uptime | awk -F'load average:' '{ print $2 }')"
        echo "Connections: $(netstat -tun | grep ESTABLISHED | wc -l)"
        echo ""

        if command -v docker &> /dev/null; then
            echo "Docker Containers:"
            docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}" 2>/dev/null || echo "No containers running"
            echo ""
        fi

        sleep 5
    done
}

# Generate performance report
generate_report() {
    print_status "Generating performance optimization report..."

    report_file="./logs/performance/optimization-report-$(date +%Y%m%d-%H%M%S).txt"

    {
        echo "GhostLink Performance Optimization Report"
        echo "Generated: $(date)"
        echo "=========================================="
        echo ""

        echo "System Information:"
        echo "-------------------"
        uname -a
        echo "CPU Cores: $(nproc)"
        echo "Total Memory: $(free -h | grep Mem | awk '{print $2}')"
        echo ""

        echo "Current Performance Metrics:"
        echo "----------------------------"
        echo "CPU Usage: $(top -bn1 | grep "Cpu(s)" | sed "s/.*, *\([0-9.]*\)%* id.*/\1/" | awk '{print 100 - $1}')%"
        echo "Memory Usage: $(free | grep Mem | awk '{printf "%.2f", $3/$2 * 100.0}')%"
        echo "Disk Usage: $(df / | tail -1 | awk '{print $5}')"
        echo "Network Connections: $(netstat -tun | grep ESTABLISHED | wc -l)"
        echo ""

        if command -v docker &> /dev/null; then
            echo "Docker Performance:"
            echo "-------------------"
            docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemPerc}}\t{{.NetIO}}\t{{.BlockIO}}" 2>/dev/null || echo "No containers accessible"
            echo ""
        fi

        echo "Optimization Recommendations:"
        echo "----------------------------"

        cpu_usage=$(top -bn1 | grep "Cpu(s)" | sed "s/.*, *\([0-9.]*\)%* id.*/\1/" | awk '{print 100 - $1}')
        if (( $(echo "$cpu_usage > 80" | bc -l) )); then
            echo "- High CPU usage detected. Consider horizontal scaling or optimizing CPU-intensive operations."
        fi

        mem_usage=$(free | grep Mem | awk '{printf "%.2f", $3/$2 * 100.0}')
        if (( $(echo "$mem_usage > 85" | bc -l) )); then
            echo "- High memory usage detected. Consider increasing memory limits or optimizing memory usage."
        fi

        disk_usage=$(df / | tail -1 | awk '{print $5}' | sed 's/%//')
        if [ "$disk_usage" -gt 90 ]; then
            echo "- High disk usage detected. Consider cleanup or increasing disk space."
        fi

        echo "- Ensure Redis caching is enabled and properly configured."
        echo "- Verify Nginx caching is active and cache hit ratios are monitored."
        echo "- Check connection pooling is implemented for database connections."
        echo "- Monitor application logs for performance bottlenecks."

    } > "$report_file"

    print_success "Performance report generated: $report_file"
}

# Main function
main() {
    case "${1:-status}" in
        "status")
            check_performance
            ;;
        "optimize")
            optimize_system
            ;;
        "clear-cache")
            clear_caches
            ;;
        "monitor")
            monitor_performance
            ;;
        "report")
            generate_report
            ;;
        "all")
            check_performance
            echo ""
            optimize_system
            echo ""
            clear_caches
            echo ""
            generate_report
            ;;
        *)
            echo "Usage: $0 [status|optimize|clear-cache|monitor|report|all]"
            echo "  status      - Check current performance status"
            echo "  optimize    - Apply system optimizations"
            echo "  clear-cache - Clear all caches"
            echo "  monitor     - Real-time performance monitoring"
            echo "  report      - Generate performance report"
            echo "  all         - Run all optimization tasks"
            exit 1
            ;;
    esac
}

main "$@"
