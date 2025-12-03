#!/usr/bin/env python3
"""Summarize the provenance index into per-file counts and top terms."""
from collections import Counter, defaultdict
import json

PROV_PATH = '/Users/ghostlink/ghostlink-wiki-organized/ghostlink_provenance_index.json'
OUT_SUMMARY = '/Users/ghostlink/ghostlink-wiki-organized/ghostlink_provenance_summary.json'

with open(PROV_PATH, encoding='utf-8') as f:
    prov = json.load(f)

matches = prov.get('matches', [])

file_counts = defaultdict(int)
file_terms = defaultdict(Counter)

for m in matches:
    path = m.get('file')
    file_counts[path] += 1
    # naive term tokenization
    tokens = m.get('snippet','').split()
    for t in tokens:
        file_terms[path][t] += 1

# Build summary
summary = {'generated_at': prov.get('generated_at'), 'files': []}
for path, count in sorted(file_counts.items(), key=lambda x: -x[1]):
    top_terms = [t for t, _ in file_terms[path].most_common(5)]
    summary['files'].append({'file': path, 'match_count': count, 'top_terms': top_terms})

with open(OUT_SUMMARY, 'w', encoding='utf-8') as f:
    json.dump(summary, f, indent=2)

print(f"Wrote provenance summary to {OUT_SUMMARY} (files={len(summary['files'])})")
