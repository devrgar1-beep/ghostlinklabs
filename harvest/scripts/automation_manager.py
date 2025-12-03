#!/usr/bin/env python3
"""Automation manager: orchestrates the whole pipeline.

Commands:
  run_all     : run full pipeline (dry-run only for refactor)
  apply_refactor : apply refactor changes (dangerous; run only when ready)
  render_graphs  : try to render graphs to PNG (requires Graphviz)
"""
import argparse
from pathlib import Path
import subprocess

SCRIPTS = Path('/Users/ghostlink/scripts')

parser = argparse.ArgumentParser('GhostLink automation manager')
parser.add_argument('command', choices=['run_all','apply_refactor','render_graphs'])
parser.add_argument('--max', type=int, default=0, help='Limit replacements in apply_refactor')
parser.add_argument('--apply', action='store_true', help='Actually apply replacements (mandatory for apply_refactor)')
args = parser.parse_args()

if args.command == 'run_all':
    steps = [
        'python3 /Users/ghostlink/scripts/provenance_index.py',
        'python3 /Users/ghostlink/scripts/generate_dependency_graph.py',
        'python3 /Users/ghostlink/scripts/provenance_summary.py',
        'python3 /Users/ghostlink/scripts/legacy_mapping.py',
        'python3 /Users/ghostlink/scripts/filter_dependency_graph.py',
        'python3 /Users/ghostlink/scripts/generate_viewer.py',
        'python3 /Users/ghostlink/ghostlink-wiki-organized/ghostlink_test_harness.py',
        'python3 /Users/ghostlink/scripts/provenance_csv_export.py'
    ]
    for s in steps:
        print('Running:', s)
        subprocess.run(s, shell=True)

elif args.command == 'apply_refactor':
    cmd = 'python3 /Users/ghostlink/scripts/apply_refactor.py'
    if args.max > 0:
        cmd += f' --max {args.max}'
    if args.apply:
        cmd += ' --apply'
    else:
        print('Warning: running dry-run. Supply --apply to actually modify files.')
    print('Running:', cmd)
    subprocess.run(cmd, shell=True)

elif args.command == 'render_graphs':
    subprocess.run('python3 /Users/ghostlink/scripts/render_graph_if_possible.py', shell=True)

print('Done')
