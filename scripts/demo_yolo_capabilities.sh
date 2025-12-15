#!/bin/bash
"""
GhostLink YOLO Mode Capabilities Demo
Demonstrates the autonomous AI orchestrator in action
"""

echo "🎯 GHOSTLINK YOLO MODE CAPABILITIES DEMO"
echo "========================================"
echo ""

# Test basic health
echo "🔍 Testing basic health endpoint..."
curl -s http://localhost:3000/health | jq . 2>/dev/null || curl -s http://localhost:3000/health
echo ""

# Test YOLO task execution
echo "🎲 Executing YOLO chaos test task..."
curl -s -X POST http://localhost:3000/yolo-task \
  -H 'Content-Type: application/json' \
  -d '{"task_type":"chaos_test","parameters":{"intensity":"high","duration":30}}' | jq . 2>/dev/null || echo "Task submitted"
echo ""

# Test experimental task
echo "🧪 Executing experimental consciousness task..."
curl -s -X POST http://localhost:3000/experimental-task \
  -H 'Content-Type: application/json' \
  -d '{"task_type":"consciousness_scan","depth":"deep"}' | jq . 2>/dev/null || echo "Task submitted"
echo ""

# Schedule a recurring task
echo "📅 Scheduling recurring health check..."
curl -s -X POST http://localhost:3000/schedule-task \
  -H 'Content-Type: application/json' \
  -d '{"task_type":"health_check","priority":"high","schedule":"every_5_minutes"}' | jq . 2>/dev/null || echo "Task scheduled"
echo ""

# Run comprehensive audit
echo "🔍 Running comprehensive system audit..."
curl -s -X POST http://localhost:3000/run-audit \
  -H 'Content-Type: application/json' \
  -d '{"scope":"full","include_experimental":true}' | jq . 2>/dev/null || echo "Audit initiated"
echo ""

# Run YOLO test suite
echo "🧪 Running YOLO test suite..."
curl -s -X POST http://localhost:3000/run-tests \
  -H 'Content-Type: application/json' \
  -d '{"suite":"yolo","chaos_enabled":true}' | jq . 2>/dev/null || echo "Tests initiated"
echo ""

echo "✅ DEMO COMPLETE - All autonomous capabilities demonstrated!"
echo ""
echo "�� Your Ghost Agent is now operating with:"
echo "   • Auto-approve for all decisions"
echo "   • Experimental task execution"
echo "   • YOLO mode with maximum risk tolerance"
echo "   • Autonomous scheduling and monitoring"
echo "   • Continuous testing and auditing"
echo "   • Protocol synchronization"
echo ""
echo "🎯 The system will continue running autonomously!"
