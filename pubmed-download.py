#!/usr/bin/env python3
# requires at least python 3.4
import argparse
import os
from pathlib import Path
import sys
import time

import requests
from requests import Request, Session

# parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("input_file", help="a file containing one or more "
    + "pmids, separated by newlines")
parser.add_argument("output_dir", help="the directory in which to store "
    + "the downloaded XML file(s)")
parser.add_argument("-c", "--continue", dest="cont",
        help="don't quit when an operation fails", action="store_true")
parser.add_argument("-o", "--overwrite",
        help="overwrite existing files", action="store_true")
args = parser.parse_args()

url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
params = {"db"      : "pubmed",
          "retmode" : "xml" }
session = Session()
req = Request("GET", url, params=params)

# read the pmids to be downloaded
with open(args.input_file) as f:
    pmids = f.readlines()

print("Will download {} documents.".format(len(pmids)))

pmids = [int(pmid) for pmid in pmids]

for pmid in pmids:
    file_path = Path(args.output_dir, str(pmid) + ".xml")
    if file_path.exists() and not args.overwrite:
        print("{} already exists. Skipping.".format(file_path))
        continue

    print("Downloading pubmed document #{}... ".format(pmid), end='')
    req.params["id"] = pmid
    prepped = req.prepare()
    try:
        response = session.send(prepped)
    except requests.exceptions.ConnectionError:
        # handle API rate limiting
        print("HTTP connection failed. Retrying in 3 seconds...")
        time.sleep(3)
        response = session.send(prepped)

    if response.status_code != 200:
        if args.cont:
            continue
        else:
            response.raise_for_status()

    with file_path.open("w") as f:
        f.write(response.text)
    print("successful.")

    # pubmed doesn't like too many requests at once, so we wait a bit
    time.sleep(.4)
