.NOTINTERMEDIATE:

all: ipc out/Thesis.pdf

out/Thesis.pdf: \
		Thesis.tex Tex/* Biblio/* Style/* \
		$(patsubst %.drawio, %.pdf, $(wildcard image/*.drawio)) \
		$(patsubst %_plot.py, %.pdf, $(wildcard plot/*_plot.py)) \
		$(patsubst %.mkd, %-crop.pdf, $(wildcard snippets/*.mkd)) \
		$(patsubst %.xlsx, %.tex, $(wildcard tables/*.xlsx))
	mkdir -p out
	xelatex -output-directory=out $<
	bibtex out/Thesis.aux
	xelatex -output-directory=out $<
	xelatex -output-directory=out $<
	# xdg-open $@

%.svg: %.drawio
	drawio -x -f svg $<
%.pdf: %.drawio
	drawio -x -f pdf --crop $<
%.png: %.drawio
	drawio -x -f png $< --scale 3

.PHONY: ipc
ipc: $(addprefix plot/ucache_ipc, $(addsuffix .pdf, 0 1 2 3 4))

plot/ucache_ipc%.svg: plot/ucache_ipc_plot.py plot/ucache_ipc.xlsx plot/head.py
	$< -f $(word 2,$^) -m $(patsubst ucache_ipc%.svg,%,$(@F))
plot/ucache_ipc%.pdf: plot/ucache_ipc%.svg
	rsvg-convert -f pdf -o $@ $<

plot/%.svg: plot/%_plot.py plot/%.xlsx plot/head.py
	$< -f $(word 2,$^)
plot/insts_inflt_breakdown_%.svg: plot/insts_inflt_breakdown_%_plot.py \
	$(wildcard plot/insts_inflt_2017/*.csv) \
	plot/fusion_combined_merged_.xlsx \
	plot/insts_inflt_2017_combined.xlsx \
	plot/jcc_2017.xlsx \
	plot/head.py plot/combine.py
	$< -o $@
plot/%.pdf: plot/%.svg
	rsvg-convert -f pdf -o $@ $<
plot/%.png: plot/%.pdf
	pdftoppm -png -singlefile -r 300 $< $(patsubst %.png, %, $@)


png: $(patsubst %.pdf, %.png, $(wildcard plot/*.pdf))

snippets/%.pdf: snippets/%.mkd
	pandoc -V pagestyle=empty -o $@ $<
snippets/%-crop.pdf: snippets/%.pdf
	pdfcrop $<

tables/%.tex tables/%.html &: tables/%.py tables/%.xlsx
	$< -f $(word 2,$^)

%.slides.html: %.slides.md \
	$(patsubst %.drawio, %.png, $(wildcard image/*.drawio)) \
	$(patsubst %.pdf, %.png, $(wildcard plot/*.pdf)) \
	$(patsubst %_plot.py, %.pdf, $(wildcard plot/*_plot.py))
	REPOROOT=./markdown_revealjs ./markdown_revealjs/bin/revealjs.sh $<

clean:
	rm -rf out/
clean-all: clean
	rm -f pictures/*.svg
	rm -f pictures/*.pdf
	rm -f plot/*.svg
	rm -f plot/*.pdf
