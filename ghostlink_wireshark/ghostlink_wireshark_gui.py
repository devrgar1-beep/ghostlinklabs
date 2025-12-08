#!/usr/bin/env python3
"""
GhostLink Wireshark GUI - Graphical Packet Analyzer
A Wireshark-like GUI for GhostLink protocol analysis
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import time
from typing import List

from protocol_dissector import GhostLinkDissector, GhostLinkPacket
from packet_capture import PacketCapture, PacketGenerator
from ghostlink_analyzer import GhostLinkAnalyzer

class GhostLinkWiresharkGUI:
    """Graphical interface for GhostLink packet analysis"""

    def __init__(self, root):
        self.root = root
        self.root.title("GhostLink Wireshark - Protocol Analyzer")
        self.root.geometry("1200x800")

        self.analyzer = GhostLinkAnalyzer()
        self.is_capturing = False

        self.setup_ui()
        self.update_timer = None
        self.start_update_timer()

    def setup_ui(self):
        """Setup the user interface"""
        # Main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Toolbar
        toolbar = ttk.Frame(main_frame)
        toolbar.pack(fill=tk.X, pady=(0, 5))

        # Control buttons
        self.start_btn = ttk.Button(toolbar, text="▶ Start Capture", command=self.start_capture)
        self.start_btn.pack(side=tk.LEFT, padx=(0, 5))

        self.stop_btn = ttk.Button(toolbar, text="⏹ Stop Capture", command=self.stop_capture, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=(0, 5))

        ttk.Button(toolbar, text="🔧 Generate Test", command=self.generate_test_packets).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(toolbar, text="📊 Statistics", command=self.show_stats).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(toolbar, text="🧹 Clear", command=self.clear_packets).pack(side=tk.LEFT, padx=(0, 5))

        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready - Not capturing")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.pack(fill=tk.X, pady=(0, 5))

        # Main content area
        content = ttk.PanedWindow(main_frame, orient=tk.VERTICAL)
        content.pack(fill=tk.BOTH, expand=True)

        # Packet list (top pane)
        packet_frame = ttk.Frame(content)
        content.add(packet_frame, weight=1)

        # Packet listbox with scrollbar
        list_frame = ttk.Frame(packet_frame)
        list_frame.pack(fill=tk.BOTH, expand=True)

        self.packet_listbox = tk.Listbox(list_frame, font=("Courier", 10))
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.packet_listbox.yview)
        self.packet_listbox.configure(yscrollcommand=scrollbar.set)

        self.packet_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.packet_listbox.bind('<<ListboxSelect>>', self.on_packet_select)

        # Packet details (bottom pane)
        details_frame = ttk.Frame(content)
        content.add(details_frame, weight=1)

        ttk.Label(details_frame, text="Packet Details:").pack(anchor=tk.W)
        self.details_text = scrolledtext.ScrolledText(details_frame, height=15, font=("Courier", 9))
        self.details_text.pack(fill=tk.BOTH, expand=True)

    def start_capture(self):
        """Start packet capture"""
        if self.analyzer.start_capture():
            self.is_capturing = True
            self.start_btn.config(state=tk.DISABLED)
            self.stop_btn.config(state=tk.NORMAL)
            self.status_var.set("🎯 Capturing packets...")
        else:
            messagebox.showerror("Error", "Failed to start packet capture")

    def stop_capture(self):
        """Stop packet capture"""
        self.analyzer.stop_capture()
        self.is_capturing = False
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.status_var.set("⏹ Capture stopped")

    def generate_test_packets(self):
        """Generate test packets"""
        if not self.is_capturing:
            messagebox.showwarning("Warning", "Start capture first to see test packets")
            return

        # Generate test packets in a thread
        def generate():
            import socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

            test_packets = [
                PacketGenerator.generate_handshake_packet(),
                PacketGenerator.generate_heartbeat_packet(),
                PacketGenerator.generate_data_packet(b"GUI Test Data"),
                PacketGenerator.generate_data_packet(b"Consciousness sync payload"),
            ]

            for packet in test_packets:
                sock.sendto(packet, ('127.0.0.1', self.analyzer.port))
                time.sleep(0.2)

            sock.close()

        threading.Thread(target=generate, daemon=True).start()

    def show_stats(self):
        """Show capture statistics"""
        stats = self.analyzer.get_stats()

        stats_text = f"""Capture Statistics

Total Packets: {stats['total_packets']}
Valid Packets: {stats['valid_packets']}
Invalid Packets: {stats['invalid_packets']}
Packets/Second: {stats['packets_per_second']:.1f}
Uptime: {stats['uptime']:.1f} seconds

Message Types:
"""

        for msg_type, count in stats['message_types'].items():
            stats_text += f"  {msg_type}: {count}\n"

        messagebox.showinfo("Statistics", stats_text)

    def clear_packets(self):
        """Clear packet list"""
        self.analyzer.packets.clear()
        self.analyzer.stats = {
            'total_packets': 0,
            'valid_packets': 0,
            'invalid_packets': 0,
            'message_types': {},
            'start_time': time.time()
        }
        self.update_packet_list()

    def update_packet_list(self):
        """Update the packet list display"""
        self.packet_listbox.delete(0, tk.END)

        packets = list(self.analyzer.packets)
        for i, packet in enumerate(packets):
            timestamp = time.strftime("%H:%M:%S", time.localtime(packet.timestamp))
            status = "✅" if packet.is_valid else "❌"
            info = f"{timestamp} {status} {packet.message_type_name} {packet.source_ip}:{packet.source_port}"
            self.packet_listbox.insert(tk.END, f"{i+1:4d} {info}")

        # Update status
        stats = self.analyzer.get_stats()
        if self.is_capturing:
            self.status_var.set(f"🎯 Capturing - {stats['total_packets']} packets")
        else:
            self.status_var.set(f"⏹ Stopped - {stats['total_packets']} packets")

    def on_packet_select(self, event):
        """Handle packet selection"""
        selection = self.packet_listbox.curselection()
        if selection:
            idx = selection[0]
            packets = list(self.analyzer.packets)
            if idx < len(packets):
                packet = packets[idx]
                details = GhostLinkDissector.format_packet_details(packet)
                self.details_text.delete(1.0, tk.END)
                self.details_text.insert(tk.END, details)

    def start_update_timer(self):
        """Start timer to update display"""
        self.update_packet_list()
        self.update_timer = self.root.after(1000, self.start_update_timer)  # Update every second

    def on_closing(self):
        """Handle window closing"""
        if self.update_timer:
            self.root.after_cancel(self.update_timer)
        self.analyzer.stop_capture()
        self.root.destroy()

def main():
    root = tk.Tk()
    app = GhostLinkWiresharkGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()
