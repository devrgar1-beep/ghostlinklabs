#!/usr/bin/env python3
"""
GhostLink Wiki - Automated Code Extraction
Systematically extracts code from conversations using planned queries

Enhancements:
- Portable paths (defaults under user's home; env/CLI overrides)
- CLI for configuring roots, batches, dry-run, and max results
- Robust fenced code parsing and inline code capture
- Safe writes (sanitized filenames, workspace scoping, UTF-8, dedup via hash)
"""

import argparse
import hashlib
import json
import logging
import os
import re
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


def default_root(env_key: str, fallback: str) -> Path:
    """Return default root path from environment or user home."""
    if os.environ.get(env_key):
        return Path(os.environ[env_key]).expanduser()
    return Path.home() / fallback


# Configuration holding roots (overridable via env and CLI)
CONFIG = {
    "wiki_root": default_root("GHOSTLINK_WIKI_ROOT", "ghostlink-wiki"),
    "trace_root": default_root("GHOSTLINK_TRACE_ROOT", "ghostlink-wiki-trace"),
}

# Extraction queries from 02_EXTRACTION_QUERIES.md
QUERY_BATCHES = {
    "BATCH_1_MCP": [
        "MCP server Node.js TypeScript index connector",
        "connector FileSystem HTTP Database GitHub Squarespace implementation",
        "Model Context Protocol tool schema stdio server",
    ],
    "BATCH_2_PYTHON": [
        "FastAPI Pydantic SQLAlchemy uvicorn async routes endpoints",
        "CMFL Collapse Mirror Forge Link reasoning cycle implementation",
        "Ghost Lumara Dak Spine kernel module class implementation",
        "content addressed storage IPFS CID hash memory persistence",
    ],
    "BATCH_3_CLOUDFLARE": [
        "Cloudflare Workers Durable Objects wrangler deployment",
        "D1 database SQLite schema migrations tables indexes",
        "KV namespace R2 bucket storage binding Workers configuration",
        "Service Bindings Workers communication coordination routing",
    ],
    "BATCH_4_REACT": [
        "React dashboard TypeScript interface visualization component",
        "Recharts LineChart BarChart visualization real-time WebSocket",
        "shadcn ui Radix Tailwind component button card dialog",
    ],
    "BATCH_5_DOCKER": [
        "Docker Dockerfile multi-stage compose container volume",
        "deployment script automation orchestration sequence bash",
        "GitHub Actions workflow deploy build test automation",
    ],
    "BATCH_6_ARCHITECTURE": [
        "64 QCL agents FCC lattice Face-Centered Cubic topology",
        "stigmergic coordination pheromone mycelial network swarm",
        "variance analysis multi-model disagreement computational substrate",
        "mathematical proof category theory lambda calculus fixed-point",
    ],
    "BATCH_7_AUTOMATION": [
        "GhostLink orchestrator Python automation sequence agent execution",
        "agent coordinator messaging state management distributed",
        "Desktop Commander MCP filesystem bash command execution",
    ],
    "BATCH_8_DATABASE": [
        "SQLite schema CREATE TABLE INDEX migration Alembic",
        "IPTC metadata taxonomy hierarchical keywords Dublin Core",
        "content addressed storage CID hash IPFS cryptographic",
    ],
    "BATCH_9_API": [
        "REST API endpoint route authentication authorization CORS",
        "WebSocket real-time streaming event handler bidirectional",
        "HTTP protocol TCP network routing mesh coordination",
    ],
    "BATCH_10_RESEARCH": [
        "research paper whitepaper publication academic documentation",
        "consciousness emergence self-organized criticality Φ threshold",
        "computational phenomenology substrate intelligence meta-learning",
    ],
    "BATCH_11_CAREER": [
        "resume cover letter career transition automotive AI diagnostics",
        "Tesla DARPA xAI company research position application",
        "skill matrix capability expertise portfolio project demonstration",
    ],
    "BATCH_12_HARDWARE": [
        "Apple Silicon M3 Pro osascript macOS system profiling",
        "hardware monitoring battery thermal CPU memory performance",
        "cross-platform macOS Windows Linux ARM64 x86 compatibility",
    ],
    "BATCH_13_TESTING": [
        "pytest test fixture integration TestClient validation",
        "error handling exception try catch validation schema",
        "logging trace audit trail observability monitoring metrics",
    ],
    "BATCH_14_CONFIG": [
        "environment variable config .env settings YAML JSON",
        "API key token JWT authentication authorization security",
        "rate limit quota throttle backpressure resource management",
    ],
    "BATCH_15_SPECIALIZED": [
        "GhostSlang symbolic compression ontology opcode 64-term",
        "Policy Guard governance capability gate sovereignty control",
        "trace event span observability distributed tracing monitoring",
    ],
}

# Extraction state tracking


def get_state_file() -> Path:
    return CONFIG["trace_root"] / "extraction_state.json"


def load_state() -> Dict[str, Any]:
    CONFIG["trace_root"].mkdir(parents=True, exist_ok=True)
    sf = get_state_file()
    if sf.exists():
        with open(sf, encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                logging.warning("Failed to parse state file; starting anew")
    return {
        "completed_batches": [],
        "completed_queries": [],
        "conversations_processed": [],
        "files_created": [],
        "last_updated": None
    }


def save_state(state: Dict[str, Any]) -> None:
    state["last_updated"] = time.strftime("%Y-%m-%d %H:%M:%S")
    CONFIG["trace_root"].mkdir(parents=True, exist_ok=True)
    with open(get_state_file(), "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)

# --------------------- Parsing and safe write helpers ---------------------


LANG_EXT = {
    "python": ".py",
    "py": ".py",
    "ts": ".ts",
    "tsx": ".tsx",
    "js": ".js",
    "jsx": ".jsx",
    "json": ".json",
    "yaml": ".yaml",
    "yml": ".yml",
    "bash": ".sh",
    "sh": ".sh",
    "dockerfile": "Dockerfile",
    "md": ".md",
}


def sanitize_filename(name: str) -> str:
    name = re.sub(r"[^a-zA-Z0-9._-]", "_", name)
    # limit length to avoid FS issues
    return name[:200]


def code_hash(code: str) -> str:
    return hashlib.sha256(code.encode("utf-8")).hexdigest()[:16]


def fenced_code_blocks(text: str) -> List[Dict[str, str]]:
    """Yield dicts of {language, code} from fenced blocks in text."""
    blocks = []
    # Triple backticks: ```lang\n...\n``` (DOTALL)
    pattern = re.compile(r"```([a-zA-Z0-9_+-]*)\n(.*?)\n```", re.DOTALL)
    for m in pattern.finditer(text):
        lang = (m.group(1) or "").strip().lower() or "txt"
        code = m.group(2)
        blocks.append({"language": lang, "code": code})
    # Inline single-backtick snippets (short)
    inline = re.compile(r"`([^`\n]{3,200})`")
    for m in inline.finditer(text):
        blocks.append({"language": "txt", "code": m.group(1)})
    return blocks


def ext_for_language(lang: str) -> str:
    if lang in LANG_EXT:
        return LANG_EXT[lang]
    # heuristic fallbacks
    if lang.startswith("docker"):
        return "Dockerfile"
    if lang in ("shell", "zsh", "bash"):
        return ".sh"
    return ".txt"


def safe_write_code_block(
    block: Dict[str, str],
    category_dir: Path,
    source_url: Optional[str],
    state: Dict[str, Any],
    dry_run: bool = False,
) -> Dict[str, Any]:
    """Safely write code block to target dir; return file info dict."""
    code = block.get("code", "")
    lang = (block.get("language") or "txt").lower()
    ext = ext_for_language(lang)
    h = code_hash(code)
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    base_name = sanitize_filename(f"{lang}_{timestamp}_{h}")
    filename = base_name + ("" if ext == "Dockerfile" else ext)
    target_name = filename if ext != "Dockerfile" else "Dockerfile"
    target_path = category_dir / target_name

    # Ensure path stays within category_dir
    category_dir.mkdir(parents=True, exist_ok=True)
    target_path_parent = target_path.parent.resolve()
    if str(target_path_parent) != str(category_dir.resolve()):
        raise ValueError("Unsafe target path")

    # Dedup: if a file with same hash already exists, skip write
    existing = [p for p in category_dir.glob(f"*{h}*")]
    if existing:
        logging.info(
            "Duplicate content detected; skipping write: %s",
            existing[0],
        )
        info = {
            "name": existing[0].name,
            "path": str(existing[0]),
            "source_url": source_url or "",
            "date": time.strftime("%Y-%m-%d"),
            "language": lang,
            "hash": h,
            "skipped": True,
        }
        state.setdefault("files_created", []).append(info)
        return info

    if not dry_run:
        with open(target_path, "w", encoding="utf-8") as f:
            f.write(code)

    info = {
        "name": target_path.name,
        "path": str(target_path),
        "source_url": source_url or "",
        "date": time.strftime("%Y-%m-%d"),
        "language": lang,
        "hash": h,
        "skipped": False,
    }
    state.setdefault("files_created", []).append(info)
    return info


def extract_code_from_conversation(
    chat_data: Dict[str, Any]
) -> List[Dict[str, str]]:
    """Extract code blocks using fenced and inline parsing."""
    code_blocks: List[Dict[str, str]] = []
    content = chat_data.get("content") or ""
    if not isinstance(content, str):
        return code_blocks
    blocks = fenced_code_blocks(content)
    # optional: file reference detection could be added here
    return blocks


def organize_by_category(
    code_blocks: List[Dict[str, str]], batch_name: str
) -> Path:
    """Organize extracted code into appropriate wiki directories"""
    category_map = {
        "BATCH_1_MCP": "04-implementation/mcp-servers/",
        "BATCH_2_PYTHON": "04-implementation/python-backend/",
        "BATCH_3_CLOUDFLARE": "03-infrastructure/cloudflare/",
        "BATCH_4_REACT": "04-implementation/typescript-frontend/",
        "BATCH_5_DOCKER": "03-infrastructure/docker/",
        "BATCH_6_ARCHITECTURE": "02-architecture/",
        "BATCH_7_AUTOMATION": "04-implementation/automation/",
        "BATCH_8_DATABASE": "05-database/",
        "BATCH_9_API": "06-api/",
        "BATCH_10_RESEARCH": "08-research/",
        "BATCH_11_CAREER": "10-reference/career/",
        "BATCH_12_HARDWARE": "04-implementation/hardware/",
        "BATCH_13_TESTING": "04-implementation/testing/",
        "BATCH_14_CONFIG": "03-infrastructure/configs/",
        "BATCH_15_SPECIALIZED": "04-implementation/specialized/",
    }
    
    target_dir = CONFIG["wiki_root"] / category_map.get(
        batch_name,
        "10-reference/misc/",
    )
    target_dir.mkdir(parents=True, exist_ok=True)
    
    return target_dir


def create_index_file(
    batch_name: str, extracted_files: List[Dict[str, Any]]
) -> Path:
    """Create an index file for the batch"""
    category_dir = organize_by_category([], batch_name)
    index_file = category_dir / "README.md"
    
    content = f"# {batch_name.replace('_', ' ').title()}\n\n"
    content += f"**Extracted:** {len(extracted_files)} files\n\n"
    content += "## Files:\n\n"
    
    for file_info in extracted_files:
        content += f"- [{file_info['name']}]({file_info['path']})\n"
        content += f"  - Source: {file_info['source_url']}\n"
        content += f"  - Date: {file_info['date']}\n\n"
    
    with open(index_file, "w", encoding="utf-8") as f:
        f.write(content)
    
    return index_file


def load_markdown_files(source_dir: Path) -> List[Dict[str, Any]]:
    """Load all markdown files from source directory as conversation data."""
    results = []
    if not source_dir.exists():
        logging.warning(f"Source directory not found: {source_dir}")
        return results
    
    for md_file in source_dir.glob("*.md"):
        try:
            with open(md_file, "r", encoding="utf-8") as f:
                content = f.read()
            results.append({
                "content": content,
                "source_url": f"file://{md_file}",
                "filename": md_file.name,
                "title": md_file.stem.replace("-", " ").title(),
            })
            logging.debug(f"Loaded: {md_file.name}")
        except Exception as e:
            logging.error(f"Failed to load {md_file}: {e}")
    
    return results


def search_in_content(
    content_list: List[Dict[str, Any]], query: str
) -> List[Dict[str, Any]]:
    """Search for query terms in loaded content."""
    # Split query into keywords for flexible matching
    keywords = [k.lower() for k in query.split() if len(k) > 2]
    results = []
    
    for item in content_list:
        content = item.get("content", "").lower()
        # Score based on keyword matches
        matches = sum(1 for kw in keywords if kw in content)
        if matches > 0:
            results.append({
                **item,
                "relevance_score": matches / len(keywords),
                "keyword_matches": matches,
            })
    
    # Sort by relevance
    results.sort(key=lambda x: x["relevance_score"], reverse=True)
    return results


def conversation_search(
    query: str, max_results: int = 10
) -> List[Dict[str, Any]]:
    """Search for relevant content from source documents.
    
    Looks in:
    1. Attached wiki documentation folder
    2. Existing wiki directories
    3. Git repository markdown files
    
    Returns list of dicts with 'content' and optional 'source_url'.
    """
    all_content: List[Dict[str, Any]] = []
    
    # Try multiple source locations
    desktop_path = (
        Path.home()
        / "Library/Mobile Documents/com~apple~CloudDocs/Desktop"
        / "Desktop - Ghost's MacBook Pro/ghostlinklabs-main"
    )
    source_paths = [
        Path.home() / "Downloads" / "files (5)",  # Attached folder
        CONFIG["wiki_root"],  # Existing wiki
        desktop_path,  # Git repo
    ]
    
    for source_path in source_paths:
        if source_path.exists():
            logging.debug(f"Scanning: {source_path}")
            all_content.extend(load_markdown_files(source_path))
            # Also scan subdirectories
            for subdir in source_path.rglob("*"):
                if subdir.is_dir() and not subdir.name.startswith("."):
                    all_content.extend(load_markdown_files(subdir))
    
    if not all_content:
        logging.warning("No source content found; using synthetic data")
        hash_id = hashlib.md5(query.encode()).hexdigest()[:8]
        synthetic_code = (
            f"# Synthetic content for: {query}\n\n"
            "```python\n# TODO: Add implementation\npass\n```"
        )
        return [{
            "content": synthetic_code,
            "source_url": f"synthetic://{hash_id}",
            "relevance_score": 0.5,
        }]
    
    # Search and return top results
    results = search_in_content(all_content, query)
    return results[:max_results]


def process_batch(
    batch_name: str,
    queries: List[str],
    state: Dict[str, Any],
    *,
    max_results: int = 10,
    dry_run: bool = False,
) -> Dict[str, Any]:
    """Process a single batch of queries"""
    print(f"\n{'='*80}")
    print(f"Processing {batch_name}")
    print(f"{'='*80}\n")
    
    batch_results: Dict[str, Any] = {
        "batch_name": batch_name,
        "queries": len(queries),
        "conversations_found": 0,
        "code_blocks_extracted": 0,
        "files_created": [],
    }
    
    for query in queries:
        if query in state["completed_queries"]:
            print(f"  ⏭ Skipping completed query: {query[:50]}...")
            continue
        
        print(f"  🔍 Query: {query}")
        
        results = conversation_search(query, max_results=max_results)
        batch_results["conversations_found"] += len(results)
        
        # Organize directory for this batch
        target_dir = organize_by_category([], batch_name)
        
        for item in results:
            blocks = extract_code_from_conversation(item)
            batch_results["code_blocks_extracted"] += len(blocks)
            for block in blocks:
                info = safe_write_code_block(
                    block,
                    target_dir,
                    item.get("source_url"),
                    state,
                    dry_run=dry_run,
                )
                batch_results["files_created"].append(info)
        
        state["completed_queries"].append(query)
        time.sleep(0.25)  # polite pacing
    
    # Mark batch as complete
    state["completed_batches"].append(batch_name)
    save_state(state)
    
    return batch_results


def generate_summary_report(state: Dict[str, Any]) -> None:
    """Generate comprehensive extraction summary"""
    report_file = CONFIG["trace_root"] / "04_EXTRACTION_REPORT.md"
    
    content = f"""# GHOSTLINK WIKI - EXTRACTION REPORT

**Generated:** {time.strftime("%Y-%m-%d %H:%M:%S")}

## Progress Summary

**Completed Batches:** {len(state['completed_batches'])} / {len(QUERY_BATCHES)}
**Completed Queries:** {len(state['completed_queries'])}
**Conversations Processed:** {len(state['conversations_processed'])}
**Files Created:** {len(state['files_created'])}

## Completed Batches

"""
    
    for batch in state['completed_batches']:
        content += f"- ✅ {batch}\n"
    
    content += "\n## Pending Batches\n\n"
    
    for batch in QUERY_BATCHES.keys():
        if batch not in state['completed_batches']:
            content += f"- ⏳ {batch}\n"
    
    content += "\n## Files Created\n\n"
    
    for file_path in state['files_created'][-20:]:  # Last 20 files
        content += f"- {file_path}\n"
    
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"\n📊 Report generated: {report_file}")


def parse_args():
    p = argparse.ArgumentParser(
        description="GhostLink Wiki - Automated Code Extraction"
    )
    p.add_argument(
        "--wiki-root",
        type=str,
        default=str(CONFIG["wiki_root"]),
        help="Wiki root directory",
    )
    p.add_argument(
        "--trace-root",
        type=str,
        default=str(CONFIG["trace_root"]),
        help="Trace root directory",
    )
    p.add_argument(
        "--batches",
        type=str,
        default="",
        help=(
            "Comma-separated batch names to process "
            "(default: all)"
        ),
    )
    p.add_argument(
        "--max-results",
        type=int,
        default=10,
        help="Max results per query",
    )
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="Do not write files; simulate only",
    )
    p.add_argument(
        "--log-level",
        type=str,
        default="INFO",
        help="Logging level (DEBUG, INFO, WARNING, ERROR)",
    )
    return p.parse_args()


def main():
    args = parse_args()

    # configure roots from args
    CONFIG["wiki_root"] = Path(args.wiki_root).expanduser()
    CONFIG["trace_root"] = Path(args.trace_root).expanduser()

    # logging
    logging.basicConfig(
        level=getattr(logging, args.log_level.upper(), logging.INFO),
        format="%(asctime)s %(levelname)s %(message)s",
    )

    print("=" * 80)
    print("GHOSTLINK WIKI - AUTOMATED EXTRACTION")
    print("=" * 80)
    print(f"Wiki:  {CONFIG['wiki_root']}")
    print(f"Trace: {CONFIG['trace_root']}")
    
    state = load_state()
    print("\nState loaded:")
    print(f"  Completed batches: {len(state['completed_batches'])}")
    print(f"  Completed queries: {len(state['completed_queries'])}")
    conv_count = len(state.get("conversations_processed", []))
    print(f"  Conversations processed: {conv_count}")

    # Determine batches to process
    selected = list(QUERY_BATCHES.keys())
    if args.batches:
        requested = [b.strip() for b in args.batches.split(",") if b.strip()]
        selected = [b for b in requested if b in QUERY_BATCHES]
        missing = [b for b in requested if b not in QUERY_BATCHES]
        if missing:
            msg = ", ".join(missing)
            logging.warning("Unknown batch names ignored: %s", msg)

    # Process each batch
    for batch_name in selected:
        queries = QUERY_BATCHES[batch_name]
        if batch_name in state['completed_batches']:
            print(f"\n⏭ Skipping completed batch: {batch_name}")
            continue
        
        batch_results = process_batch(
            batch_name,
            queries,
            state,
            max_results=args.max_results,
            dry_run=args.dry_run,
        )
        
        # Create batch index
        if batch_results['files_created']:
            index_file = create_index_file(
                batch_name,
                batch_results["files_created"],
            )
            print(f"  📄 Index created: {index_file}")
        
        # Mark batch complete
        state["completed_batches"].append(batch_name)
        save_state(state)
    
    # Generate final report
    generate_summary_report(state)
    
    print("\n" + "=" * 80)
    print("EXTRACTION COMPLETE")
    print("=" * 80)
    print(f"\nTotal batches: {len(QUERY_BATCHES)}")
    print(f"Completed: {len(state['completed_batches'])}")
    print(f"Remaining: {len(QUERY_BATCHES) - len(state['completed_batches'])}")


if __name__ == "__main__":
    main()
