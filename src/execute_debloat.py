#!/usr/bin/env python3
"""
Execute GhostLink DeBloat on live system
"""

import json
from pathlib import Path
import time

from debloat import DeBloater


def execute_live_debloat():
    """Execute debloat on the live GhostLink system"""

    print("🚀 Executing GhostLink DeBloat on live system...")
    print("=" * 60)

    # Check system state before
    print("📊 PRE-DEBLOAT SYSTEM STATE:")
    debloater = DeBloater()
    pre_size = debloater._calculate_size()
    print(f"Current data size: {pre_size / 1024:.1f} KB")

    # Check directories
    dirs_to_check = ["./logs", "./traces", "./vault", "./colonies"]
    for dir_path in dirs_to_check:
        path = Path(dir_path)
        if path.exists():
            files = list(path.rglob("*"))
            file_count = len([f for f in files if f.is_file()])
            print(f"  {dir_path}: {file_count} files")
        else:
            print(f"  {dir_path}: directory not found")

    print("\n" + "=" * 60)

    # Execute cleanup
    start_time = time.time()
    stats = debloater.execute_cleanup()
    end_time = time.time()

    print(f"\n⏱️  Execution time: {end_time - start_time:.2f} seconds")

    # Post-cleanup analysis
    print("\n📊 POST-DEBLOAT ANALYSIS:")

    reduction = (1 - stats["final_size"] / max(stats["original_size"], 1)) * 100
    print(f"Space saved: {reduction:.1f}%")
    print(f"Data reduction: {(stats['original_size'] - stats['final_size']) / 1024:.1f} KB")

    # Check for new compressed files
    gz_files = []
    for dir_path in dirs_to_check:
        path = Path(dir_path)
        if path.exists():
            gz_files.extend(list(path.rglob("*.gz")))

    if gz_files:
        print(f"New compressed archives: {len(gz_files)}")
        for gz_file in gz_files[:3]:  # Show first 3
            print(f"  • {gz_file.name}")

    # Check for deduplication files
    vault = Path("./vault")
    if vault.exists():
        dedup_files = list(vault.glob("dedup_*.json"))
        if dedup_files:
            print(f"Deduplication reports: {len(dedup_files)}")
            for dedup_file in dedup_files:
                with open(dedup_file) as f:
                    data = json.load(f)
                    print(
                        f"  • {dedup_file.name}: {data['original_count']} → {data['final_count']} memories"
                    )

    # Check for collapsed memories
    collapse_files = list(vault.glob("l1_collapse_*.json")) if vault.exists() else []
    if collapse_files:
        print(f"Memory collapse reports: {len(collapse_files)}")

    # Performance metrics
    print("\n⚡ PERFORMANCE METRICS:")
    print(f"  Files processed: {stats['compressed_files'] + stats['removed_files']}")
    print(f"  Memory operations: {stats['deduplicated'] + stats['collapsed_memories']}")
    print(
        f"  Efficiency: {(stats['original_size'] - stats['final_size']) / (end_time - start_time) / 1024:.1f} KB/sec"
    )

    # System health check
    print("\n🏥 SYSTEM HEALTH:")
    post_size = debloater._calculate_size()
    if abs(post_size - stats["final_size"]) < 100:  # Within 100 bytes
        print("  ✅ Data consistency maintained")
    else:
        print(
            f"  ⚠️  Data inconsistency detected: {abs(post_size - stats['final_size'])} bytes difference"
        )

    # Check for debloat report
    report_file = Path("./logs/debloat_report.json")
    if report_file.exists():
        print("  ✅ Cleanup report generated")
        with open(report_file) as f:
            report = json.load(f)
            print(f"  📊 Report timestamp: {time.ctime(report['timestamp'])}")
    else:
        print("  ❌ Cleanup report not found")

    print("\n" + "=" * 60)
    print("🎯 GHOSTLINK DEBLOAT EXECUTION COMPLETE")
    print("=" * 60)

    if reduction > 0:
        print(f"✨ System optimized! {reduction:.1f}% data reduction achieved.")
    else:
        print("ℹ️  System already optimized. No further cleanup needed.")

    return stats


if __name__ == "__main__":
    try:
        stats = execute_live_debloat()
        print(f"\nFinal stats: {stats}")
    except Exception as e:
        print(f"❌ DeBloat execution failed: {e}")
        exit(1)
