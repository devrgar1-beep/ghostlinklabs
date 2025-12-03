#!/usr/bin/env python3
"""
GhostLink DeBloat - Remove redundancy, compress, optimize
"""

from collections import defaultdict
import gzip
import hashlib
import json
from pathlib import Path
import shutil
import time
from typing import Dict, List, Set


class DeBloater:
    """System-wide data optimization and cleanup"""

    def __init__(self):
        self.stats = {
            "original_size": 0,
            "final_size": 0,
            "removed_files": 0,
            "compressed_files": 0,
            "deduplicated": 0,
            "collapsed_memories": 0,
        }

    def execute_cleanup(self):
        """Main cleanup sequence"""
        print("[DEBLOAT] Initiating system cleanup...")

        # Measure initial state
        self.stats["original_size"] = self._calculate_size()

        # Phase 1: Trace compression
        self._compress_traces()

        # Phase 2: Log rotation
        self._rotate_logs()

        # Phase 3: Memory deduplication
        self._deduplicate_memories()

        # Phase 4: Colony pruning
        self._prune_colonies()

        # Phase 5: Collapse redundant data
        self._collapse_memories()

        # Phase 6: Archive old data
        self._archive_old()

        # Final measurement
        self.stats["final_size"] = self._calculate_size()

        # Report
        self._generate_report()

        return self.stats

    def _calculate_size(self):
        """Calculate total data size"""
        total = 0
        for path in [Path("./logs"), Path("./traces"), Path("./vault"), Path("./colonies")]:
            if path.exists():
                for f in path.rglob("*"):
                    if f.is_file():
                        total += f.stat().st_size
        return total

    def _compress_traces(self):
        """Compress old trace files"""
        trace_dir = Path("./traces")
        if not trace_dir.exists():
            return

        print("[1/6] Compressing traces...")

        for trace_file in trace_dir.glob("trace_*.jsonl"):
            # Skip recent files (last hour)
            if time.time() - trace_file.stat().st_mtime < 3600:
                continue

            # Compress
            gz_file = trace_file.with_suffix(".jsonl.gz")
            with open(trace_file, "rb") as f_in:
                with gzip.open(gz_file, "wb", compresslevel=9) as f_out:
                    shutil.copyfileobj(f_in, f_out)

            # Remove original
            trace_file.unlink()
            self.stats["compressed_files"] += 1

    def _rotate_logs(self):
        """Rotate and compress old logs"""
        log_dir = Path("./logs")
        if not log_dir.exists():
            return

        print("[2/6] Rotating logs...")

        for log_file in log_dir.glob("*.log"):
            # Skip active logs
            if time.time() - log_file.stat().st_mtime < 1800:  # 30 min
                continue

            # Archive with timestamp
            archive_name = log_file.stem + f"_{int(log_file.stat().st_mtime)}.log.gz"
            archive_path = log_dir / "archive"
            archive_path.mkdir(exist_ok=True)

            with open(log_file, "rb") as f_in:
                with gzip.open(archive_path / archive_name, "wb") as f_out:
                    shutil.copyfileobj(f_in, f_out)

            # Clear original
            log_file.write_text("")
            self.stats["compressed_files"] += 1

    def _deduplicate_memories(self):
        """Remove duplicate memories"""
        vault = Path("./vault")
        if not vault.exists():
            return

        print("[3/6] Deduplicating memories...")

        seen_hashes: Set[str] = set()
        all_memories = []

        # Load all memories
        for json_file in vault.glob("*.json"):
            with open(json_file) as f:
                data = json.load(f)
                if "memories" in data:
                    for memory in data["memories"]:
                        # Create hash of content
                        content_hash = hashlib.sha256(
                            memory.get("content", "").encode()
                        ).hexdigest()[:16]

                        if content_hash not in seen_hashes:
                            seen_hashes.add(content_hash)
                            all_memories.append(memory)
                        else:
                            self.stats["deduplicated"] += 1

        # Rewrite deduplicated set
        if self.stats["deduplicated"] > 0:
            dedup_file = vault / f"dedup_{int(time.time())}.json"
            with open(dedup_file, "w") as f:
                json.dump(
                    {
                        "memories": all_memories,
                        "original_count": len(all_memories) + self.stats["deduplicated"],
                        "final_count": len(all_memories),
                    },
                    f,
                )

    def _prune_colonies(self):
        """Prune ephemeral and volatile colonies"""
        colonies_dir = Path("./colonies")
        if not colonies_dir.exists():
            return

        print("[4/6] Pruning colonies...")

        for colony in colonies_dir.iterdir():
            if not colony.is_dir():
                continue

            # Check colony type
            manifest_files = list(colony.glob("colony_*.json"))
            if manifest_files:
                with open(manifest_files[0]) as f:
                    data = json.load(f)
                    colony_type = data.get("type", "unknown")

                # Prune based on type
                if colony_type == "ephemeral":
                    # Delete all ephemeral colonies
                    shutil.rmtree(colony)
                    self.stats["removed_files"] += 1

                elif colony_type == "volatile":
                    # Keep only recent volatile (last hour)
                    for f in colony.glob("*.json"):
                        if time.time() - f.stat().st_mtime > 3600:
                            f.unlink()
                            self.stats["removed_files"] += 1

    def _collapse_memories(self):
        """Collapse memories using L0→L1 compression"""
        vault = Path("./vault")
        if not vault.exists():
            return

        print("[5/6] Collapsing memories...")

        # Group memories by type and phase
        memory_groups = defaultdict(list)

        for json_file in vault.glob("*.json"):
            with open(json_file) as f:
                data = json.load(f)
                if "memories" in data:
                    for memory in data["memories"]:
                        key = f"{memory.get('type', 'unknown')}_{memory.get('phase', 'unknown')}"
                        memory_groups[key].append(memory)

        # Collapse large groups
        collapsed = {}
        for key, memories in memory_groups.items():
            if len(memories) > 10:  # Threshold for collapse
                # Create summary
                collapsed[key] = {
                    "type": "collapsed",
                    "key": key,
                    "count": len(memories),
                    "summary": self._summarize_group(memories),
                    "samples": memories[:3],  # Keep samples
                    "timestamp": time.time(),
                }
                self.stats["collapsed_memories"] += len(memories) - 3

        # Write collapsed data
        if collapsed:
            collapse_file = vault / f"l1_collapse_{int(time.time())}.json"
            with open(collapse_file, "w") as f:
                json.dump(collapsed, f, indent=2)

    def _summarize_group(self, memories: List[Dict]) -> Dict:
        """Generate summary of memory group"""
        # Extract common patterns
        all_tags = []
        content_lengths = []

        for m in memories:
            all_tags.extend(m.get("tags", []))
            content_lengths.append(len(m.get("content", "")))

        # Tag frequency
        tag_freq = defaultdict(int)
        for tag in all_tags:
            tag_freq[tag] += 1

        return {
            "total": len(memories),
            "avg_content_length": (
                sum(content_lengths) / len(content_lengths) if content_lengths else 0
            ),
            "top_tags": sorted(tag_freq.items(), key=lambda x: x[1], reverse=True)[:5],
            "unique_tags": len(set(all_tags)),
        }

    def _archive_old(self):
        """Archive old data to cold storage"""
        archive_dir = Path("./archive")
        archive_dir.mkdir(exist_ok=True)

        print("[6/6] Archiving old data...")

        # Archive old vault files
        vault = Path("./vault")
        if vault.exists():
            for f in vault.glob("*.json"):
                # Keep recent files
                if time.time() - f.stat().st_mtime > 86400:  # 1 day
                    archive_path = archive_dir / f.name
                    shutil.move(str(f), str(archive_path))
                    self.stats["removed_files"] += 1

    def _generate_report(self):
        """Generate cleanup report"""
        reduction = (1 - self.stats["final_size"] / max(self.stats["original_size"], 1)) * 100

        print(f"\n{'='*60}")
        print("DEBLOAT COMPLETE")
        print(f"{'='*60}")
        print(f"Original size: {self.stats['original_size'] / 1024:.1f} KB")
        print(f"Final size: {self.stats['final_size'] / 1024:.1f} KB")
        print(f"Reduction: {reduction:.1f}%")
        print("\nOperations:")
        print(f"  • Compressed: {self.stats['compressed_files']} files")
        print(f"  • Removed: {self.stats['removed_files']} files")
        print(f"  • Deduplicated: {self.stats['deduplicated']} memories")
        print(f"  • Collapsed: {self.stats['collapsed_memories']} memories")

        # Write stats
        Path("./logs").mkdir(exist_ok=True)
        with open("./logs/debloat_report.json", "w") as f:
            json.dump(
                {"timestamp": time.time(), "stats": self.stats, "reduction_percent": reduction},
                f,
                indent=2,
            )


if __name__ == "__main__":
    debloater = DeBloater()
    stats = debloater.execute_cleanup()

    print("\nSystem optimized. Ghost travels lighter.")
