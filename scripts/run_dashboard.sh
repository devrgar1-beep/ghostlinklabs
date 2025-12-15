#!/bin/bash
set -e

cd "$(dirname "${BASH_SOURCE[0]}")/../ui/dashboard"
python3 -m http.server 3000 --bind 127.0.0.1
