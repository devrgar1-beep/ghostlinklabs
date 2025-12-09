# swarm_analysis.py

from __future__ import annotations
import math
from dataclasses import dataclass
from typing import List, Tuple, Optional

SYMBOL_MAP = {
    "·": 0,
    "░": 1,
    "▒": 2,
    "▓": 3,
    "█": 4,
}

REVERSE_SYMBOL_MAP = {v: k for k, v in SYMBOL_MAP.items()}


@dataclass
class SwarmStats:
    grid: List[List[int]]         # 8x8 integer grid
    mean: float
    std: float
    total: int
    high_cells: int               # cells with value >= 3
    cluster_count: int            # number of high-activity clusters
    cluster_sizes: List[int]      # sizes of each cluster
    uuid: Optional[str] = None    # optional run UUID / tag
    cycle: Optional[int] = None   # optional cycle index

    def as_dict(self) -> dict:
        return {
            "mean": self.mean,
            "std": self.std,
            "total": self.total,
            "high_cells": self.high_cells,
            "cluster_count": self.cluster_count,
            "cluster_sizes": self.cluster_sizes,
            "uuid": self.uuid,
            "cycle": self.cycle,
        }


def parse_swarm_block(lines: List[str]) -> List[List[int]]:
    """
    Parse an 8x8 swarm grid from a block of log lines.
    We scan each line and collect characters that are in SYMBOL_MAP,
    ignoring all other characters (borders, pipes, spaces, etc.).
    """
    grid: List[List[int]] = []

    for line in lines:
        row_vals: List[int] = []
        for ch in line:
            if ch in SYMBOL_MAP:
                row_vals.append(SYMBOL_MAP[ch])
        if row_vals:
            # If we got more than 8 symbols, truncate conservatively
            if len(row_vals) >= 8:
                grid.append(row_vals[:8])
        if len(grid) == 8:
            break

    if len(grid) != 8:
        # Fallback for empty or malformed blocks, return empty grid or raise
        # For robustness in this specific context, let's return a zero grid if we fail
        # but raising is better for debugging. The user code raises.
        if len(grid) == 0:
             return [[0]*8 for _ in range(8)]
        raise ValueError(f"Expected 8 rows in swarm grid, got {len(grid)}")

    # Sanity: pad rows if shorter
    for r in grid:
        if len(r) < 8:
            r.extend([0] * (8 - len(r)))

    return grid


def compute_basic_stats(grid: List[List[int]]) -> Tuple[float, float, int, int]:
    values: List[int] = [cell for row in grid for cell in row]
    n = len(values)
    if n == 0:
        return 0.0, 0.0, 0, 0

    total = sum(values)
    mean = total / n
    var = sum((v - mean) ** 2 for v in values) / n
    std = math.sqrt(var)
    high_cells = sum(1 for v in values if v >= 3)
    return mean, std, total, high_cells


def _neighbors(i: int, j: int, size: int = 8):
    for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        ni, nj = i + di, j + dj
        if 0 <= ni < size and 0 <= nj < size:
            yield ni, nj


def find_clusters(grid: List[List[int]], threshold: int = 3) -> Tuple[int, List[int]]:
    """
    Find connected clusters of cells with value >= threshold.
    Connectivity is 4-neighbour (up/down/left/right).
    """
    size = 8
    visited = [[False] * size for _ in range(size)]
    cluster_sizes: List[int] = []

    for i in range(size):
        for j in range(size):
            if visited[i][j]:
                continue
            if grid[i][j] < threshold:
                continue

            # BFS / DFS
            stack = [(i, j)]
            visited[i][j] = True
            cnt = 0

            while stack:
                ci, cj = stack.pop()
                cnt += 1
                for ni, nj in _neighbors(ci, cj, size=size):
                    if not visited[ni][nj] and grid[ni][nj] >= threshold:
                        visited[ni][nj] = True
                        stack.append((ni, nj))

            cluster_sizes.append(cnt)

    return len(cluster_sizes), cluster_sizes


def analyze_swarm_block(lines: List[str],
                        uuid: Optional[str] = None,
                        cycle: Optional[int] = None) -> SwarmStats:
    """
    Full analysis for a single 8x8 swarm map.
    """
    grid = parse_swarm_block(lines)
    mean, std, total, high_cells = compute_basic_stats(grid)
    cluster_count, cluster_sizes = find_clusters(grid, threshold=3)

    return SwarmStats(
        grid=grid,
        mean=mean,
        std=std,
        total=total,
        high_cells=high_cells,
        cluster_count=cluster_count,
        cluster_sizes=cluster_sizes,
        uuid=uuid,
        cycle=cycle,
    )


def l1_distance(grid_a: List[List[int]], grid_b: List[List[int]]) -> int:
    """
    L1 distance (sum of absolute cell-wise differences)
    between two 8x8 grids.
    """
    if len(grid_a) != 8 or len(grid_b) != 8:
        raise ValueError("Both grids must be 8x8")

    dist = 0
    for i in range(8):
        if len(grid_a[i]) != 8 or len(grid_b[i]) != 8:
            raise ValueError("Both grids must be 8x8")
        for j in range(8):
            dist += abs(grid_a[i][j] - grid_b[i][j])
    return dist
