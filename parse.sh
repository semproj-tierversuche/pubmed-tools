#!/bin/bash
# extract all pmids mentioned in the data/ directory

{ ls -1 ./data/*.tsv | xargs basename -a | cut -d . -f 1 ; cat ./data/*.tsv | cut -f 1 ; } | sort -n | uniq
