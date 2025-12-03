#!/usr/bin/env python3
"""Produce a provenance index for legacy GhostLink terms.

Search roots (configurable) for files and record term hits with context.
"""
import json
import os
from pathlib import Path
import re

ROOTS = [
    "/Users/ghostlink/ghostlink-wiki-organized",
    "/Users/ghostlink/Organized",
    "/Users/ghostlink/Documents/GitHub/ghostlinklabs_redacted_backup_20251127T150532"
]
TERMS = [
    r"Wraithgate",
    r"WraithGate",
    r"wraithgate",
    r"Sentinel",
    r"Dak",
    r"Lumara",
    r"GhostLink",
    r"GhostLinkLabs",
]
EXTS = {'.py', '.md', '.txt', '.json', '.html', '.csv'}

out = {
    'generated_at': None,
    'roots': ROOTS,
    'matches': []
}

import datetime

out['generated_at'] = datetime.datetime.utcnow().isoformat() + 'Z'

term_regex = re.compile('|'.join(TERMS))

for root in ROOTS:
    if not os.path.exists(root):
        continue
    for dirpath, _dirnames, filenames in os.walk(root):
        # skip hidden dirs
        if any(part.startswith('.') for part in Path(dirpath).parts):
            continue
        for fn in filenames:
            ext = os.path.splitext(fn)[1]
            if ext.lower() not in EXTS:
                continue
            path = os.path.join(dirpath, fn)
            try:
                with open(path, encoding='utf-8', errors='ignore') as f:
                    for i, line in enumerate(f, start=1):
                        if term_regex.search(line):
                            snippet = line.strip()
                            out['matches'].append({
                                'file': path,
                                'line': i,
                                'snippet': snippet
                            })
            except Exception:
                # skip unreadable files
                continue

# Write output
out_path = '/Users/ghostlink/ghostlink-wiki-organized/ghostlink_provenance_index.json'
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(out, f, indent=2)

print(f"Wrote provenance index with {len(out['matches'])} matches to {out_path}")
