#!/usr/bin/env python3
"""Apply refactor replacements from dry-run mapping.

This script is cautious: It uses the /ghostlink_refactor_dryrun.json to apply replacements
and by default operates in dry-run mode. The --apply flag actually modifies files, backing up originals
into .bak files; the process is non-destructive because backups are kept.
"""
import argparse
import json
from pathlib import Path
import shutil

WORK_DIR = Path('/Users/ghostlink/ghostlink-wiki-organized')
DRYRUN_PATH = WORK_DIR / 'ghostlink_refactor_dryrun.json'

parser = argparse.ArgumentParser("Apply refactor suggested mappings from dry-run report")
parser.add_argument('--apply', action='store_true', help='Actually perform replacements')
parser.add_argument('--max', type=int, default=0, help='Limit changes to first N replacements (0=all)')
args = parser.parse_args()

if not DRYRUN_PATH.exists():
    print('Dry-run report not found:', DRYRUN_PATH)
    raise SystemExit(1)

with open(DRYRUN_PATH, encoding='utf-8') as f:
    dryrun = json.load(f)

replacements = dryrun.get('replacements', [])
if args.max > 0:
    replacements = replacements[:args.max]

changes_count = 0
for r in replacements:
    path = Path(r['file'])
    old = r['old']
    new = r['suggested_new']
    try:
        if not path.exists():
            continue
        text = path.read_text(encoding='utf-8', errors='ignore')
        if old not in text:
            continue

        print(f"Would replace: {old} -> {new} in {path}:{r['line']}")

        if args.apply:
            bak = path.with_suffix(path.suffix + '.bak')
            if not bak.exists():
                shutil.copy2(path, bak)
            new_text = text.replace(old, new)
            path.write_text(new_text, encoding='utf-8')
            changes_count += 1

    except Exception as e:
        print('Error processing', path, e)

if args.apply:
    print(f"Applied changes: {changes_count}")
else:
    print(f"Dry-run: suggested replacements: {len(replacements)}")

print('Done')
