#!/bin/bash

# GhostLink Load Testing Script
# Comprehensive load testing for production deployment

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
TARGET_URL="${TARGET_URL:-http://localhost:3000}"
CONCURRENT_USERS="${CONCURRENT_USERS:-10}"
TOTAL_REQUESTS="${TOTAL_REQUESTS:-1000}"
RAMP_UP_TIME="${RAMP_UP_TIME:-30}"
TEST_DURATION="${TEST_DURATION:-60}"
RESULTS_DIR="./performance/results"

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

# Check if required tools are installed
check_dependencies() {
    local missing_tools=()

    if ! command -v curl &> /dev/null; then
        missing_tools+=("curl")
    fi

    if ! command -v jq &> /dev/null; then
        missing_tools+=("jq")
    fi

    if ! command -v bc &> /dev/null; then
        missing_tools+=("bc")
    fi

    # Check for load testing tools
    if ! command -v ab &> /dev/null && ! command -v siege &> /dev/null && ! command -v hey &> /dev/null; then
        print_warning "No load testing tool found (apache-bench, siege, or hey). Installing apache-bench..."
        if command -v apt-get &> /dev/null; then
            sudo apt-get update && sudo apt-get install -y apache2-utils
        elif command -v yum &> /dev/null; then
            sudo yum install -y httpd-tools
        elif command -v brew &> /dev/null; then
            brew install apache-bench
        else
            print_error "Cannot install apache-bench. Please install manually."
            exit 1
        fi
    fi

    if [ ${#missing_tools[@]} -ne 0 ]; then
        print_error "Missing required tools: ${missing_tools[*]}"
        exit 1
    fi

    print_success "All dependencies satisfied"
}

# Create results directory
setup_results_dir() {
    mkdir -p "$RESULTS_DIR"
    TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
    TEST_ID="load_test_${TIMESTAMP}"
    TEST_DIR="$RESULTS_DIR/$TEST_ID"
    mkdir -p "$TEST_DIR"

    print_success "Results directory created: $TEST_DIR"
}

# Test basic connectivity
test_connectivity() {
    print_status "Testing basic connectivity to $TARGET_URL..."

    if ! curl -s --max-time 10 "$TARGET_URL/health" > /dev/null; then
        print_error "Cannot connect to $TARGET_URL. Please ensure the service is running."
        exit 1
    fi

    print_success "Service is accessible"
}

# Run Apache Bench load test
run_ab_test() {
    local test_name=$1
    local url=$2
    local concurrency=$3
    local requests=$4

    print_status "Running Apache Bench test: $test_name"
    print_status "URL: $url"
    print_status "Concurrency: $concurrency, Requests: $requests"

    local output_file="$TEST_DIR/${test_name}.ab"

    ab -n "$requests" -c "$concurrency" -g "$TEST_DIR/${test_name}.tsv" \
       -H "Accept: application/json" \
       -H "User-Agent: GhostLink-LoadTest/1.0" \
       "$url" > "$output_file" 2>&1

    print_success "Apache Bench test completed: $test_name"
}

# Run Siege load test (if available)
run_siege_test() {
    if ! command -v siege &> /dev/null; then
        return
    fi

    local test_name=$1
    local url=$2
    local concurrency=$3
    local duration=$4

    print_status "Running Siege test: $test_name"
    print_status "URL: $url"
    print_status "Concurrency: $concurrency, Duration: ${duration}s"

    local output_file="$TEST_DIR/${test_name}.siege"

    siege -c "$concurrency" -t "${duration}s" \
          -H "Accept: application/json" \
          -H "User-Agent: GhostLink-LoadTest/1.0" \
          --log="$TEST_DIR/${test_name}.siege.log" \
          "$url" > "$output_file" 2>&1

    print_success "Siege test completed: $test_name"
}

# Run custom load test with curl
run_custom_load_test() {
    local test_name=$1
    local url=$2
    local concurrency=$3
    local duration=$4

    print_status "Running custom load test: $test_name"
    print_status "URL: $url"
    print_status "Concurrency: $concurrency, Duration: ${duration}s"

    local output_file="$TEST_DIR/${test_name}.custom"
    local start_time=$(date +%s)
    local end_time=$((start_time + duration))

    # Create temporary script for parallel execution
    cat > "$TEST_DIR/${test_name}_worker.sh" << EOF
#!/bin/bash
while [ \$(date +%s) -lt $end_time ]; do
    curl -s -w "%{http_code} %{time_total}\\n" \\
         -H "Accept: application/json" \\
         -H "User-Agent: GhostLink-LoadTest/1.0" \\
         -o /dev/null \\
         "$url" >> "$TEST_DIR/${test_name}_responses.txt"
done
EOF

    chmod +x "$TEST_DIR/${test_name}_worker.sh"

    # Start workers
    for i in $(seq 1 "$concurrency"); do
        "$TEST_DIR/${test_name}_worker.sh" &
    done

    # Wait for test duration
    sleep "$duration"

    # Kill workers
    pkill -f "${test_name}_worker.sh"

    # Analyze results
    local total_requests=$(wc -l < "$TEST_DIR/${test_name}_responses.txt")
    local success_count=$(grep "^200" "$TEST_DIR/${test_name}_responses.txt" | wc -l)
    local error_count=$(grep -v "^200" "$TEST_DIR/${test_name}_responses.txt" | wc -l)
    local avg_response_time=$(awk '{sum += $2} END {print sum/NR}' "$TEST_DIR/${test_name}_responses.txt" 2>/dev/null || echo "0")

    cat > "$output_file" << EOF
Custom Load Test Results: $test_name
=====================================
Target URL: $url
Concurrency: $concurrency
Duration: ${duration}s
Total Requests: $total_requests
Successful Requests: $success_count
Failed Requests: $error_count
Average Response Time: ${avg_response_time}s
Requests per Second: $(echo "scale=2; $total_requests / $duration" | bc 2>/dev/null || echo "0")
Success Rate: $(echo "scale=2; $success_count * 100 / $total_requests" | bc 2>/dev/null || echo "0")%
EOF

    print_success "Custom load test completed: $test_name"
}

# Test different endpoints
test_endpoints() {
    print_status "Testing different API endpoints..."

    # Health endpoint
    run_ab_test "health_endpoint" "$TARGET_URL/health" 5 100

    # API info endpoint
    run_ab_test "api_info" "$TARGET_URL/api/info" 5 100

    # Web interface
    run_ab_test "web_interface" "$TARGET_URL/" 5 100

    # AI status endpoint (if available)
    if curl -s "$TARGET_URL/api/ai/status" > /dev/null 2>&1; then
        run_ab_test "ai_status" "$TARGET_URL/api/ai/status" 5 100
    fi
}

# Run stress test
run_stress_test() {
    print_status "Running stress test..."

    # Gradually increase load
    local concurrency_levels=(1 5 10 25 50 100)

    for concurrency in "${concurrency_levels[@]}"; do
        print_status "Testing with $concurrency concurrent users..."
        run_ab_test "stress_c${concurrency}" "$TARGET_URL/health" "$concurrency" $((concurrency * 20))
        sleep 2
    done
}

# Run endurance test
run_endurance_test() {
    print_status "Running endurance test..."

    # Long duration test with moderate load
    run_siege_test "endurance" "$TARGET_URL/health" 10 300

    # Custom endurance test as fallback
    if ! command -v siege &> /dev/null; then
        run_custom_load_test "endurance" "$TARGET_URL/health" 10 300
    fi
}

# Analyze results
analyze_results() {
    print_status "Analyzing test results..."

    local summary_file="$TEST_DIR/summary.txt"

    cat > "$summary_file" << EOF
GhostLink Load Testing Summary
===============================
Test ID: $TEST_ID
Test Date: $(date)
Target URL: $TARGET_URL

Test Configuration:
- Concurrent Users: $CONCURRENT_USERS
- Total Requests: $TOTAL_REQUESTS
- Ramp Up Time: ${RAMP_UP_TIME}s
- Test Duration: ${TEST_DURATION}s

Results Summary:
EOF

    # Analyze each test result
    for result_file in "$TEST_DIR"/*.ab "$TEST_DIR"/*.siege "$TEST_DIR"/*.custom; do
        if [ -f "$result_file" ]; then
            echo "" >> "$summary_file"
            echo "=== $(basename "$result_file") ===" >> "$summary_file"

            if [[ "$result_file" == *.ab ]]; then
                # Parse Apache Bench results
                grep -E "(Concurrency Level|Time taken|Complete requests|Failed requests|Requests per second|Time per request)" "$result_file" >> "$summary_file" 2>/dev/null || echo "Parse error" >> "$summary_file"
            elif [[ "$result_file" == *.siege ]]; then
                # Parse Siege results
                grep -E "(Transactions:|Availability:|Elapsed time:|Data transferred:|Response time:|Transaction rate:|Throughput:|Concurrency:|Successful transactions:|Failed transactions:)" "$result_file" >> "$summary_file" 2>/dev/null || echo "Parse error" >> "$summary_file"
            elif [[ "$result_file" == *.custom ]]; then
                # Custom results are already formatted
                cat "$result_file" >> "$summary_file"
            fi
        fi
    done

    # Generate recommendations
    cat >> "$summary_file" << EOF

Recommendations:
===============

1. Performance Analysis:
   - Review response times and error rates
   - Check system resource usage during tests
   - Identify performance bottlenecks

2. Scaling Considerations:
   - Consider horizontal scaling if response times degrade significantly
   - Implement caching for frequently accessed data
   - Optimize database queries and connections

3. Monitoring:
   - Set up continuous performance monitoring
   - Configure alerts for performance degradation
   - Monitor resource usage patterns

4. Optimization Opportunities:
   - Implement connection pooling
   - Add request/response compression
   - Consider CDN for static assets
   - Optimize application code and database queries

Test completed successfully. Review detailed results in $TEST_DIR/
EOF

    print_success "Results analysis completed: $summary_file"
}

# Generate performance report
generate_report() {
    print_status "Generating performance report..."

    local report_file="$RESULTS_DIR/performance_report_${TIMESTAMP}.md"

    cat > "$report_file" << EOF
# GhostLink Performance Test Report

**Test ID:** $TEST_ID
**Date:** $(date)
**Target:** $TARGET_URL

## Test Configuration

- **Concurrent Users:** $CONCURRENT_USERS
- **Total Requests:** $TOTAL_REQUESTS
- **Ramp Up Time:** ${RAMP_UP_TIME}s
- **Test Duration:** ${TEST_DURATION}s

## Executive Summary

This report contains the results of comprehensive load testing performed on the GhostLink production deployment.

## Detailed Results

See the summary file: \`$TEST_DIR/summary.txt\`

## Recommendations

1. **Monitor Performance:** Set up continuous monitoring of key metrics
2. **Optimize Bottlenecks:** Address any identified performance issues
3. **Scale as Needed:** Implement auto-scaling based on load patterns
4. **Regular Testing:** Perform load testing after significant changes

## Files Generated

- **Summary:** \`$TEST_DIR/summary.txt\`
- **Detailed Results:** \`$TEST_DIR/\`
- **Raw Data:** Various .ab, .siege, and .custom files

---
*Generated by GhostLink Load Testing Suite*
EOF

    print_success "Performance report generated: $report_file"
}

# Main load testing function
main() {
    echo "🔥 GhostLink Load Testing Suite"
    echo "==============================="

    check_dependencies
    setup_results_dir
    test_connectivity

    print_status "Starting load tests..."
    echo "Target: $TARGET_URL"
    echo "Concurrent Users: $CONCURRENT_USERS"
    echo "Total Requests: $TOTAL_REQUESTS"
    echo "Results: $TEST_DIR"
    echo ""

    # Run different types of tests
    test_endpoints
    run_stress_test
    run_endurance_test

    # Analyze and report
    analyze_results
    generate_report

    print_success "🎉 Load testing completed!"
    print_status "📊 Results available in: $TEST_DIR"
    print_status "📋 Summary: $TEST_DIR/summary.txt"
    print_status "📄 Report: $RESULTS_DIR/performance_report_${TIMESTAMP}.md"

    # Display key metrics
    echo ""
    echo "📈 Key Metrics:"
    if [ -f "$TEST_DIR/summary.txt" ]; then
        grep -E "(Requests per second|Response time|Success rate)" "$TEST_DIR/summary.txt" 2>/dev/null || echo "Metrics parsing failed"
    fi
}

# Run main function
main "$@"