#!/usr/bin/env python3
"""Export the provenance summary into a CSV of top files and counts."""
import json
import csv
from pathlib import Path

PROV_SUM = Path('/Users/ghostlink/ghostlink-wiki-organized/ghostlink_provenance_summary.json')
OUT_CSV = Path('/Users/ghostlink/ghostlink-wiki-organized/ghostlink_provenance_summary.csv')

if not PROV_SUM.exists():
    print('Provenance summary not found')
    raise SystemExit(1)

with open(PROV_SUM, 'r', encoding='utf-8') as f:
    summary = json.load(f)

files = summary.get('files', [])

with open(OUT_CSV, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['file', 'match_count', 'top_term_1', 'top_term_2', 'top_term_3', 'top_term_4', 'top_term_5'])
    for item in files:
        row = [item['file'], item['match_count']] + (item.get('top_terms', [])[:5] + ['']*5)[:5]
        writer.writerow(row)

print(f'Wrote CSV to {OUT_CSV} (rows={len(files)})')
