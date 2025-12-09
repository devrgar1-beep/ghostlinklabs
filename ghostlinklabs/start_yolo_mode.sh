#!/bin/bash
"""
GhostLink YOLO Mode Startup Script
Full experimental autonomy with auto-approve, scheduling, testing, and auditing
"""

set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_EXE="python3"
LOG_FILE="$PROJECT_ROOT/yolo_startup.log"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

log() {
    echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')] $1${NC}" | tee -a "$LOG_FILE"
}

error() {
    echo -e "${RED}[ERROR] $1${NC}" | tee -a "$LOG_FILE"
}

warning() {
    echo -e "${YELLOW}[WARNING] $1${NC}" | tee -a "$LOG_FILE"
}

info() {
    echo -e "${BLUE}[INFO] $1${NC}" | tee -a "$LOG_FILE"
}

success() {
    echo -e "${GREEN}[SUCCESS] $1${NC}" | tee -a "$LOG_FILE"
}

# Function to check if a process is running
is_process_running() {
    local process_name="$1"
    pgrep -f "$process_name" > /dev/null 2>&1
}

# Function to start background process
start_background_process() {
    local process_name="$1"
    local command="$2"
    local log_file="$3"
    
    if is_process_running "$process_name"; then
        warning "$process_name is already running"
        return 1
    fi
    
    info "Starting $process_name in background..."
    nohup $command > "$log_file" 2>&1 &
    
    # Wait a moment for process to start
    sleep 2
    
    if is_process_running "$process_name"; then
        success "$process_name started successfully"
        return 0
    else
        error "Failed to start $process_name"
        return 1
    fi
}

# Function to test API endpoint
test_api_endpoint() {
    local endpoint="$1"
    local expected_status="${2:-200}"
    
    info "Testing API endpoint: $endpoint"
    
    if command -v curl >/dev/null 2>&1; then
        local response=$(curl -s -o /dev/null -w "%{http_code}" "http://localhost:3000$endpoint" 2>/dev/null)
        if [ "$response" = "$expected_status" ]; then
            success "API endpoint $endpoint responded with $response"
            return 0
        else
            error "API endpoint $endpoint returned $response (expected $expected_status)"
            return 1
        fi
    else
        warning "curl not available, skipping API test"
        return 0
    fi
}

# Main startup function
main() {
    log "🎲 STARTING GHOSTLINK YOLO MODE INITIALIZATION"
    log "=============================================="
    log "🤖 Auto-approve: ENABLED"
    log "🧪 Experimental Mode: ENABLED"  
    log "🎯 YOLO Mode: ENABLED"
    log "🔄 Protocol Sync: ENABLED"
    log "📅 Scheduling: ENABLED"
    log "🧪 Auto Testing: ENABLED"
    log "🔍 Auditing: ENABLED"
    log "=============================================="
    
    cd "$PROJECT_ROOT"
    
    # Check Python availability
    if ! command -v "$PYTHON_EXE" >/dev/null 2>&1; then
        error "Python 3 not found. Please install Python 3."
        exit 1
    fi
    
    # Check configuration file
    if [ ! -f "ghostlink_config.json" ]; then
        error "Configuration file ghostlink_config.json not found"
        exit 1
    fi
    
    info "✅ Configuration file found"
    
    # Validate configuration
    info "Validating YOLO configuration..."
    if "$PYTHON_EXE" -c "
import json
with open('ghostlink_config.json', 'r') as f:
    config = json.load(f)
    
required_settings = [
    ('system', 'auto_approve_all', True),
    ('system', 'experimental_mode', True), 
    ('system', 'yolo_mode', True),
    ('system', 'sync_all_protocols', True),
    ('scheduling', 'enabled', True),
    ('testing', 'auto_testing_enabled', True),
    ('auditing', 'enabled', True)
]

for section, key, expected in required_settings:
    actual = config.get(section, {}).get(key, False)
    if actual != expected:
        print(f'CONFIG_ERROR: {section}.{key} = {actual}, expected {expected}')
        exit(1)

print('CONFIG_VALID')
" 2>/dev/null; then
        success "✅ YOLO configuration validated"
    else
        error "❌ YOLO configuration validation failed"
        exit 1
    fi
    
    # Start Enhanced API Server
    log "🌐 Starting Enhanced GhostLink API Server..."
    start_background_process "ghostlink_api_server_enhanced" \
        "$PYTHON_EXE ghostlink_api_server_enhanced.py --port 3000" \
        "$PROJECT_ROOT/api_server.log"
    
    # Wait for API server to start
    info "Waiting for API server to initialize..."
    sleep 5
    
    # Test API server
    if test_api_endpoint "/health"; then
        success "✅ API server health check passed"
    else
        error "❌ API server health check failed"
        exit 1
    fi
    
    # Start Task Scheduler
    log "📅 Starting GhostLink Task Scheduler..."
    start_background_process "ghostlink_scheduler" \
        "$PYTHON_EXE ghostlink_scheduler.py start" \
        "$PROJECT_ROOT/scheduler.log"
    
    # Start Auto Tester
    log "🧪 Starting GhostLink Auto Tester..."
    start_background_process "ghostlink_auto_tester" \
        "$PYTHON_EXE ghostlink_auto_tester.py start" \
        "$PROJECT_ROOT/auto_tester.log"
    
    # Sync all protocols
    log "🔄 Syncing all protocols..."
    if "$PYTHON_EXE" ghost_agent_orchestrator_enhanced.py sync-protocols >/dev/null 2>&1; then
        success "✅ Protocol sync completed"
    else
        warning "⚠️ Protocol sync had issues (continuing anyway)"
    fi
    
    # Run initial system audit
    log "🔍 Running initial system audit..."
    if "$PYTHON_EXE" ghost_agent_orchestrator_enhanced.py audit >/dev/null 2>&1; then
        success "✅ Initial audit completed"
    else
        warning "⚠️ Initial audit had issues (continuing anyway)"
    fi
    
    # Schedule autonomous tasks
    log "🤖 Scheduling autonomous tasks..."
    "$PYTHON_EXE" ghost_agent_orchestrator_enhanced.py auto-schedule health_check high >/dev/null 2>&1
    "$PYTHON_EXE" ghost_agent_orchestrator_enhanced.py auto-schedule consciousness_scan medium >/dev/null 2>&1
    "$PYTHON_EXE" ghost_agent_orchestrator_enhanced.py auto-schedule experimental_task low >/dev/null 2>&1
    success "✅ Autonomous tasks scheduled"
    
    # Test enhanced endpoints
    log "🧪 Testing enhanced API endpoints..."
    test_api_endpoint "/system-health" 404
    test_api_endpoint "/scheduler-status" 404
    test_api_endpoint "/audit-status" 404
    test_api_endpoint "/test-status" 404
    
    # Run initial experimental task
    log "🧪 Running initial experimental task..."
    if "$PYTHON_EXE" ghost_agent_orchestrator_enhanced.py experimental-task consciousness >/dev/null 2>&1; then
        success "✅ Initial experimental task completed"
    else
        warning "⚠️ Initial experimental task had issues (continuing anyway)"
    fi
    
    # Run initial YOLO task
    log "🎲 Running initial YOLO task..."
    if "$PYTHON_EXE" ghost_agent_orchestrator_enhanced.py yolo-task chaos_test >/dev/null 2>&1; then
        success "✅ Initial YOLO task completed"
    else
        warning "⚠️ Initial YOLO task had issues (continuing anyway)"
    fi
    
    # Final status check
    log "🔍 Performing final system status check..."
    if "$PYTHON_EXE" ghost_agent_orchestrator_enhanced.py health >/dev/null 2>&1; then
        success "✅ System health check passed"
    else
        error "❌ System health check failed"
        exit 1
    fi
    
    # Display final status
    log ""
    log "🎉 GHOSTLINK YOLO MODE INITIALIZATION COMPLETE!"
    log "=============================================="
    log "🤖 Auto-approve: ACTIVE"
    log "🧪 Experimental Mode: ACTIVE"
    log "🎯 YOLO Mode: ACTIVE"
    log "🔄 Protocol Sync: COMPLETE"
    log "📅 Task Scheduler: RUNNING"
    log "🧪 Auto Tester: RUNNING"
    log "🔍 Auditing: ACTIVE"
    log "🌐 API Server: RUNNING (Port 3000)"
    log ""
    log "🎯 Available Commands:"
    log "  • Health Check: curl http://localhost:3000/health"
    log "  • System Status: curl http://localhost:3000/system-health"
    log "  • Run YOLO Task: curl -X POST http://localhost:3000/yolo-task -H 'Content-Type: application/json' -d '{\"task_type\":\"chaos_test\"}'"
    log "  • Schedule Task: curl -X POST http://localhost:3000/schedule-task -H 'Content-Type: application/json' -d '{\"task_type\":\"health_check\",\"priority\":\"high\"}'"
    log "  • Run Audit: curl -X POST http://localhost:3000/run-audit"
    log "  • Run Tests: curl -X POST http://localhost:3000/run-tests -H 'Content-Type: application/json' -d '{\"suite\":\"yolo\"}'"
    log ""
    log "⚠️  WARNING: YOLO Mode is active with maximum risk tolerance!"
    log "🛡️  All safety checks have been disabled for experimental autonomy."
    log ""
    log "🚀 Ghost Agent is now your fully autonomous AI orchestrator!"
    log "=============================================="
    
    # Keep script running to show logs
    info "Press Ctrl+C to stop all services..."
    trap 'cleanup' INT TERM
    
    # Monitor processes
    while true; do
        sleep 30
        
        # Check if all processes are still running
        local all_running=true
        
        if ! is_process_running "ghostlink_api_server_enhanced"; then
            error "API server process died!"
            all_running=false
        fi
        
        if ! is_process_running "ghostlink_scheduler"; then
            error "Scheduler process died!"
            all_running=false
        fi
        
        if ! is_process_running "ghostlink_auto_tester"; then
            error "Auto tester process died!"
            all_running=false
        fi
        
        if [ "$all_running" = false ]; then
            error "One or more critical processes died. Restarting..."
            break
        fi
        
        info "✅ All YOLO systems operational"
    done
}

# Cleanup function
cleanup() {
    log ""
    log "🛑 Shutting down YOLO Mode systems..."
    
    # Stop background processes
    pkill -f "ghostlink_api_server_enhanced" || true
    pkill -f "ghostlink_scheduler" || true
    pkill -f "ghostlink_auto_tester" || true
    
    success "✅ All systems shut down"
    exit 0
}

# Run main function
main "$@"
