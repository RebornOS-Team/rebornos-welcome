# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = source
BUILDDIR      = build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
# make html will call html: in Makefile to output HTML from .md and .rst
html:
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(0)

# make latexpdf will call latexpdf: in Makefile to output PDF from .rst only
latexpdf:
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(0)

# make latex will call latex: in Makefile to run pandoc to make PDF from .md only.
# latex:
# 	@pandoc --toc --latex-engine=pdflatex -V fontfamily="cmbright" -V geometry=margin=0.5in -V documentclass="book" -o /build/API_documentation.pdf -s Introduction.md Thank_You.md Copyright.md
