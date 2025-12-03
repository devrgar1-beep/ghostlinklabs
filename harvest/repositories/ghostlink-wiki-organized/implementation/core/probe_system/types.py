"""
GhostLink Probe System - Core Types and Interfaces

Implements the probe runtime: scatter → sync → emerge
Structure-only resonance engine with zero payload storage.
"""

from __future__ import annotations

import asyncio
from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field
import hashlib
import json
import secrets
from typing import Any, Protocol


# Core Types
@dataclass
class Signal:
    """Input signal (text, image, audio, video, metadata)"""

    id: str
    kind: str  # 'text' | 'image' | 'audio' | 'video'
    ts: float
    bytes_: bytes | None = None
    text: str | None = None
    meta: dict[str, Any] | None = None

    @property
    def bytes(self) -> bytes | None:
        return self.bytes_

    @bytes.setter
    def bytes(self, value: bytes | None):
        self.bytes_ = value


@dataclass
class Candidate:
    """Potential match from scatter phase"""

    id: str
    signal_id: str
    score: float
    hints: list[str] = field(default_factory=list)


@dataclass
class Resonance:
    """Confirmed match from sync phase"""

    probe_id: str
    candidate_id: str
    strength: float
    spectrum: list[float]
    ts: float
    hints: list[str] = field(default_factory=list)


@dataclass
class Emergence:
    """Human-facing outputs and actions"""

    actions: list[dict[str, Any]]
    summary: str


# Probe Interface
class Probe(Protocol):
    """Probe interface: scatter → sync → emerge"""

    id: str
    name: str
    version: str
    seed: dict[str, Any]
    policy: dict[str, Any]

    async def scatter(self, signal: Signal, ctx: ScatterContext) -> list[Candidate]:
        """Phase 1: Scatter - find potential matches"""
        ...

    def sync(self, candidates: list[Candidate], ctx: SyncContext) -> list[Resonance]:
        """Phase 2: Sync - confirm and rank matches"""
        ...

    def emerge(self, resonances: list[Resonance], ctx: EmergeContext) -> Emergence:
        """Phase 3: Emerge - generate human outputs"""
        ...


# Context Interfaces
@dataclass
class ScatterContext:
    """Context for scatter phase"""

    embed: Callable[[str | bytes], Awaitable[list[float]]]
    tokens: set[str]

    async def embed_text(self, text: str) -> list[float]:
        """Embed text content"""
        return await self.embed(text)

    async def embed_bytes(self, data: bytes) -> list[float]:
        """Embed binary content"""
        return await self.embed(data)


@dataclass
class SyncContext:
    """Context for sync phase"""

    top_k: int = 8


@dataclass
class EmergeContext:
    """Context for emerge phase"""

    ui: UIContext


@dataclass
class UIContext:
    """UI interaction context"""

    toast: Callable[[str], None]


# Signal Sketching (Structure-Only)
class SignalSketcher:
    """Converts signals to salted structural sketches"""

    def __init__(self, device_salt: str | None = None):
        self.device_salt = device_salt or secrets.token_hex(16)
        self.session_salt = secrets.token_hex(8)

    def sketch_signal(self, signal: Signal) -> str:
        """Create salted sketch of signal (no payload storage)"""
        sketch_data = {
            "id": signal.id,
            "kind": signal.kind,
            "ts": signal.ts,
            "salt": f"{self.device_salt}:{self.session_salt}",
        }

        if signal.text:
            sketch_data["text_sketch"] = self._sketch_text(signal.text)
        if signal.bytes:
            sketch_data["bytes_sketch"] = self._sketch_bytes(signal.bytes)

        sketch_json = json.dumps(sketch_data, sort_keys=True)
        return hashlib.sha256(sketch_json.encode()).hexdigest()

    def _sketch_text(self, text: str) -> dict[str, Any]:
        """Text sketching: bag-of-n-grams, token counts"""
        words = text.lower().split()
        bigrams = [f"{words[i]}_{words[i+1]}" for i in range(len(words) - 1)]
        trigrams = [f"{words[i]}_{words[i+1]}_{words[i+2]}" for i in range(len(words) - 2)]

        return {
            "word_count": len(words),
            "unique_words": len(set(words)),
            "bigram_count": len(bigrams),
            "trigram_count": len(trigrams),
            "avg_word_len": (sum(len(w) for w in words) / len(words) if words else 0),
        }

    def _sketch_bytes(self, data: bytes) -> dict[str, Any]:
        """Binary sketching: perceptual hashes, statistics"""
        # Simple byte frequency analysis (structure only)
        freq = {}
        for byte in data:
            freq[byte] = freq.get(byte, 0) + 1

        return {
            "size": len(data),
            "entropy": self._calculate_entropy(data),
            "byte_freq": {str(k): v for k, v in freq.items()},
            "chunk_hashes": self._chunk_hashes(data),
        }

    def _calculate_entropy(self, data: bytes) -> float:
        """Calculate Shannon entropy"""
        if not data:
            return 0.0

        freq = {}
        for byte in data:
            freq[byte] = freq.get(byte, 0) + 1

        entropy = 0.0
        length = len(data)
        for count in freq.values():
            p = count / length
            entropy -= p * (p.bit_length() - 1)  # Approximation

        return entropy

    def _chunk_hashes(self, data: bytes, chunk_size: int = 1024) -> list[str]:
        """Create rolling hashes of data chunks"""
        hashes = []
        for i in range(0, len(data), chunk_size):
            chunk = data[i : i + chunk_size]
            hashes.append(hashlib.md5(chunk).hexdigest())
        return hashes


# Resonance Engine
class ResonanceEngine:
    """Core resonance calculation"""

    @staticmethod
    def calculate_strength(
        a: list[float], b: list[float], a_tokens: set[str], b_tokens: set[str]
    ) -> float:
        """Calculate resonance strength between embeddings and token sets"""
        # Cosine similarity of embeddings
        dot = sum(ai * bi for ai, bi in zip(a, b))
        na = sum(ai * ai for ai in a) ** 0.5
        nb = sum(bi * bi for bi in b) ** 0.5
        cos = dot / (na * nb) if na and nb else 0

        # Jaccard similarity of token sets
        inter = len(a_tokens & b_tokens)
        union = len(a_tokens | b_tokens) or 1
        jaccard = inter / union

        # Weighted combination
        return min(1.0, max(0.0, 0.7 * cos + 0.3 * jaccard))


# Probe Runner
class ProbeRunner:
    """Executes probe pipeline: scatter → sync → emerge"""

    def __init__(self, embedder: Callable[[str | bytes], Awaitable[list[float]]] | None = None):
        self.embedder = embedder or self._default_embedder
        self.sketcher = SignalSketcher()

    async def run_probe(self, probe: Probe, signal: Signal) -> Emergence:
        """Execute complete probe pipeline"""
        # Phase 1: Scatter
        scatter_ctx = ScatterContext(embed=self.embedder, tokens=set(probe.seed.get("tokens", [])))
        candidates = await probe.scatter(signal, scatter_ctx)

        # Phase 2: Sync
        sync_ctx = SyncContext()
        resonances = probe.sync(candidates, sync_ctx)

        # Phase 3: Emerge
        emerge_ctx = EmergeContext(ui=UIContext(toast=self._default_toast))
        return probe.emerge(resonances, emerge_ctx)

    async def _default_embedder(self, content: str | bytes) -> list[float]:
        """Simple default embedder (placeholder)"""
        # This would be replaced with actual embedding model
        if isinstance(content, str):
            # Simple bag-of-words style embedding
            words = content.lower().split()
            embedding = [0.0] * 128
            for i, word in enumerate(words[:128]):
                embedding[i % 128] += hash(word) % 1000 / 1000.0
            return embedding
        # Simple byte-based embedding
        embedding = [0.0] * 128
        for i, byte in enumerate(content[:128]):
            embedding[i % 128] += byte / 255.0
        return embedding

    def _default_toast(self, message: str):
        """Default toast implementation"""
        # Default implementation - can be overridden


# Example Probe Implementation
class CitationProbe:
    """Example probe: Citation Consistency Checker"""

    def __init__(self):
        self.id = "gl.probe.citation-check.v1"
        self.name = "Citation Consistency"
        self.version = "1.0.0"
        self.seed = {"grammar": "APA|MLA|Chicago", "tokens": ["et al.", "doi:", "pp.", "In:"]}
        self.policy = {"retention": "session", "exportable": True, "net": False, "io": ["fs"]}

    async def scatter(self, signal: Signal, ctx: ScatterContext) -> list[Candidate]:
        """Find potential citations in text"""
        if signal.kind != "text" or not signal.text:
            return []

        text = signal.text
        score = 0.0
        hints = []

        # Check for citation markers
        citation_markers = ["doi:", "et al.", "pp.", "vol.", "no."]
        found_markers = [m for m in citation_markers if m in text.lower()]

        if found_markers:
            score = min(0.6 + len(found_markers) * 0.1, 1.0)
            hints.extend([f"citation-marker:{m}" for m in found_markers])

        # Check for structured patterns
        if "(" in text and ")" in text:
            score += 0.2
            hints.append("structured-reference")

        return [
            Candidate(
                id=f"{signal.id}:citation", signal_id=signal.id, score=min(score, 1.0), hints=hints
            )
        ]

    def sync(self, candidates: list[Candidate], ctx: SyncContext) -> list[Resonance]:
        """Confirm citation resonances"""
        resonances = []
        for candidate in candidates:
            if candidate.score > 0.3:  # Threshold
                resonance = Resonance(
                    probe_id=self.id,
                    candidate_id=candidate.id,
                    strength=min(1.0, candidate.score + 0.2),
                    spectrum=[candidate.score, 0.1, 0.3],
                    ts=asyncio.get_event_loop().time(),
                    hints=candidate.hints,
                )
                resonances.append(resonance)

        return sorted(resonances, key=lambda r: r.strength, reverse=True)[: ctx.top_k]

    def emerge(self, resonances: list[Resonance], ctx: EmergeContext) -> Emergence:
        """Generate citation analysis output"""
        count = len(resonances)

        if count == 0:
            summary = "No citation patterns detected"
            actions = []
        else:
            summary = f"{count} likely citation(s) detected; " "recommend consistency check"
            actions = [
                {"label": "Open Style Guide", "run": lambda: ctx.ui.toast("Style guide opened")}
            ]

        return Emergence(actions=actions, summary=summary)
