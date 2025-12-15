# GhostLink — Computational Proteins for Distributed Intelligence

**Version:** v1.0 (November 2025)  
**Author:** Ghost

GhostLink reframes AI systems as *computational proteins*: specialized agents folding into task-specific configurations. This repo includes a camera‑ready paper, figures, a methods supplement, a conference two‑column, two executive summaries, a metrics CSV, a pitch deck, and CI/build scripts.

## Contents
- `ghostlink_whitepaper_v1_figs.tex` — main paper (figures included)
- `ghostlink_methods_supplement_v1.tex` — methods supplement
- `ghostlink_conference_two_column.tex` — two‑column version
- `ghostlink_executive_summary_onepager*.tex` — executive summaries (classic + CSV‑wired)
- `fig_*.png` — figures
- `ghostlink_metrics_v1.csv` — metrics used by CSV one‑pager
- `ghostlink_refs.bib` — BibTeX
- `ghostlink_pitch_deck_v1.pdf` — 6‑slide deck
- `Makefile` / `compile_all.sh` — build all targets into `dist/`
- `.github/workflows/latex.yml` — CI build (PDF outputs as artifacts)
- `ghostlink_artifacts_manifest_v1.json` — sizes + SHA‑256
- `ghostlink_artifacts_checklist_v1.md` — artifacts list

## Build
```bash
make all          # or: ./compile_all.sh
# outputs in ./dist
```

## arXiv
Use `ghostlink_arxiv.tex` for a lean, dependency‑light submission. Or run:
```bash
make arxiv
```
to package a source archive (requires a local TeX install).

## License
MIT (see `LICENSE`).

## Citation
See `CITATION.cff`.
