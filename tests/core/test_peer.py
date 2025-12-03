#!/usr/bin/env python3
import json
import socket
import time

HOST = '127.0.0.1'
PORT = 7420

while True:
    try:
        with socket.create_connection((HOST, PORT), timeout=5) as s:
            hello_msg = {
                "type": "hello",
                "proto": "glp/0",
                "role": "peer",
                "mode": "ro"
            }
            s.sendall((json.dumps(hello_msg) + "\n").encode())

            legend_msg = {
                "type": "legend",
                "signals": [
                    {"id": "cpu_temp_c", "unit": "C", "tags": ["Δ"]},
                    {"id": "fault", "unit": "code", "tags": ["SCAR"]}
                ],
                "roi": [{"id": "rack.core", "expr": "zone=='core'"}]
            }
            s.sendall((json.dumps(legend_msg) + "\n").encode())

            while True:
                sample = {
                    "type": "sample",
                    "ts": time.time(),
                    "data": {
                        "zone": "core",
                        "cpu_temp_c": (35.0 + (time.time() % 10)),
                        "fault": None
                    }
                }
                s.sendall((json.dumps(sample) + "\n").encode())
                time.sleep(1)
    except (ConnectionError, OSError):
        time.sleep(2)
