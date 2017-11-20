#!/bin/bash
set -eu
./pubmed-download.py data/pmids data/documents
for file in data/documents/*.xml; do
	xsltproc pubmed2json.xsl "$file" | jsonlint -f > ${file/%.xml/.json}
done
