"""Minimal heartbeat helper used by upgrade scripts and monitors."""

import time


class Heartbeat:
    def __init__(self, interval: int = 7):
        self.interval = interval
        self.last = time.time()

    def ping(self):
        self.last = time.time()
        return self.last

    def status(self):
        return {"interval": self.interval, "last": self.last}
