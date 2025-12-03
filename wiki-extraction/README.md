# GhostLink Wiki Extraction Tool

Automated code extraction from conversations to build the comprehensive GhostLink technical wiki.

## Overview

This tool systematically searches through your conversation history, extracts code blocks, documentation, and architecture details, then organizes them into the wiki structure defined in `01_CONSTRUCTION_PLAN.md`.

## Features

- **Portable paths**: Defaults to `~/ghostlink-wiki` and `~/ghostlink-wiki-trace`, overridable via env vars or CLI
- **CLI configuration**: Control roots, batch selection, dry-run mode, max results, logging
- **Robust parsing**: Extracts fenced code blocks with language detection and inline code snippets
- **Safe writes**: Sanitized filenames, workspace scoping, UTF-8 encoding, deduplication via content hash
- **State tracking**: JSON-based progress tracking, resumable extraction
- **Type safety**: Full typing annotations for maintainability

## Installation

```bash
# No external dependencies required - uses stdlib only
chmod +x extraction_script.py
```

## Usage

### Basic Extraction

```bash
# Extract all batches (dry-run to preview)
./extraction_script.py --dry-run

# Extract for real
./extraction_script.py
```

### Targeted Extraction

```bash
# Extract specific batches
./extraction_script.py --batches BATCH_1_MCP,BATCH_2_PYTHON

# Custom wiki location
./extraction_script.py --wiki-root /path/to/wiki --trace-root /path/to/trace

# Increase results per query
./extraction_script.py --max-results 20

# Debug logging
./extraction_script.py --log-level DEBUG
```

### Environment Variables

```bash
# Set default paths via environment
export GHOSTLINK_WIKI_ROOT="/Users/ghostlink/ghostlink-wiki"
export GHOSTLINK_TRACE_ROOT="/Users/ghostlink/ghostlink-wiki-trace"
./extraction_script.py
```

## Query Batches

The script processes 15 predefined batches covering all GhostLink domains:

1. **BATCH_1_MCP**: MCP servers & connectors
2. **BATCH_2_PYTHON**: Core Python modules
3. **BATCH_3_CLOUDFLARE**: Infrastructure code
4. **BATCH_4_REACT**: Frontend dashboards
5. **BATCH_5_DOCKER**: Deployment configs
6. **BATCH_6_ARCHITECTURE**: Theory & architecture
7. **BATCH_7_AUTOMATION**: Orchestration systems
8. **BATCH_8_DATABASE**: Schemas & storage
9. **BATCH_9_API**: REST/WebSocket endpoints
10. **BATCH_10_RESEARCH**: Papers & findings
11. **BATCH_11_CAREER**: Portfolio materials
12. **BATCH_12_HARDWARE**: Platform integration
13. **BATCH_13_TESTING**: Test infrastructure
14. **BATCH_14_CONFIG**: Configuration systems
15. **BATCH_15_SPECIALIZED**: GhostSlang, Policy Guard, etc.

## Wiki Structure

Extracted code is organized into:

```
ghostlink-wiki/
├── 02-architecture/          # BATCH_6
├── 03-infrastructure/
│   ├── cloudflare/           # BATCH_3
│   ├── docker/               # BATCH_5
│   └── configs/              # BATCH_14
├── 04-implementation/
│   ├── mcp-servers/          # BATCH_1
│   ├── python-backend/       # BATCH_2
│   ├── typescript-frontend/  # BATCH_4
│   ├── automation/           # BATCH_7
│   ├── hardware/             # BATCH_12
│   ├── testing/              # BATCH_13
│   └── specialized/          # BATCH_15
├── 05-database/              # BATCH_8
├── 06-api/                   # BATCH_9
├── 08-research/              # BATCH_10
└── 10-reference/
    └── career/               # BATCH_11
```

Each directory gets a `README.md` index with file listings and source references.

## State & Progress

- **State file**: `trace_root/extraction_state.json` tracks completed batches, queries, and files
- **Resumable**: Re-running the script skips already-processed queries
- **Report**: `trace_root/04_EXTRACTION_REPORT.md` summarizes progress

## Deduplication

- Content hashed with SHA-256 (16-char prefix)
- Existing files with same hash are skipped
- Duplicate detection via glob pattern matching

## Integration with Conversation Search

**TODO**: Replace the stubbed `conversation_search()` function with actual integration:

```python
def conversation_search(query: str, max_results: int = 10) -> List[Dict[str, Any]]:
    """
    Call GitHub Copilot conversation search API
    Returns: [{"content": "...", "source_url": "..."}, ...]
    """
    # Integrate with your conversation search mechanism here
    pass
```

## Example Workflow

```bash
# 1. Dry-run to preview extraction
./extraction_script.py --dry-run --batches BATCH_1_MCP

# 2. Review output paths and content

# 3. Run for real
./extraction_script.py --batches BATCH_1_MCP

# 4. Check extraction report
cat ~/ghostlink-wiki-trace/04_EXTRACTION_REPORT.md

# 5. Process all remaining batches
./extraction_script.py
```

## Troubleshooting

**State corruption**: Delete `trace_root/extraction_state.json` to start fresh

**Path issues**: Use absolute paths or set `GHOSTLINK_WIKI_ROOT`/`GHOSTLINK_TRACE_ROOT` env vars

**Duplicate detection false positives**: Check `--log-level DEBUG` to see hash calculations

**Missing code blocks**: Increase `--max-results` or refine queries in `QUERY_BATCHES`

## Next Steps

1. **Integrate conversation search**: Replace stub with real API calls
2. **Add file reference detection**: Parse `file: path/to/file.py` patterns
3. **Implement conversation metadata extraction**: Pull timestamps, authors, thread info
4. **Add progress bar**: Use `tqdm` for visual progress tracking
5. **Generate navigation**: Create inter-page links and search index

## Project Context

This is part of the GhostLink Protocol wiki construction project (Phase 2).

- **Source**: 500+ conversations from GhostLink development
- **Target**: Comprehensive technical wiki with all code, architecture, and research
- **Method**: Systematic extraction → organization → deduplication → navigation

See `01_CONSTRUCTION_PLAN.md` for full project scope.

---

**Status**: Ready for integration and production use  
**Author**: Robbie "Ghost" George  
**Last Updated**: 2025-11-25
