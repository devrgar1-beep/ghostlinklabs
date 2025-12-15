#!/usr/bin/env bash
# Usage: enable-experimental.sh <API_KEY>
API_KEY=$1
if [ -z "$API_KEY" ]; then
  echo "Usage: $0 <API_KEY>"
  exit 2
fi
curl -s -X POST http://127.0.0.1:8765/extensions/experimental -H "Content-Type: application/json" -H "x-api-key: $API_KEY" -d '{"enable":true}' | jq
