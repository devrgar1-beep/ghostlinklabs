"""
GhostLink Protocol Dissector
Handles dissection of GhostLink protocol packets
"""

import struct
import time
from dataclasses import dataclass
from typing import Optional, Dict, Any, List
from enum import Enum

# GPU acceleration imports
try:
    import pyopencl as cl
    import numpy as np
    GPU_AVAILABLE = True
except ImportError:
    GPU_AVAILABLE = False
    print("⚠️  GPU acceleration not available - install pyopencl for GPU support")

class MessageType(Enum):
    """GhostLink message types"""
    HANDSHAKE = 1
    HEARTBEAT = 2
    DATA_TRANSFER = 3
    COMMAND = 4
    RESPONSE = 5
    EVOLUTION_UPDATE = 6
    CONSCIOUSNESS_SYNC = 7
    AGENT_ASSIGNMENT = 8
    HARDWARE_DISCOVERY = 9
    DARWIN_INTEGRATION = 10

@dataclass
class GhostLinkPacket:
    """Represents a dissected GhostLink packet"""
    timestamp: float
    source_ip: str
    dest_ip: str
    source_port: int
    dest_port: int
    magic: str
    version: int
    message_type: MessageType
    payload_length: int
    payload: bytes
    checksum: Optional[int]
    is_valid: bool = True
    error_message: Optional[str] = None

    @property
    def message_type_name(self) -> str:
        """Get human-readable message type name"""
        return self.message_type.name.replace('_', ' ').title()

    @property
    def size(self) -> int:
        """Get total packet size"""
        return 18 + self.payload_length + (4 if self.checksum else 0)

class GhostLinkDissector:
    """Dissects GhostLink protocol packets"""

    MAGIC_HEADER = b"GHOSTLINK"
    HEADER_SIZE = 17  # magic(9) + version(2) + msg_type(2) + payload_len(4)

    def __init__(self):
        self.gpu_context = None
        self.gpu_queue = None
        self.gpu_program = None
        self._init_gpu()

    def _init_gpu(self):
        """Initialize GPU acceleration if available"""
        if not GPU_AVAILABLE:
            return

        try:
            # Initialize OpenCL
            self.gpu_context = cl.create_some_context()
            self.gpu_queue = cl.CommandQueue(self.gpu_context)

            # GPU kernel for parallel packet validation
            kernel_code = """
            __kernel void validate_packets(
                __global const uchar* packets,
                __global const uint* packet_lengths,
                __global uint* results,
                const uint num_packets
            ) {
                int gid = get_global_id(0);
                if (gid >= num_packets) return;

                uint offset = 0;
                for (uint i = 0; i < gid; i++) {
                    offset += packet_lengths[i];
                }

                // Check magic header (GHOSTLINK = 71,72,79,83,84,76,73,78,75)
                if (packet_lengths[gid] < 9) {
                    results[gid] = 0; // Invalid
                    return;
                }

                bool magic_valid = true;
                uchar expected_magic[9] = {71,72,79,83,84,76,73,78,75};
                for (int i = 0; i < 9; i++) {
                    if (packets[offset + i] != expected_magic[i]) {
                        magic_valid = false;
                        break;
                    }
                }

                results[gid] = magic_valid ? 1 : 0;
            }

            __kernel void calculate_checksums(
                __global const uchar* packets,
                __global const uint* packet_lengths,
                __global uint* checksums,
                const uint num_packets
            ) {
                int gid = get_global_id(0);
                if (gid >= num_packets) return;

                uint offset = 0;
                for (uint i = 0; i < gid; i++) {
                    offset += packet_lengths[i];
                }

                // Simple checksum calculation
                uint checksum = 0;
                for (uint i = 0; i < packet_lengths[gid]; i++) {
                    checksum += packets[offset + i];
                }
                checksums[gid] = checksum & 0xFFFFFFFF;
            }
            """

            self.gpu_program = cl.Program(self.gpu_context, kernel_code).build()
            print("🎮 GPU acceleration initialized for packet dissection")

        except Exception as e:
            print(f"⚠️  GPU initialization failed: {e}")
            self.gpu_context = None

    @staticmethod
    def dissect_packet(data: bytes, metadata: Dict[str, Any]) -> GhostLinkPacket:
        """
        Dissect raw packet data into GhostLink packet structure

        Args:
            data: Raw packet payload
            metadata: Packet metadata (source_ip, dest_ip, ports, timestamp)

        Returns:
            GhostLinkPacket: Dissected packet
        """
        packet = GhostLinkPacket(
            timestamp=metadata.get('timestamp', time.time()),
            source_ip=metadata.get('source_ip', 'unknown'),
            dest_ip=metadata.get('dest_ip', 'unknown'),
            source_port=metadata.get('source_port', 0),
            dest_port=metadata.get('dest_port', 0),
            magic="",
            version=0,
            message_type=MessageType.HANDSHAKE,
            payload_length=0,
            payload=b"",
            checksum=None
        )

        try:
            if len(data) < GhostLinkDissector.HEADER_SIZE:
                packet.is_valid = False
                packet.error_message = f"Packet too short: {len(data)} bytes, minimum {GhostLinkDissector.HEADER_SIZE}"
                return packet

            # Check magic header
            magic = data[:9]
            if magic != GhostLinkDissector.MAGIC_HEADER:
                packet.is_valid = False
                packet.error_message = f"Invalid magic header: {magic}"
                return packet

            packet.magic = magic.decode('ascii')

            # Parse header fields
            offset = 9
            packet.version = struct.unpack('>H', data[offset:offset+2])[0]
            offset += 2

            msg_type_val = struct.unpack('>H', data[offset:offset+2])[0]
            try:
                packet.message_type = MessageType(msg_type_val)
            except ValueError:
                packet.is_valid = False
                packet.error_message = f"Unknown message type: {msg_type_val}"
                return packet
            offset += 2

            packet.payload_length = struct.unpack('>I', data[offset:offset+4])[0]
            offset += 4

            # Parse payload
            if packet.payload_length > 0:
                if len(data) < offset + packet.payload_length:
                    packet.is_valid = False
                    packet.error_message = f"Payload length mismatch: expected {packet.payload_length}, got {len(data) - offset}"
                    return packet
                packet.payload = data[offset:offset + packet.payload_length]
                offset += packet.payload_length

            # Parse checksum if present
            if len(data) >= offset + 4:
                packet.checksum = struct.unpack('>I', data[offset:offset+4])[0]

        except Exception as e:
            packet.is_valid = False
            packet.error_message = f"Dissection error: {str(e)}"

        return packet

    @staticmethod
    def format_packet_info(packet: GhostLinkPacket) -> str:
        """Format packet information for display"""
        if not packet.is_valid:
            return f"❌ INVALID: {packet.error_message}"

        info = [
            f"🔗 GHOSTLINK v{packet.version}",
            f"📨 {packet.message_type_name}",
            f"📏 {packet.payload_length} bytes",
            f"🌐 {packet.source_ip}:{packet.source_port} → {packet.dest_ip}:{packet.dest_port}"
        ]

        if packet.checksum is not None:
            info.append(f"🔒 Checksum: 0x{packet.checksum:08X}")

        return " | ".join(info)

    @staticmethod
    def format_packet_details(packet: GhostLinkPacket) -> str:
        """Format detailed packet information"""
        lines = [
            "=" * 60,
            f"GhostLink Packet Details",
            "=" * 60,
            f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(packet.timestamp))}",
            f"Source: {packet.source_ip}:{packet.source_port}",
            f"Destination: {packet.dest_ip}:{packet.dest_port}",
            f"Magic Header: {packet.magic}",
            f"Protocol Version: {packet.version}",
            f"Message Type: {packet.message_type_name} ({packet.message_type.value})",
            f"Payload Length: {packet.payload_length} bytes",
        ]

        if packet.payload:
            # Try to decode payload as UTF-8, fallback to hex
            try:
                payload_str = packet.payload.decode('utf-8')
                if len(payload_str) > 100:
                    payload_str = payload_str[:97] + "..."
                lines.append(f"Payload (UTF-8): {repr(payload_str)}")
            except UnicodeDecodeError:
                lines.append(f"Payload (Hex): {packet.payload.hex()}")

        if packet.checksum is not None:
            lines.append(f"Checksum: 0x{packet.checksum:08X}")

        if not packet.is_valid:
            lines.append(f"Error: {packet.error_message}")

        lines.append("=" * 60)
        return "\n".join(lines)

    def dissect_packets_batch_gpu(self, packets_data: List[bytes], metadata_list: List[Dict[str, Any]]) -> List[GhostLinkPacket]:
        """
        GPU-accelerated batch packet dissection for high-throughput processing

        Args:
            packets_data: List of raw packet payloads
            metadata_list: List of packet metadata dictionaries

        Returns:
            List of dissected GhostLinkPacket objects
        """
        if not self.gpu_context or not packets_data:
            # Fallback to CPU processing
            return [self.dissect_packet(data, meta) for data, meta in zip(packets_data, metadata_list)]

        try:
            num_packets = len(packets_data)

            # Prepare data for GPU
            max_packet_size = max(len(p) for p in packets_data)
            total_data_size = sum(len(p) for p in packets_data)

            # Create GPU buffers
            packet_lengths = np.array([len(p) for p in packets_data], dtype=np.uint32)
            flat_packets = np.zeros(total_data_size, dtype=np.uint8)

            # Flatten packet data
            offset = 0
            for packet in packets_data:
                packet_bytes = np.frombuffer(packet, dtype=np.uint8)
                flat_packets[offset:offset + len(packet)] = packet_bytes
                offset += len(packet)

            # GPU buffers
            gpu_packets = cl.Buffer(self.gpu_context, cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR, hostbuf=flat_packets)
            gpu_lengths = cl.Buffer(self.gpu_context, cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR, hostbuf=packet_lengths)
            gpu_results = cl.Buffer(self.gpu_context, cl.mem_flags.WRITE_ONLY, packet_lengths.nbytes)

            # Execute GPU kernel for validation
            if self.gpu_program:
                validate_kernel = self.gpu_program.validate_packets
                validate_kernel(self.gpu_queue, (num_packets,), None, gpu_packets, gpu_lengths, gpu_results, np.uint32(num_packets))

            # Get validation results
            validation_results = np.zeros(num_packets, dtype=np.uint32)
            cl.enqueue_copy(self.gpu_queue, validation_results, gpu_results)

            # Process valid packets
            results = []
            data_offset = 0

            for i, (data, meta, is_valid) in enumerate(zip(packets_data, metadata_list, validation_results)):
                if is_valid:
                    # Valid packet - dissect normally (CPU for complex parsing)
                    packet = self.dissect_packet(data, meta)
                else:
                    # Invalid packet
                    packet = GhostLinkPacket(
                        timestamp=meta.get('timestamp', time.time()),
                        source_ip=meta.get('source_ip', 'unknown'),
                        dest_ip=meta.get('dest_ip', 'unknown'),
                        source_port=meta.get('source_port', 0),
                        dest_port=meta.get('dest_port', 0),
                        magic="",
                        version=0,
                        message_type=MessageType.HANDSHAKE,
                        payload_length=0,
                        payload=b"",
                        checksum=None,
                        is_valid=False,
                        error_message="GPU validation failed"
                    )
                results.append(packet)

            return results

        except Exception as e:
            print(f"⚠️  GPU batch processing failed: {e}")
            # Fallback to CPU processing
            return [self.dissect_packet(data, meta) for data, meta in zip(packets_data, metadata_list)]

    def calculate_checksums_gpu(self, packets_data: List[bytes]) -> List[int]:
        """
        GPU-accelerated checksum calculation for multiple packets

        Args:
            packets_data: List of raw packet payloads

        Returns:
            List of calculated checksums
        """
        if not self.gpu_context or not packets_data:
            # CPU fallback
            return [sum(p) & 0xFFFFFFFF for p in packets_data]

        try:
            num_packets = len(packets_data)
            total_data_size = sum(len(p) for p in packets_data)

            # Prepare data
            packet_lengths = np.array([len(p) for p in packets_data], dtype=np.uint32)
            flat_packets = np.zeros(total_data_size, dtype=np.uint8)

            offset = 0
            for packet in packets_data:
                packet_bytes = np.frombuffer(packet, dtype=np.uint8)
                flat_packets[offset:offset + len(packet)] = packet_bytes
                offset += len(packet)

            # GPU buffers
            gpu_packets = cl.Buffer(self.gpu_context, cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR, hostbuf=flat_packets)
            gpu_lengths = cl.Buffer(self.gpu_context, cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR, hostbuf=packet_lengths)
            gpu_checksums = cl.Buffer(self.gpu_context, cl.mem_flags.WRITE_ONLY, packet_lengths.nbytes)

            # Execute GPU kernel
            if self.gpu_program:
                checksum_kernel = self.gpu_program.calculate_checksums
                checksum_kernel(self.gpu_queue, (num_packets,), None, gpu_packets, gpu_lengths, gpu_checksums, np.uint32(num_packets))

            # Get results
            checksums = np.zeros(num_packets, dtype=np.uint32)
            cl.enqueue_copy(self.gpu_queue, checksums, gpu_checksums)

            return checksums.tolist()

        except Exception as e:
            print(f"⚠️  GPU checksum calculation failed: {e}")
            return [sum(p) & 0xFFFFFFFF for p in packets_data]
