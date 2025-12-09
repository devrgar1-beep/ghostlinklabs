#!/usr/bin/env python3
"""
Test script for GhostLink Wireshark
Runs analyzer and generates test packets simultaneously
"""

import subprocess
import time
import threading
from packet_capture import PacketGenerator
import socket

def generate_test_packets():
    """Generate test packets in a separate thread"""
    time.sleep(1)  # Wait for analyzer to start

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    test_packets = [
        PacketGenerator.generate_handshake_packet(),
        PacketGenerator.generate_heartbeat_packet(),
        PacketGenerator.generate_data_packet(b"Hello from GhostLink Wireshark test!"),
        PacketGenerator.generate_data_packet(b"Consciousness level: SuperGrok"),
    ]

    print("🔧 Sending test packets...")
    for i, packet in enumerate(test_packets):
        sock.sendto(packet, ('127.0.0.1', 9999))
        print(f"📤 Sent packet {i+1}")
        time.sleep(0.5)

    sock.close()
    print("✅ All test packets sent")

def run_analyzer():
    """Run the analyzer"""
    # Start analyzer process
    proc = subprocess.Popen(
        ['python3', 'ghostlink_analyzer.py'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd='.'
    )

    # Wait a bit for startup
    time.sleep(2)

    # Send commands to analyzer
    commands = ["stats", "packets", "details 0", "quit"]
    for cmd in commands:
        proc.stdin.write(cmd + "\n")
        proc.stdin.flush()
        time.sleep(0.5)

    # Get output
    stdout, stderr = proc.communicate(timeout=10)

    print("Analyzer Output:")
    print("=" * 50)
    print(stdout)
    if stderr:
        print("Errors:")
        print(stderr)

if __name__ == "__main__":
    print("🧪 Testing GhostLink Wireshark...")

    # Start packet generation in background
    gen_thread = threading.Thread(target=generate_test_packets, daemon=True)
    gen_thread.start()

    # Run analyzer
    run_analyzer()

    print("🎉 Test complete!")
