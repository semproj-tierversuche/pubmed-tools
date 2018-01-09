#!/bin/bash
# This script converts all PubMed XML files in ../data/documents/ and
# converts them to BioC with our XSL transformation. The resulting files
# are checked for well-formedness and conformance with the BioC DTD with
# xmllint and then saved to ../data/documents with a ".bioc-generated.xml"
# suffix.
set -eu
shopt -s extglob
for file in ../data/documents/+([0-9]).xml; do
	target=${file/%.xml/.bioc-generated.xml}
	xsltproc --nonet --path . --stringparam article-date `date +%Y%m%d` pubmed2bioc.xsl "$file" | xmllint --dtdvalid BioC.dtd - > $target
	# the following line can be uncommented to manually check the 
	# differences between the BioC we generate and the BioC from the
	# PubMed API
	# diff ${file/%.xml/.bioc.xml} $target || true
done
