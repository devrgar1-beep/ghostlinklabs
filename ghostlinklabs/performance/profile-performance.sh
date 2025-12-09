#!/bin/bash

# GhostLink Performance Profiling Script
# Comprehensive performance analysis and optimization recommendations

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
RESULTS_DIR="./performance/profiles"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
PROFILE_ID="profile_${TIMESTAMP}"

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

# Create results directory
setup_profile_dir() {
    mkdir -p "$RESULTS_DIR"
    PROFILE_DIR="$RESULTS_DIR/$PROFILE_ID"
    mkdir -p "$PROFILE_DIR"

    print_success "Profile directory created: $PROFILE_DIR"
}

# System information gathering
gather_system_info() {
    print_status "Gathering system information..."

    local sysinfo_file="$PROFILE_DIR/system_info.txt"

    cat > "$sysinfo_file" << EOF
GhostLink System Performance Profile
====================================
Profile ID: $PROFILE_ID
Date: $(date)
Hostname: $(hostname)
OS: $(uname -a)

Hardware Information:
EOF

    # CPU Information
    echo "CPU:" >> "$sysinfo_file"
    if command -v lscpu &> /dev/null; then
        lscpu | grep -E "(Architecture|CPU\(s\)|Model name|CPU MHz|Cache)" >> "$sysinfo_file"
    else
        sysctl -n machdep.cpu.brand_string >> "$sysinfo_file" 2>/dev/null || echo "CPU info not available" >> "$sysinfo_file"
    fi

    echo "" >> "$sysinfo_file"
    echo "Memory:" >> "$sysinfo_file"
    if command -v free &> /dev/null; then
        free -h >> "$sysinfo_file"
    else
        vm_stat | grep -E "(Pages free|Pages active|Pages wired)" >> "$sysinfo_file" 2>/dev/null || echo "Memory info not available" >> "$sysinfo_file"
    fi

    echo "" >> "$sysinfo_file"
    echo "Disk:" >> "$sysinfo_file"
    df -h >> "$sysinfo_file"

    echo "" >> "$sysinfo_file"
    echo "Network:" >> "$sysinfo_file"
    ifconfig 2>/dev/null | head -20 >> "$sysinfo_file" || ip addr 2>/dev/null | head -20 >> "$sysinfo_file" || echo "Network info not available" >> "$sysinfo_file"

    print_success "System information gathered"
}

# Docker container analysis
analyze_containers() {
    print_status "Analyzing Docker containers..."

    if ! command -v docker &> /dev/null; then
        print_warning "Docker not available, skipping container analysis"
        return
    fi

    local container_file="$PROFILE_DIR/containers.txt"

    cat > "$container_file" << EOF
Docker Container Analysis
=========================

Running Containers:
EOF

    docker ps --format "table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}" >> "$container_file"

    echo "" >> "$container_file"
    echo "Container Resource Usage:" >> "$container_file"
    docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}\t{{.BlockIO}}" >> "$container_file"

    echo "" >> "$container_file"
    echo "Container Images:" >> "$container_file"
    docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}" >> "$container_file"

    print_success "Container analysis completed"
}

# Application performance profiling
profile_application() {
    print_status "Profiling application performance..."

    local app_profile="$PROFILE_DIR/application_profile.txt"

    cat > "$app_profile" << EOF
Application Performance Profile
===============================

Process Analysis:
EOF

    # Check for GhostLink processes
    if pgrep -f "ghostlink\|python.*ghostlink" > /dev/null; then
        echo "GhostLink processes found:" >> "$app_profile"
        ps aux | grep -E "(ghostlink|python.*ghostlink)" | grep -v grep >> "$app_profile"
    else
        echo "No GhostLink processes currently running" >> "$app_profile"
    fi

    echo "" >> "$app_profile"
    echo "Network Connections:" >> "$app_profile"
    netstat -tlnp 2>/dev/null | grep -E ":(3000|8000|9090|3001)" || ss -tlnp 2>/dev/null | grep -E ":(3000|8000|9090|3001)" || echo "Network analysis not available" >> "$app_profile"

    echo "" >> "$app_profile"
    echo "Open Files (if available):" >> "$app_profile"
    lsof -i :3000 2>/dev/null | head -10 >> "$app_profile" || echo "lsof not available" >> "$app_profile"

    print_success "Application profiling completed"
}

# Memory analysis
analyze_memory() {
    print_status "Analyzing memory usage..."

    local memory_file="$PROFILE_DIR/memory_analysis.txt"

    cat > "$memory_file" << EOF
Memory Usage Analysis
======================

Current Memory Usage:
EOF

    if command -v free &> /dev/null; then
        free -h >> "$memory_file"
        echo "" >> "$memory_file"
        echo "Detailed Memory Info:" >> "$memory_file"
        cat /proc/meminfo 2>/dev/null | head -20 >> "$memory_file" || echo "/proc/meminfo not available" >> "$memory_file"
    else
        # macOS memory info
        vm_stat >> "$memory_file" 2>/dev/null || echo "Memory info not available" >> "$memory_file"
    fi

    echo "" >> "$memory_file"
    echo "Top Memory Consumers:" >> "$memory_file"
    ps aux --sort=-%mem | head -10 >> "$memory_file" 2>/dev/null || ps aux | sort -rk 4 | head -10 >> "$memory_file" 2>/dev/null || echo "Process memory info not available" >> "$memory_file"

    print_success "Memory analysis completed"
}

# CPU analysis
analyze_cpu() {
    print_status "Analyzing CPU usage..."

    local cpu_file="$PROFILE_DIR/cpu_analysis.txt"

    cat > "$cpu_file" << EOF
CPU Usage Analysis
===================

CPU Information:
EOF

    if command -v lscpu &> /dev/null; then
        lscpu >> "$cpu_file"
    else
        sysctl -n machdep.cpu 2>/dev/null >> "$cpu_file" || echo "CPU info not available" >> "$cpu_file"
    fi

    echo "" >> "$cpu_file"
    echo "Current CPU Usage:" >> "$cpu_file"
    top -bn1 | head -20 >> "$cpu_file" 2>/dev/null || echo "Top command not available" >> "$cpu_file"

    echo "" >> "$cpu_file"
    echo "Top CPU Consumers:" >> "$cpu_file"
    ps aux --sort=-%cpu | head -10 >> "$cpu_file" 2>/dev/null || ps aux | sort -rk 3 | head -10 >> "$cpu_file" 2>/dev/null || echo "Process CPU info not available" >> "$cpu_file"

    print_success "CPU analysis completed"
}

# Disk I/O analysis
analyze_disk_io() {
    print_status "Analyzing disk I/O..."

    local disk_file="$PROFILE_DIR/disk_analysis.txt"

    cat > "$disk_file" << EOF
Disk I/O Analysis
==================

Disk Usage:
EOF

    df -h >> "$disk_file"

    echo "" >> "$disk_file"
    echo "Disk I/O Statistics:" >> "$disk_file"
    iostat -x 1 5 2>/dev/null | tail -10 >> "$disk_file" || echo "iostat not available" >> "$disk_file"

    echo "" >> "$disk_file"
    echo "File System Details:" >> "$disk_file"
    mount | grep -E "(ext4|xfs|btrfs|zfs|apfs)" >> "$disk_file" 2>/dev/null || mount >> "$disk_file" 2>/dev/null || echo "Mount info not available" >> "$disk_file"

    print_success "Disk I/O analysis completed"
}

# Network analysis
analyze_network() {
    print_status "Analyzing network performance..."

    local network_file="$PROFILE_DIR/network_analysis.txt"

    cat > "$network_file" << EOF
Network Performance Analysis
=============================

Network Interfaces:
EOF

    ifconfig 2>/dev/null >> "$network_file" || ip addr 2>/dev/null >> "$network_file" || echo "Network interface info not available" >> "$network_file"

    echo "" >> "$network_file"
    echo "Network Statistics:" >> "$network_file"
    netstat -i 2>/dev/null >> "$network_file" || echo "Network stats not available" >> "$network_file"

    echo "" >> "$network_file"
    echo "Open Connections:" >> "$network_file"
    netstat -t 2>/dev/null | wc -l >> "$network_file" 2>/dev/null || ss -t 2>/dev/null | wc -l >> "$network_file" 2>/dev/null || echo "Connection count not available" >> "$network_file"

    echo "" >> "$network_file"
    echo "Network Latency Test (if internet available):" >> "$network_file"
    ping -c 3 8.8.8.8 2>/dev/null | tail -3 >> "$network_file" || echo "Ping test not available" >> "$network_file"

    print_success "Network analysis completed"
}

# Generate performance recommendations
generate_recommendations() {
    print_status "Generating performance recommendations..."

    local recommendations_file="$PROFILE_DIR/recommendations.txt"

    cat > "$recommendations_file" << EOF
GhostLink Performance Recommendations
=====================================

Profile ID: $PROFILE_ID
Generated: $(date)

PERFORMANCE OPTIMIZATION RECOMMENDATIONS:
=========================================

1. SYSTEM RESOURCE OPTIMIZATION
-------------------------------

Memory Optimization:
- Monitor memory usage patterns
- Consider increasing RAM if consistently >80% usage
- Implement memory limits for containers
- Optimize application memory allocation

CPU Optimization:
- Monitor CPU usage during peak loads
- Consider CPU affinity for critical processes
- Implement CPU limits for containers
- Profile and optimize CPU-intensive operations

Disk I/O Optimization:
- Use SSD storage for better I/O performance
- Implement disk caching strategies
- Monitor disk usage and implement log rotation
- Consider RAID configuration for redundancy

2. APPLICATION OPTIMIZATION
---------------------------

Container Optimization:
- Use multi-stage Docker builds to reduce image size
- Implement proper resource limits (CPU, memory)
- Use health checks for container orchestration
- Optimize Docker layer caching

API Optimization:
- Implement response caching (Redis/memcached)
- Use connection pooling for database connections
- Optimize database queries and indexes
- Implement rate limiting and request queuing

AI Orchestrator Optimization:
- Implement model caching for frequently used models
- Use GPU acceleration if available
- Optimize memory usage for AI models
- Implement model quantization for better performance

3. INFRASTRUCTURE OPTIMIZATION
------------------------------

Load Balancing:
- Implement horizontal scaling with load balancers
- Use container orchestration (Kubernetes/Docker Swarm)
- Implement auto-scaling based on metrics
- Distribute load across multiple instances

Monitoring & Alerting:
- Set up comprehensive monitoring (Prometheus/Grafana)
- Implement alerting for performance thresholds
- Monitor resource usage trends
- Set up automated performance testing

4. NETWORK OPTIMIZATION
-----------------------

Network Configuration:
- Optimize network stack settings
- Implement HTTP/2 for better performance
- Use CDN for static assets
- Implement connection keep-alive

Security Performance:
- Use efficient SSL/TLS termination
- Implement security at the edge (WAF, CDN)
- Optimize security scanning performance
- Balance security with performance requirements

5. SCALING STRATEGIES
---------------------

Horizontal Scaling:
- Implement stateless application design
- Use container orchestration platforms
- Implement service discovery and load balancing
- Design for elastic scaling

Vertical Scaling:
- Monitor resource usage patterns
- Upgrade hardware based on bottlenecks
- Optimize application for available resources
- Implement resource quotas and limits

6. CACHING STRATEGIES
---------------------

Application Caching:
- Implement multi-level caching (browser, CDN, application, database)
- Use Redis for session and data caching
- Implement cache invalidation strategies
- Monitor cache hit rates and performance

Database Caching:
- Implement query result caching
- Use database connection pooling
- Optimize database indexes
- Implement read replicas for scaling

7. PERFORMANCE MONITORING
-------------------------

Key Metrics to Monitor:
- Response time (p50, p95, p99)
- Throughput (requests per second)
- Error rates and types
- Resource utilization (CPU, memory, disk, network)
- Application-specific metrics (AI model performance, etc.)

Monitoring Tools:
- Prometheus for metrics collection
- Grafana for visualization
- Application Performance Monitoring (APM)
- Custom business metrics

8. MAINTENANCE & OPTIMIZATION
-----------------------------

Regular Tasks:
- Performance testing after deployments
- Resource usage trend analysis
- Code profiling and optimization
- Database maintenance and optimization

Emergency Procedures:
- Performance degradation response plan
- Resource exhaustion handling
- Auto-scaling trigger configuration
- Performance incident postmortem process

IMPLEMENTATION PRIORITY:
========================

HIGH PRIORITY (Immediate):
- Implement basic monitoring and alerting
- Set resource limits for containers
- Optimize database queries and connections
- Implement response caching

MEDIUM PRIORITY (1-2 weeks):
- Implement horizontal scaling capabilities
- Optimize network configuration
- Set up comprehensive monitoring
- Implement performance testing automation

LOW PRIORITY (1-2 months):
- Implement advanced caching strategies
- Optimize AI model performance
- Set up auto-scaling
- Implement advanced monitoring and alerting

For detailed implementation guidance, refer to the performance test results
and monitoring dashboards.
EOF

    print_success "Performance recommendations generated"
}

# Generate summary report
generate_summary() {
    print_status "Generating performance summary..."

    local summary_file="$PROFILE_DIR/performance_summary.md"

    cat > "$summary_file" << EOF
# GhostLink Performance Profile Summary

**Profile ID:** $PROFILE_ID
**Date:** $(date)
**System:** $(hostname)

## Profile Overview

This performance profile provides a comprehensive analysis of the GhostLink system's current performance characteristics and optimization opportunities.

## Key Findings

### System Resources
- **CPU:** $(grep -c "processor" /proc/cpuinfo 2>/dev/null || sysctl -n hw.ncpu 2>/dev/null || echo "Unknown") cores
- **Memory:** $(free -h | grep "^Mem:" | awk '{print $2}' 2>/dev/null || echo "Unknown")
- **Storage:** $(df -h / | tail -1 | awk '{print $2}' 2>/dev/null || echo "Unknown")

### Current Performance Status
- System resource utilization analysis completed
- Container performance metrics collected
- Application profiling data gathered
- Network performance characteristics analyzed

## Performance Metrics

See detailed analysis in the following files:
- System Information: \`system_info.txt\`
- Container Analysis: \`containers.txt\`
- Application Profile: \`application_profile.txt\`
- Memory Analysis: \`memory_analysis.txt\`
- CPU Analysis: \`cpu_analysis.txt\`
- Disk Analysis: \`disk_analysis.txt\`
- Network Analysis: \`network_analysis.txt\`

## Recommendations

See \`recommendations.txt\` for detailed optimization recommendations.

## Next Steps

1. **Review Recommendations:** Address high-priority optimization opportunities
2. **Implement Monitoring:** Set up continuous performance monitoring
3. **Load Testing:** Run comprehensive load tests to establish baselines
4. **Optimization:** Implement identified performance improvements
5. **Re-profile:** Re-run profiling after optimizations to measure improvements

## Files Generated

All profile data is stored in: \`$PROFILE_DIR/\`

---
*Generated by GhostLink Performance Profiling Suite*
EOF

    print_success "Performance summary generated: $summary_file"
}

# Main profiling function
main() {
    echo "📊 GhostLink Performance Profiling"
    echo "=================================="

    setup_profile_dir

    print_status "Starting comprehensive performance profiling..."
    echo "Profile ID: $PROFILE_ID"
    echo "Results: $PROFILE_DIR"
    echo ""

    # Gather all performance data
    gather_system_info
    analyze_containers
    profile_application
    analyze_memory
    analyze_cpu
    analyze_disk_io
    analyze_network

    # Generate analysis and recommendations
    generate_recommendations
    generate_summary

    print_success "🎉 Performance profiling completed!"
    print_status "📊 Profile available in: $PROFILE_DIR"
    print_status "📋 Summary: $PROFILE_DIR/performance_summary.md"
    print_status "💡 Recommendations: $PROFILE_DIR/recommendations.txt"

    # Display quick insights
    echo ""
    echo "🔍 Quick Insights:"
    if [ -f "$PROFILE_DIR/system_info.txt" ]; then
        echo "- System cores: $(grep -c "processor" /proc/cpuinfo 2>/dev/null || sysctl -n hw.ncpu 2>/dev/null || echo "Unknown")"
        echo "- Memory: $(free -h | grep "^Mem:" | awk '{print $2}' 2>/dev/null || echo "Unknown")"
    fi

    if [ -f "$PROFILE_DIR/containers.txt" ] && command -v docker &> /dev/null; then
        container_count=$(docker ps | wc -l)
        echo "- Running containers: $((container_count - 1))"
    fi
}

# Run main function
main "$@"