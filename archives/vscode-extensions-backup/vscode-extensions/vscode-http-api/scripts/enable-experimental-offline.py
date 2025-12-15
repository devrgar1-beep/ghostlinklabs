#!/usr/bin/env python3
import json
import sys
import re
from pathlib import Path

# Simple script to scan installed VSCode extensions and enable experimental flags in user settings
# Usage:
#   python3 enable-experimental-offline.py [extensions_dir] [settings_path]
# defaults: ~/.vscode/extensions and macOS settings: ~/Library/Application Support/Code/User/settings.json

extensions_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.home() / '.vscode' / 'extensions'
settings_path = Path(sys.argv[2]) if len(sys.argv) > 2 else Path.home() / 'Library' / 'Application Support' / 'Code' / 'User' / 'settings.json'
dry_run = '--dry-run' in sys.argv

if not extensions_dir.exists():
    print('Extensions directory not found:', extensions_dir)
    sys.exit(1)

if not settings_path.exists():
    print('Settings file not found, creating:', settings_path)
    settings_path.parent.mkdir(parents=True, exist_ok=True)
    settings = {}
else:
    try:
        with open(settings_path, 'r', encoding='utf-8') as f:
            settings = json.load(f)
    except Exception:
        settings = {}

pattern = re.compile(r'experimental|preview|beta|proposed|enablePreview', re.IGNORECASE)

changed = {}
for ext in extensions_dir.iterdir():
    package_json = ext / 'package.json'
    if not package_json.exists():
        continue
    try:
        with open(package_json, 'r', encoding='utf-8') as f:
            pkg = json.load(f)
    except Exception:
        continue
    contrib = (pkg.get('contributes') or {}).get('configuration') or {}
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
        if pattern.search(k) or pattern.search(title) or pattern.search(desc):
            # Enable
            settings[k] = True
            changed[k] = {
                'extension': pkg.get('name') or pkg.get('publisher') or ext.name,
                'package_name': pkg.get('name'),
                'title': title,
                'description': desc
            }

if dry_run:
    print('DRY RUN: no changes will be written to', settings_path)
    print('Would update settings keys:', list(changed.keys()))
else:
    # Save settings (create backup first)
    try:
        backup = settings_path.with_suffix(settings_path.suffix + '.bak')
        if settings_path.exists():
            with open(backup, 'w', encoding='utf-8') as bf:
                json.dump(settings, bf, indent=2, ensure_ascii=False)
    except Exception:
        pass
    with open(settings_path, 'w', encoding='utf-8') as f:
        json.dump(settings, f, indent=2, ensure_ascii=False)

print('Updated settings at', settings_path)
print('Changed keys:', len(changed))
for k, v in changed.items():
    print(k, '->', v.get('extension') or v.get('package_name'))

print('Done.')
