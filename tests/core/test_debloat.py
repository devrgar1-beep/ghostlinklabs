#!/usr/bin/env python3
"""
Test GhostLink DeBloat functionality
"""

import json
import os
import time
from pathlib import Path

from debloat import DeBloater


def create_test_data():
    """Create sample data for testing debloat"""

    # Create directories
    Path("./logs").mkdir(exist_ok=True)
    Path("./traces").mkdir(exist_ok=True)
    Path("./vault").mkdir(exist_ok=True)
    Path("./colonies").mkdir(exist_ok=True)

    # Create old log file
    old_log = Path("./logs/old_test.log")
    old_log.write_text("Old log data\n" * 100)
    # Make it old
    os.utime(old_log, (time.time() - 7200, time.time() - 7200))  # 2 hours ago

    # Create recent log file
    recent_log = Path("./logs/recent_test.log")
    recent_log.write_text("Recent log data\n" * 50)

    # Create trace files
    old_trace = Path("./traces/trace_old.jsonl")
    old_trace.write_text('{"event": "old", "data": "test"}\n' * 200)
    os.utime(old_trace, (time.time() - 7200, time.time() - 7200))

    recent_trace = Path("./traces/trace_recent.jsonl")
    recent_trace.write_text('{"event": "recent", "data": "test"}\n' * 100)

    # Create vault with duplicate memories
    vault_data = {
        "memories": [
            {"content": "duplicate content 1", "type": "test", "tags": ["tag1"]},
            {"content": "duplicate content 1", "type": "test", "tags": ["tag1"]},  # duplicate
            {"content": "duplicate content 1", "type": "test", "tags": ["tag1"]},  # duplicate
            {"content": "unique content", "type": "test", "tags": ["tag2"]},
            {"content": "another duplicate", "type": "test", "tags": ["tag3"]},
            {"content": "another duplicate", "type": "test", "tags": ["tag3"]},  # duplicate
        ]
    }

    with open("./vault/memories.json", "w") as f:
        json.dump(vault_data, f)

    # Create colony
    colony_dir = Path("./colonies/test_colony")
    colony_dir.mkdir(exist_ok=True)

    colony_manifest = {
        "type": "volatile",
        "name": "test_colony",
        "created": time.time() - 7200,  # 2 hours ago
    }

    with open(colony_dir / "colony_manifest.json", "w") as f:
        json.dump(colony_manifest, f)

    # Create old colony file
    old_file = colony_dir / "old_data.json"
    old_file.write_text('{"data": "old volatile data"}')
    os.utime(old_file, (time.time() - 7200, time.time() - 7200))

    print("✅ Test data created")


def test_debloat():
    """Test debloat functionality"""

    print("🔄 Testing GhostLink DeBloat...")

    # Create test data
    create_test_data()

    # Run debloat
    debloater = DeBloater()
    stats = debloater.execute_cleanup()

    # Verify results
    print("\n📊 VERIFICATION:")

    # Check compression
    gz_files = list(Path("./logs/archive").glob("*.gz")) if Path("./logs/archive").exists() else []
    print(f"Compressed files: {len(gz_files)} (expected: 1)")

    # Check deduplication
    dedup_files = list(Path("./vault").glob("dedup_*.json"))
    print(f"Deduplication files: {len(dedup_files)} (expected: 1)")

    # Check colony pruning
    colony_files = list(Path("./colonies/test_colony").glob("*.json"))
    print(f"Remaining colony files: {len(colony_files)} (expected: 1, manifest only)")

    # Check stats
    print("\n📈 FINAL STATS:")
    print(f"  Original size: {stats['original_size']} bytes")
    print(f"  Final size: {stats['final_size']} bytes")
    print(f"  Compressed: {stats['compressed_files']}")
    print(f"  Removed: {stats['removed_files']}")
    print(f"  Deduplicated: {stats['deduplicated']}")
    print(f"  Collapsed: {stats['collapsed_memories']}")

    # Cleanup test data
    print("\n🧹 Cleaning up test data...")
    import shutil

    for dir_path in ["./logs", "./traces", "./vault", "./colonies", "./archive"]:
        if Path(dir_path).exists():
            shutil.rmtree(dir_path)

    print("✅ Test complete!")


if __name__ == "__main__":
    test_debloat()
