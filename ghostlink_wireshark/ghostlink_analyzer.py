#!/usr/bin/env python3
"""
GhostLink Wireshark - Custom Network Protocol Analyzer
A specialized packet analyzer for GhostLink protocol dissection and analysis
"""

import argparse
import curses
import threading
import time
from collections import deque
from typing import List, Deque

from protocol_dissector import GhostLinkDissector, GhostLinkPacket
from packet_capture import PacketCapture, PacketGenerator

class GhostLinkAnalyzer:
    """Main GhostLink protocol analyzer"""

    def __init__(self, port: int = 9999, max_packets: int = 1000, use_gpu: bool = True):
        self.port = port
        self.max_packets = max_packets
        self.packets: Deque[GhostLinkPacket] = deque(maxlen=max_packets)
        self.capture = PacketCapture(port=port)
        self.dissector = GhostLinkDissector()  # GPU-accelerated dissector
        self.is_running = False
        self.use_gpu = use_gpu
        self.batch_buffer = []  # Buffer for batch GPU processing
        self.batch_metadata = []  # Corresponding metadata
        self.batch_size = 32  # Process packets in batches of 32

        self.stats = {
            'total_packets': 0,
            'valid_packets': 0,
            'invalid_packets': 0,
            'message_types': {},
            'start_time': time.time(),
            'gpu_packets': 0,
            'cpu_packets': 0
        }

    def start_capture(self) -> bool:
        """Start packet capture"""
        def packet_handler(data: bytes, metadata: dict):
            if self.use_gpu and self.dissector.gpu_context:
                # Buffer packets for batch GPU processing
                self.batch_buffer.append(data)
                self.batch_metadata.append(metadata)

                # Process batch when buffer is full
                if len(self.batch_buffer) >= self.batch_size:
                    self._process_batch_gpu()
            else:
                # CPU processing for single packets or when GPU unavailable
                packet = self.dissector.dissect_packet(data, metadata)
                self.packets.append(packet)
                self._update_stats(packet)
                self.stats['cpu_packets'] += 1

        self.is_running = True
        success = self.capture.start_capture(packet_handler)

        if success and self.use_gpu and self.dissector.gpu_context:
            print("🎮 GPU acceleration enabled for packet dissection")
        elif self.use_gpu:
            print("⚠️  GPU acceleration requested but not available - using CPU")

        return success

    def _process_batch_gpu(self):
        """Process buffered packets using GPU acceleration"""
        if not self.batch_buffer:
            return

        try:
            # Process batch with GPU
            batch_packets = self.dissector.dissect_packets_batch_gpu(
                self.batch_buffer, self.batch_metadata
            )

            # Add to packet queue and update stats
            for packet in batch_packets:
                self.packets.append(packet)
                self._update_stats(packet)

            self.stats['gpu_packets'] += len(batch_packets)

        except Exception as e:
            print(f"⚠️  GPU batch processing failed: {e}")
            # Fallback to CPU processing
            for data, meta in zip(self.batch_buffer, self.batch_metadata):
                packet = self.dissector.dissect_packet(data, meta)
                self.packets.append(packet)
                self._update_stats(packet)
                self.stats['cpu_packets'] += 1

        # Clear buffers
        self.batch_buffer.clear()
        self.batch_metadata.clear()

    def flush_batch(self):
        """Flush any remaining packets in the batch buffer"""
        if self.batch_buffer:
            self._process_batch_gpu()

    def stop_capture(self):
        """Stop packet capture"""
        self.is_running = False

        # Flush any remaining packets in batch buffer
        self.flush_batch()

        self.capture.stop_capture()

    def _update_stats(self, packet: GhostLinkPacket):
        """Update capture statistics"""
        self.stats['total_packets'] += 1
        if packet.is_valid:
            self.stats['valid_packets'] += 1
            msg_type = packet.message_type.name
            self.stats['message_types'][msg_type] = self.stats['message_types'].get(msg_type, 0) + 1
        else:
            self.stats['invalid_packets'] += 1

    def get_stats(self) -> dict:
        """Get current statistics"""
        stats = self.stats.copy()
        stats['uptime'] = time.time() - stats['start_time']
        stats['packets_per_second'] = stats['total_packets'] / max(stats['uptime'], 1)
        return stats

    def get_recent_packets(self, count: int = 10) -> List[GhostLinkPacket]:
        """Get most recent packets"""
        return list(self.packets)[-count:]

class CLIAnalyzer:
    """Command-line interface for the analyzer"""

    def __init__(self, analyzer: GhostLinkAnalyzer):
        self.analyzer = analyzer

    def run(self):
        """Run the CLI analyzer"""
        print("🔍 GhostLink Wireshark - Protocol Analyzer")
        print("=" * 50)
        print(f"📡 Listening on port {self.analyzer.port}")
        print("Commands: 'stats', 'packets', 'details <n>', 'generate', 'quit'")
        print("Press Ctrl+C to stop capture")
        print()

        if not self.analyzer.start_capture():
            print("❌ Failed to start capture")
            return

        try:
            while self.analyzer.is_running:
                cmd = input("ghostlink-wireshark> ").strip().lower()
                if cmd == 'quit':
                    break
                elif cmd == 'stats':
                    self.show_stats()
                elif cmd == 'packets':
                    self.show_packets()
                elif cmd.startswith('details '):
                    try:
                        idx = int(cmd.split()[1])
                        self.show_packet_details(idx)
                    except (ValueError, IndexError):
                        print("❌ Invalid packet index")
                elif cmd == 'generate':
                    self.generate_test_packets()
                else:
                    print("❓ Unknown command. Try: stats, packets, details <n>, generate, quit")
        except KeyboardInterrupt:
            print("\n⏹️  Stopping capture...")
        finally:
            self.analyzer.stop_capture()

    def show_stats(self):
        """Show capture statistics"""
        stats = self.analyzer.get_stats()
        print("\n📊 Capture Statistics")
        print("-" * 30)
        print(f"Total Packets: {stats['total_packets']}")
        print(f"Valid Packets: {stats['valid_packets']}")
        print(f"Invalid Packets: {stats['invalid_packets']}")
        print(".2f")
        print(".1f")

        # GPU statistics
        if 'gpu_packets' in stats and 'cpu_packets' in stats:
            gpu_packets = stats.get('gpu_packets', 0)
            cpu_packets = stats.get('cpu_packets', 0)
            total_processed = gpu_packets + cpu_packets
            if total_processed > 0:
                gpu_percentage = (gpu_packets / total_processed) * 100
                print(".1f")
                print(f"GPU Processed: {gpu_packets}")
                print(f"CPU Processed: {cpu_packets}")

        print("\n📋 Message Types:")
        for msg_type, count in stats['message_types'].items():
            print(f"  {msg_type}: {count}")
        print()

    def show_packets(self):
        """Show recent packets"""
        packets = self.analyzer.get_recent_packets(20)
        if not packets:
            print("📭 No packets captured yet")
            return

        print("\n📦 Recent Packets")
        print("-" * 80)
        print("<10")
        print("-" * 80)
        for i, packet in enumerate(packets):
            status = "✅" if packet.is_valid else "❌"
            info = GhostLinkDissector.format_packet_info(packet)
            print("2d")
        print()

    def show_packet_details(self, idx: int):
        """Show detailed packet information"""
        packets = self.analyzer.get_recent_packets(100)
        if 0 <= idx < len(packets):
            packet = packets[-(idx+1)]  # Most recent is index 0
            details = GhostLinkDissector.format_packet_details(packet)
            print(details)
        else:
            print(f"❌ Packet index {idx} not found")

    def generate_test_packets(self):
        """Generate test packets for testing"""
        print("🔧 Generating test packets...")

        # Generate some test packets
        test_packets = [
            PacketGenerator.generate_handshake_packet(),
            PacketGenerator.generate_heartbeat_packet(),
            PacketGenerator.generate_data_packet(b"Test data payload"),
        ]

        # Send them to ourselves for testing
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        for packet in test_packets:
            sock.sendto(packet, ('127.0.0.1', self.analyzer.port))
            time.sleep(0.1)
        sock.close()

        print("✅ Test packets sent")
        time.sleep(1)  # Wait for processing

def main():
    parser = argparse.ArgumentParser(description="GhostLink Wireshark - Protocol Analyzer")
    parser.add_argument('--port', type=int, default=9999, help='Port to listen on (default: 9999)')
    parser.add_argument('--max-packets', type=int, default=1000, help='Maximum packets to store (default: 1000)')
    parser.add_argument('--cli', action='store_true', help='Run in CLI mode (default)')
    parser.add_argument('--generate-test', action='store_true', help='Generate test packets and exit')
    parser.add_argument('--no-gpu', action='store_true', help='Disable GPU acceleration')

    args = parser.parse_args()

    use_gpu = not args.no_gpu
    analyzer = GhostLinkAnalyzer(port=args.port, max_packets=args.max_packets, use_gpu=use_gpu)

    if args.generate_test:
        # Generate test packets and send to analyzer
        print("🔧 Generating test packets...")
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        test_packets = [
            PacketGenerator.generate_handshake_packet(),
            PacketGenerator.generate_heartbeat_packet(),
            PacketGenerator.generate_data_packet(b"Hello from GhostLink test!"),
        ]

        for packet in test_packets:
            sock.sendto(packet, ('127.0.0.1', args.port))
            time.sleep(0.1)

        sock.close()
        print("✅ Test packets sent to localhost")
        return

    # Start CLI analyzer
    cli = CLIAnalyzer(analyzer)
    cli.run()

if __name__ == "__main__":
    main()
