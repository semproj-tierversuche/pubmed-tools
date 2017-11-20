## Download PubMed records from file
    ./pubmed-download.py data/pmids data/documents/

## Convert a single PubMed XML record to JSON
*See `ISSUES.md`.*

    xsltproc -o 23367398.json pubmed2json.xsl data/documents/23367398.xml
