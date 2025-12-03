#!/usr/bin/env python3
"""Produce a dry-run mapping of legacy terms to neutral names using the provenance index."""
import json
from collections import defaultdict

PROV_PATH = '/Users/ghostlink/ghostlink-wiki-organized/ghostlink_provenance_index.json'
OUT_MAPPING = '/Users/ghostlink/ghostlink-wiki-organized/ghostlink_legacy_mapping.json'
OUT_DRYRUN = '/Users/ghostlink/ghostlink-wiki-organized/ghostlink_refactor_dryrun.json'

# Suggest mapping (editable)
SUGGESTED = {
    'Wraithgate': 'secure_gateway',
    'WraithGate': 'secure_gateway',
    'wraithgate': 'secure_gateway',
    'GhostLinkLabs': 'ghostlink_docs',
    'GhostLink': 'GhostLink',
    'Sentinel': 'sentinel_watchdog',
    'Dak': 'dak_kill_switch',
    'Lumara': 'lumara_profile'
}

with open(PROV_PATH, 'r', encoding='utf-8') as f:
    prov = json.load(f)

matches = prov.get('matches', [])

# Aggregate by term occurrences (simple substring check)
term_hits = defaultdict(list)
for m in matches:
    line = m.get('snippet','')
    for term in SUGGESTED.keys():
        if term in line:
            term_hits[term].append({'file': m['file'], 'line': m['line'], 'snippet': m['snippet']})

# Produce mapping file
mapping_out = {'generated_at': prov.get('generated_at'), 'suggested_mapping': SUGGESTED}
with open(OUT_MAPPING, 'w', encoding='utf-8') as f:
    json.dump(mapping_out, f, indent=2)

# Dry-run: list every occurrence with suggested replacement
dryrun = {'generated_at': prov.get('generated_at'), 'replacements': []}
for term, hits in term_hits.items():
    replacement = SUGGESTED.get(term)
    for h in hits:
        dryrun['replacements'].append({
            'file': h['file'], 'line': h['line'], 'old': term, 'suggested_new': replacement, 'snippet': h['snippet']
        })

with open(OUT_DRYRUN, 'w', encoding='utf-8') as f:
    json.dump(dryrun, f, indent=2)

print(f"Wrote mapping to {OUT_MAPPING} and dry-run report to {OUT_DRYRUN} (replacements={len(dryrun['replacements'])})")
