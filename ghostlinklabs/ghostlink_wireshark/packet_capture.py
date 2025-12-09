"""
GhostLink Packet Capture Module
Handles network packet capture for GhostLink protocol analysis
"""

import socket
import threading
import time
from typing import Callable, Optional, Dict, Any
import select

class PacketCapture:
    """Handles packet capture for GhostLink protocol analysis"""

    def __init__(self, port: int = 9999, interface: str = "0.0.0.0"):
        self.port = port
        self.interface = interface
        self.socket: Optional[socket.socket] = None
        self.is_capturing = False
        self.capture_thread: Optional[threading.Thread] = None
        self.packet_callback: Optional[Callable[[bytes, Dict[str, Any]], None]] = None

    def start_capture(self, callback: Callable[[bytes, Dict[str, Any]], None]) -> bool:
        """Start packet capture"""
        if self.is_capturing:
            return False

        try:
            # Create UDP socket for capture
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind((self.interface, self.port))

            self.packet_callback = callback
            self.is_capturing = True

            # Start capture thread
            self.capture_thread = threading.Thread(target=self._capture_loop, daemon=True)
            self.capture_thread.start()

            print(f"🎯 Started packet capture on {self.interface}:{self.port}")
            return True

        except Exception as e:
            print(f"❌ Failed to start capture: {e}")
            return False

    def stop_capture(self) -> bool:
        """Stop packet capture"""
        if not self.is_capturing:
            return False

        self.is_capturing = False

        if self.socket:
            self.socket.close()
            self.socket = None

        if self.capture_thread and self.capture_thread.is_alive():
            self.capture_thread.join(timeout=2)

        print("⏹️  Packet capture stopped")
        return True

    def _capture_loop(self):
        """Main packet capture loop"""
        while self.is_capturing and self.socket:
            try:
                # Use select for non-blocking receive
                ready = select.select([self.socket], [], [], 1.0)
                if ready[0] and self.socket in ready[0]:
                    data, addr = self.socket.recvfrom(65535)  # Max UDP packet size

                    # Create metadata
                    metadata = {
                        'timestamp': time.time(),
                        'source_ip': addr[0],
                        'source_port': addr[1],
                        'dest_ip': self.interface,
                        'dest_port': self.port
                    }

                    # Call callback if registered
                    if self.packet_callback:
                        self.packet_callback(data, metadata)

            except OSError:
                # Socket closed
                break
            except Exception as e:
                print(f"⚠️  Capture error: {e}")
                time.sleep(0.1)

class PacketGenerator:
    """Generates test GhostLink packets for testing"""

    @staticmethod
    def generate_handshake_packet(version: int = 1) -> bytes:
        """Generate a handshake packet"""
        import struct
        magic = b"GHOSTLINK"
        msg_type = 1  # HANDSHAKE
        payload = b"Hello GhostLink"
        payload_len = len(payload)
        checksum = 0x12345678  # Dummy checksum

        packet = magic + struct.pack('>HHI', version, msg_type, payload_len) + payload + struct.pack('>I', checksum)
        return packet

    @staticmethod
    def generate_heartbeat_packet() -> bytes:
        """Generate a heartbeat packet"""
        import struct
        magic = b"GHOSTLINK"
        version = 1
        msg_type = 2  # HEARTBEAT
        payload = b"PING"
        payload_len = len(payload)
        checksum = 0x87654321

        packet = magic + struct.pack('>HHI', version, msg_type, payload_len) + payload + struct.pack('>I', checksum)
        return packet

    @staticmethod
    def generate_data_packet(data: bytes) -> bytes:
        """Generate a data transfer packet"""
        import struct
        magic = b"GHOSTLINK"
        version = 1
        msg_type = 3  # DATA_TRANSFER
        payload_len = len(data)
        checksum = sum(data) & 0xFFFFFFFF  # Simple checksum

        packet = magic + struct.pack('>HHI', version, msg_type, payload_len) + data + struct.pack('>I', checksum)
        return packet
