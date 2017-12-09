#!/usr/bin/env python3
# requires at least python 3.4
import argparse
import os
from pathlib import Path
import sys
import time

import requests
from requests import Request, Session

def document_for_pmid(pmid, format="xml"):
    if format == "bioc":
        url = "https://www.ncbi.nlm.nih.gov/bionlp/RESTful/pubmed.cgi/BioC_xml/{:d}/unicode"
        url = url.format(pmid)
        params = {}
    else:
        url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
        params = {"db"      : "pubmed",
                  "retmode" : "xml",
                  "id"      : int(pmid) }
    req = Request("GET", url, params=params)
    req = req.prepare()
    try:
        response = session.send(req)
    except requests.exceptions.ConnectionError:
        # handle API rate limiting
        print("HTTP connection failed. Retrying in 3 seconds...")
        time.sleep(3)
        response = session.send(req)

    response.raise_for_status()

    return response.text

# parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("input_file", help="a file containing one or more "
    + "pmids, separated by newlines")
parser.add_argument("output_dir", help="the directory in which to store "
    + "the downloaded XML file(s)")
parser.add_argument("-b", "--bioc", help="download BioC XML",
        action="store_true")
parser.add_argument("-c", "--continue", dest="cont",
        help="don't quit when an operation fails", action="store_true")
parser.add_argument("-o", "--overwrite",
        help="overwrite existing files", action="store_true")
args = parser.parse_args()

# requests setup
session = Session()

if args.bioc:
    format = "bioc"
    ext = ".bioc.xml"
else:
    format = "xml"
    ext = ".xml"

# read the pmids to be downloaded
with open(args.input_file) as f:
    pmids = f.readlines()

print("Will download {} documents.".format(len(pmids)))

pmids = [int(pmid) for pmid in pmids]

for pmid in pmids:
    file_path = Path(args.output_dir, str(pmid) + ext)
    if file_path.exists() and not args.overwrite:
        print("{} already exists. Skipping.".format(file_path))
        continue

    print("Downloading pubmed document #{}... ".format(pmid), end='')

    text = document_for_pmid(pmid, format)

    with file_path.open("w") as f:
        f.write(text)
    print("successful.")

    # pubmed doesn't like too many requests at once, so we wait a bit
    time.sleep(.4)
