TEX=pdflatex
FLAGS=-interaction=nonstopmode -halt-on-error

all: paper methods conference onepager onepager_csv deck reviewer_pack dist

paper:
	$(TEX) $(FLAGS) ghostlink_whitepaper_v1_figs.tex
	$(TEX) ghostlink_whitepaper_v1_figs.tex

methods:
	$(TEX) $(FLAGS) ghostlink_methods_supplement_v1.tex
	$(TEX) ghostlink_methods_supplement_v1.tex

conference:
	$(TEX) $(FLAGS) ghostlink_conference_two_column.tex
	$(TEX) ghostlink_conference_two_column.tex

onepager:
	$(TEX) $(FLAGS) ghostlink_executive_summary_onepager.tex
	$(TEX) ghostlink_executive_summary_onepager.tex

onepager_csv:
	$(TEX) $(FLAGS) ghostlink_executive_summary_onepager_csv.tex
	$(TEX) ghostlink_executive_summary_onepager_csv.tex

reviewer_pack: paper methods
	$(TEX) $(FLAGS) reviewer_pack.tex
	$(TEX) reviewer_pack.tex

deck:
	@echo "Pitch deck already provided as PDF: ghostlink_pitch_deck_v1.pdf"

dist: paper methods conference onepager onepager_csv reviewer_pack
	mkdir -p dist
	cp -f ghostlink_whitepaper_v1_figs.pdf dist/
	cp -f ghostlink_methods_supplement_v1.pdf dist/
	cp -f ghostlink_conference_two_column.pdf dist/
	cp -f ghostlink_executive_summary_onepager.pdf dist/
	cp -f ghostlink_executive_summary_onepager_csv.pdf dist/
	cp -f reviewer_pack.pdf dist/
	cp -f ghostlink_pitch_deck_v1.pdf dist/
	cp -f fig_*.png dist/
	cp -f ghostlink_metrics_v1.csv dist/
	cp -f ghostlink_refs.bib dist/
	cp -f ghostlink_artifacts_checklist_v1.md dist/
	cp -f ghostlink_artifacts_manifest_v1.json dist/
	cp -f README_compile.txt dist/
# optional: package dist
#	zip -r ghostlink_dist_v1.zip dist

clean:
	rm -f *.aux *.log *.out *.toc *.lof *.lot *.bbl *.blg *.fls *.fdb_latexmk *.synctex.gz
	rm -f ghostlink_whitepaper_v1_figs.pdf ghostlink_methods_supplement_v1.pdf ghostlink_conference_two_column.pdf
	rm -f ghostlink_executive_summary_onepager.pdf ghostlink_executive_summary_onepager_csv.pdf reviewer_pack.pdf
	rm -rf dist


dist-zip: dist
	zip -r ghostlink_dist_v1.zip dist

arxiv:
	./prep_arxiv_source.sh ghostlink_arxiv_source.tar.gz

