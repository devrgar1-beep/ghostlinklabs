#!/usr/bin/env python3
"""Filter a large DOT file to produce a focused graph around core modules."""
import re
from pathlib import Path

SRC = '/Users/ghostlink/ghostlink-wiki-organized/ghostlink_dependency_graph.dot'
OUT = '/Users/ghostlink/ghostlink-wiki-organized/ghostlink_dependency_graph_filtered.dot'

CORE = set(['design_clarity_os','mirror_comprehension','multi_agent_engine','evolutionary_intelligence','ghostlink_backend'])

if not Path(SRC).exists():
    print('Source DOT not found')
    raise SystemExit(1)

with open(SRC, 'r', encoding='utf-8') as f:
    lines = f.readlines()

nodes = set()
edges = []
node_re = re.compile(r'"([^"]+)";')
edge_re = re.compile(r'"([^"]+)" -> "([^"]+)";')

for L in lines:
    m = edge_re.search(L)
    if m:
        a, b = m.group(1), m.group(2)
        edges.append((a,b))
        nodes.add(a); nodes.add(b)

# Keep edges where a or b in CORE or connected to CORE
keep = []
for a,b in edges:
    if a in CORE or b in CORE:
        keep.append((a,b))

# Also include immediate neighbors
neighbors = set()
for a,b in keep:
    neighbors.add(a); neighbors.add(b)

filtered_nodes = set(neighbors)
filtered_edges = [e for e in edges if e[0] in filtered_nodes and e[1] in filtered_nodes]

with open(OUT, 'w', encoding='utf-8') as f:
    f.write('digraph ghostlink_dependencies_filtered {\n')
    for n in sorted(filtered_nodes):
        f.write(f'  "{n}";\n')
    for a,b in filtered_edges:
        f.write(f'  "{a}" -> "{b}";\n')
    f.write('}\n')

print(f'Wrote filtered DOT to {OUT} (nodes={len(filtered_nodes)} edges={len(filtered_edges)})')
