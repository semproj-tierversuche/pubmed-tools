#!/bin/bash
set -eu
mkdir -p data/results
for file in data/*.tsv; do
	result_file="data/results/$(basename ${file/%.tsv/.json})"
	./resultFromTSV.py "$file" data/documents | jsonlint -f > "$result_file"
done
