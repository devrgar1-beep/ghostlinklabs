#!/usr/bin/env python3
"""Generate a simple dependency graph (DOT) from Python imports in selected roots."""
import os
import ast
from pathlib import Path

ROOTS = [
    "/Users/ghostlink/ghostlink-wiki-organized",
    "/Users/ghostlink/Organized/Projects"
]

nodes = set()
edges = set()

for root in ROOTS:
    if not os.path.exists(root):
        continue
    for p in Path(root).rglob('*.py'):
        try:
            text = p.read_text(encoding='utf-8', errors='ignore')
            tree = ast.parse(text)
            module_name = p.stem
            nodes.add(module_name)
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for n in node.names:
                        edges.add((module_name, n.name.split('.')[0]))
                        nodes.add(n.name.split('.')[0])
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        edges.add((module_name, node.module.split('.')[0]))
                        nodes.add(node.module.split('.')[0])
        except Exception as e:
            continue

# Write DOT
out_path = '/Users/ghostlink/ghostlink-wiki-organized/ghostlink_dependency_graph.dot'
with open(out_path, 'w', encoding='utf-8') as f:
    f.write('digraph ghostlink_dependencies {\n')
    for n in sorted(nodes):
        f.write(f'  "{n}";\n')
    for a, b in sorted(edges):
        f.write(f'  "{a}" -> "{b}";\n')
    f.write('}\n')

print(f'Wrote dependency graph to {out_path} (nodes={len(nodes)} edges={len(edges)})')
