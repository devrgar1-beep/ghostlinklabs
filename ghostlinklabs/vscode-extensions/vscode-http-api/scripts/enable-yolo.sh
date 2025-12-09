#!/usr/bin/env bash
# Usage: enable-yolo.sh <API_KEY> [true|false]
API_KEY=$1
EN=${2:-true}
if [ -z "$API_KEY" ]; then
  echo "Usage: $0 <API_KEY> [true|false]"
  exit 2
fi
curl -s -X POST http://127.0.0.1:8765/yolo -H "Content-Type: application/json" -H "x-api-key: $API_KEY" -d "{ \"enable\": $EN }" | jq
