#!/usr/bin/env bash
set -euo pipefail

OUT="/tmp/ghostlink_capture.pcap"
COUNT=500

echo "This script requires sudo to capture packets. You will be prompted for your password."
sudo tcpdump -i any -s 0 -c "$COUNT" -w "$OUT"
echo "Capture saved to: $OUT"
echo "To analyze (local): tcpdump -nn -r $OUT | head -n 200"
