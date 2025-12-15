#!/usr/bin/env python3
import json
import sys
import re
from pathlib import Path

# Script to toggle YOLO / master auto-approve flags for installed extensions in VS Code settings
# Usage:
#   python3 enable-yolo-offline.py [extensions_dir] [settings_path] [--enable true|false] [--dry-run]

extensions_dir = Path(sys.argv[1]) if len(sys.argv) > 1 and not sys.argv[1].startswith('--') else Path.home() / '.vscode' / 'extensions'
settings_path = Path(sys.argv[2]) if len(sys.argv) > 2 and not sys.argv[2].startswith('--') else Path.home() / 'Library' / 'Application Support' / 'Code' / 'User' / 'settings.json'

enable = True
if '--enable' in sys.argv:
    try:
        idx = sys.argv.index('--enable')
        enable = sys.argv[idx + 1].lower() in ('true', '1', 'yes')
    except Exception:
        enable = True

dry_run = '--dry-run' in sys.argv

pattern_keys = re.compile(r'yolo|autoapprove|auto_approve|auto-approve|masterauto|master_auto|master-auto|enableAutoApprove|autoaccept|auto_accept|auto-accept', re.IGNORECASE)

if not extensions_dir.exists():
    print('Extensions dir not found:', extensions_dir)
    sys.exit(1)

settings = {}
if settings_path.exists():
    try:
        with open(settings_path, 'r', encoding='utf-8') as f:
            settings = json.load(f)
    except Exception:
        settings = {}

changed = {}
for ext in extensions_dir.iterdir():
    pkg = ext / 'package.json'
    if not pkg.exists():
        continue
    try:
        with open(pkg, 'r', encoding='utf-8') as f:
            pkg_json = json.load(f)
    except Exception:
        continue
    contrib = (pkg_json.get('contributes') or {}).get('configuration') or {}
    # configuration can be an object or an array of objects
    props = {}
    if isinstance(contrib, dict):
        props = (contrib or {}).get('properties') or {}
    elif isinstance(contrib, list):
        for c in contrib:
            if isinstance(c, dict):
                p = (c.get('properties') or {})
                if isinstance(p, dict):
                    props.update(p)
    for k, v in props.items():
        title = (v.get('title') or '') if isinstance(v, dict) else ''
        desc = (v.get('description') or '') if isinstance(v, dict) else ''
        if pattern_keys.search(k) or pattern_keys.search(title) or pattern_keys.search(desc):
            changed[k] = True
            settings[k] = enable

# Save / print
print('Found keys to toggle:', len(changed))
if len(changed) > 0:
    for k in changed.keys():
        print(' -', k)

if dry_run:
    print('Dry run enabled, not writing changes to', settings_path)
else:
    # Backup
    try:
        backup = settings_path.with_suffix(settings_path.suffix + '.bak')
        if settings_path.exists():
            with open(backup, 'w', encoding='utf-8') as bf:
                json.dump(settings, bf, indent=2, ensure_ascii=False)
    except Exception:
        pass
    # Write
    with open(settings_path, 'w', encoding='utf-8') as f:
        json.dump(settings, f, indent=2, ensure_ascii=False)
    print('Written changes to', settings_path)

print('Done')
