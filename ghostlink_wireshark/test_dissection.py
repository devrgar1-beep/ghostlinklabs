#!/usr/bin/env python3
"""
Simple test for GhostLink packet dissection
"""

from protocol_dissector import GhostLinkDissector
from packet_capture import PacketGenerator

def test_dissection():
    """Test packet dissection"""
    print("🧪 Testing GhostLink packet dissection...")

    # Generate test packets
    packets = [
        PacketGenerator.generate_handshake_packet(),
        PacketGenerator.generate_heartbeat_packet(),
        PacketGenerator.generate_data_packet(b"Test data"),
    ]

    for i, packet_data in enumerate(packets):
        print(f"\n📦 Testing packet {i+1}")
        print(f"Raw data: {packet_data}")
        print(f"Length: {len(packet_data)} bytes")
        print(f"Raw data repr: {repr(packet_data)}")

        # Test dissection
        metadata = {
            'timestamp': 0,
            'source_ip': '127.0.0.1',
            'dest_ip': '127.0.0.1',
            'source_port': 12345,
            'dest_port': 9999
        }

        packet = GhostLinkDissector.dissect_packet(packet_data, metadata)

        # Debug magic header
        magic_bytes = packet_data[:9]
        print(f"Magic bytes: {magic_bytes} (len={len(magic_bytes)})")
        print(f"Magic repr: {repr(magic_bytes)}")
        print(f"Magic hex: {magic_bytes.hex()}")
        print(f"Expected: {GhostLinkDissector.MAGIC_HEADER}")
        print(f"Expected repr: {repr(GhostLinkDissector.MAGIC_HEADER)}")
        print(f"Expected hex: {GhostLinkDissector.MAGIC_HEADER.hex()}")
        print(f"Match: {magic_bytes == GhostLinkDissector.MAGIC_HEADER}")

        # Check byte by byte
        for i in range(9):
            print(f"  Byte {i}: got {magic_bytes[i]:02x}, expected {GhostLinkDissector.MAGIC_HEADER[i]:02x}")

        print(f"Valid: {packet.is_valid}")
        if packet.is_valid:
            print(f"Message Type: {packet.message_type_name}")
            print(f"Version: {packet.version}")
            print(f"Payload Length: {packet.payload_length}")
            print(f"Payload: {packet.payload}")
            print(f"Checksum: {packet.checksum}")
        else:
            print(f"Error: {packet.error_message}")

if __name__ == "__main__":
    test_dissection()
