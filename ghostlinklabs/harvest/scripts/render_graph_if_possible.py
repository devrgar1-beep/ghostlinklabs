#!/usr/bin/env python3
"""Attempt to render dependency graphs to PNG using dot (Graphviz) if available.

If Graphviz 'dot' is not found, output instructions for the user.
"""
import shutil
from pathlib import Path
import subprocess

SRC = Path('/Users/ghostlink/ghostlink-wiki-organized/ghostlink_dependency_graph_filtered.dot')
OUT = Path('/Users/ghostlink/ghostlink-wiki-organized/ghostlink_dependency_graph_filtered.png')

if not SRC.exists():
    print('Source DOT not found:', SRC)
    raise SystemExit(1)

dot_cmd = shutil.which('dot')

if not dot_cmd:
    print("Graphviz 'dot' not found on PATH. To render, install Graphviz (e.g., 'brew install graphviz' on macOS) and re-run this script.")
else:
    try:
        subprocess.run([dot_cmd, '-Tpng', str(SRC), '-o', str(OUT)], check=True)
        print(f'Rendered PNG to {OUT}')
    except subprocess.CalledProcessError as e:
        print('dot rendering failed:', e)
