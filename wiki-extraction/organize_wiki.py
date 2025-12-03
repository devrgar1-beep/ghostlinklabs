#!/usr/bin/env python3
"""
GhostLink Wiki Organization Script
Restructures extracted wiki content into semantic categories.
Generates indexes, removes node_modules noise, integrates with macOS.
"""

import hashlib
import json
import logging
import shutil
from pathlib import Path
from typing import Dict, List, Set
from collections import defaultdict

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

# Configuration
WIKI_ROOT = Path.home() / "ghostlink-wiki"
ORGANIZED_ROOT = Path.home() / "ghostlink-wiki-organized"
STATE_FILE = Path.home() / "ghostlink-wiki-trace" / "extraction_state.json"


def load_state() -> Dict:
    """Load extraction state to identify duplicates and sources"""
    if not STATE_FILE.exists():
        return {}
    return json.loads(STATE_FILE.read_text())


def is_node_modules_file(path: Path, source_url: str = "") -> bool:
    """Check if file is from node_modules"""
    return "node_modules" in str(path) or "node_modules" in source_url


def is_core_runtime_file(filename: str) -> bool:
    """Identify core GhostLink runtime files"""
    core_files = {
        "ghostlink_main", "ghostlink_runtime", "ghostlink_consolidated",
        "ghost_consciousness", "autonomous_evolution", "ghostlink_lattice",
        "bios_bridge", "ghostlink_audit", "ghostknife"
    }
    return any(core in filename.lower() for core in core_files)


def extract_semantic_name(content: str, ext: str) -> str:
    """Extract semantic name from code content"""
    lines = content.split('\n')[:20]  # First 20 lines
    
    # Look for class names
    for line in lines:
        if 'class ' in line and ext == '.py':
            name = line.split('class ')[1].split('(')[0].split(':')[0].strip()
            if name and name[0].isupper():
                return name
        elif 'function ' in line and ext in ['.js', '.ts']:
            name = line.split('function ')[1].split('(')[0].strip()
            if name:
                return name
        elif 'def ' in line and ext == '.py':
            name = line.split('def ')[1].split('(')[0].strip()
            if name and not name.startswith('_'):
                return name
    
    return None


def categorize_file(filepath: Path, source_url: str) -> str:
    """Determine correct category for file"""
    filename = filepath.name.lower()
    
    # Core runtime
    if is_core_runtime_file(filename):
        return "core-runtime"
    
    # Node modules
    if is_node_modules_file(filepath, source_url):
        return "node-modules-docs"
    
    # Unified dashboard
    if "unified-dashboard" in source_url or "unified-dashboard" in str(filepath):
        if "node_modules" not in str(filepath):
            return "unified-dashboard"
        return "node-modules-docs"
    
    # MCP servers
    if "mcp" in filename or "connector" in filename or "server" in source_url:
        return "mcp-servers"
    
    # Infrastructure
    if any(x in filename for x in ["docker", "cloudflare", "worker", ".yml", ".yaml"]):
        return "infrastructure"
    
    # Documentation
    if filepath.suffix in ['.md', '.txt'] and not is_node_modules_file(filepath, source_url):
        return "documentation"
    
    # Database
    if any(x in filename for x in ["sql", "schema", "migration", "database"]):
        return "database"
    
    # API
    if any(x in filename for x in ["api", "endpoint", "route", "websocket"]):
        return "api"
    
    # Testing
    if any(x in filename for x in ["test", "spec", "mock"]):
        return "testing"
    
    # Default to implementation
    return "implementation"


def organize_wiki():
    """Main organization function"""
    logger.info("="*60)
    logger.info("GHOSTLINK WIKI ORGANIZATION")
    logger.info("="*60)
    
    # Load state
    logger.info("Loading extraction state...")
    state = load_state()
    files_data = state.get("files_created", [])
    
    # Create organized structure
    logger.info(f"Creating organized wiki at: {ORGANIZED_ROOT}")
    ORGANIZED_ROOT.mkdir(exist_ok=True)
    
    categories = {
        "core-runtime": ORGANIZED_ROOT / "core-runtime",
        "unified-dashboard": ORGANIZED_ROOT / "unified-dashboard",
        "mcp-servers": ORGANIZED_ROOT / "mcp-servers",
        "infrastructure": ORGANIZED_ROOT / "infrastructure",
        "documentation": ORGANIZED_ROOT / "documentation",
        "database": ORGANIZED_ROOT / "database",
        "api": ORGANIZED_ROOT / "api",
        "testing": ORGANIZED_ROOT / "testing",
        "node-modules-docs": ORGANIZED_ROOT / "node-modules-docs",
        "implementation": ORGANIZED_ROOT / "implementation"
    }
    
    for path in categories.values():
        path.mkdir(exist_ok=True)
    
    # Statistics
    stats = defaultdict(int)
    processed = 0
    skipped_dupes = 0
    
    # Process files
    logger.info("Processing files...")
    for file_data in files_data:
        if file_data.get("skipped"):
            skipped_dupes += 1
            continue
        
        filepath = Path(file_data.get("path", ""))
        if not filepath.exists():
            continue
        
        source_url = file_data.get("source_url", "")
        category = categorize_file(filepath, source_url)
        
        # Skip node_modules txt files (too noisy)
        if category == "node-modules-docs" and filepath.suffix == ".txt":
            stats["skipped_node_modules"] += 1
            continue
        
        # Copy to organized location
        dest_dir = categories[category]
        dest_file = dest_dir / filepath.name
        
        # Handle name collisions
        counter = 1
        while dest_file.exists():
            stem = filepath.stem
            dest_file = dest_dir / f"{stem}_{counter}{filepath.suffix}"
            counter += 1
        
        try:
            shutil.copy2(filepath, dest_file)
            stats[category] += 1
            processed += 1
            
            if processed % 1000 == 0:
                logger.info(f"  Processed {processed:,} files...")
        
        except Exception as e:
            logger.error(f"Error copying {filepath}: {e}")
    
    # Generate indexes
    logger.info("\nGenerating category indexes...")
    for category, path in categories.items():
        files = sorted(path.glob("*"))
        if not files:
            continue
        
        readme = path / "README.md"
        with readme.open("w") as f:
            f.write(f"# {category.replace('-', ' ').title()}\n\n")
            f.write(f"**Files:** {len(files)}\n\n")
            
            # Group by extension
            by_ext = defaultdict(list)
            for file in files:
                if file.name != "README.md":
                    by_ext[file.suffix].append(file)
            
            for ext, ext_files in sorted(by_ext.items()):
                f.write(f"## {ext or 'No extension'} ({len(ext_files)} files)\n\n")
                for file in sorted(ext_files)[:50]:  # Limit to 50 per type
                    f.write(f"- [{file.name}]({file.name})\n")
                if len(ext_files) > 50:
                    f.write(f"\n*...and {len(ext_files) - 50} more*\n")
                f.write("\n")
    
    # Master index
    logger.info("Generating master index...")
    master_index = ORGANIZED_ROOT / "INDEX.md"
    with master_index.open("w") as f:
        f.write("# GhostLink Wiki - Organized Index\n\n")
        f.write(f"**Generated:** {Path.cwd()}\n\n")
        f.write("## Categories\n\n")
        
        for category, path in sorted(categories.items()):
            count = stats.get(category, 0)
            if count > 0:
                f.write(f"### [{category.replace('-', ' ').title()}](./{category}/)\n\n")
                f.write(f"**Files:** {count:,}\n\n")
                
                # Show file type breakdown
                by_ext = defaultdict(int)
                for file in path.glob("*"):
                    if file.name != "README.md":
                        by_ext[file.suffix] += 1
                
                for ext, count in sorted(by_ext.items(), key=lambda x: -x[1])[:5]:
                    f.write(f"- `{ext or 'none'}`: {count:,} files\n")
                f.write("\n")
        
        f.write("\n## Statistics\n\n")
        f.write(f"- **Total files processed:** {processed:,}\n")
        f.write(f"- **Duplicates skipped:** {skipped_dupes:,}\n")
        f.write(f"- **Node modules skipped:** {stats['skipped_node_modules']:,}\n")
    
    # Print summary
    logger.info("\n" + "="*60)
    logger.info("ORGANIZATION COMPLETE")
    logger.info("="*60)
    logger.info(f"Organized wiki: {ORGANIZED_ROOT}")
    logger.info(f"Files processed: {processed:,}")
    logger.info(f"Duplicates skipped: {skipped_dupes:,}")
    logger.info(f"Node modules skipped: {stats['skipped_node_modules']:,}")
    logger.info("\nCategory breakdown:")
    for category, count in sorted(stats.items(), key=lambda x: -x[1]):
        if category != "skipped_node_modules" and count > 0:
            logger.info(f"  {category:30s}: {count:6,} files")
    logger.info("="*60)


if __name__ == "__main__":
    organize_wiki()
