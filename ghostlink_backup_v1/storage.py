from hashlib import sha256
from typing import Dict


class MockIPFS:
    """A simple in-memory mock of IPFS using SHA-256 hashing."""

    def __init__(self) -> None:
        self.storage: Dict[str, str] = {}

    def store(self, data: str) -> str:
        """Store data and return its SHA-256 hash."""
        digest = sha256(data.encode()).hexdigest()
        self.storage[digest] = data
        return digest

    def retrieve(self, data_hash: str) -> str | None:
        """Retrieve data by its hash."""
        return self.storage.get(data_hash)
