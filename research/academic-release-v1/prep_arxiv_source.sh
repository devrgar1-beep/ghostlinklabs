#!/usr/bin/env bash
set -euo pipefail
# Prepare arXiv-friendly source bundle
OUT=${1:-ghostlink_arxiv_source.tar.gz}
TEX=ghostlink_arxiv.tex
FIGS="fig_funnel.png fig_motifs.png fig_active_site.png fig_ablations.png fig_pbft_timing.png fig_metrics_glance.png"
echo "Packing $OUT"
tar -czf "$OUT" $TEX $FIGS README.md LICENSE
echo "Done."
