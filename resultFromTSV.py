#!/usr/bin/env python3
import argparse
import json
import os
from pathlib import Path
# TODO remove
from pprint import pprint
import sys

parser = argparse.ArgumentParser()
parser.add_argument("input_file", help="a TSV file containing training data")
parser.add_argument("data_dir", help="where JSON files for PMIDs are stored")
args = parser.parse_args()

def json_for_pmid(pmid):
    json_path = Path(args.data_dir, pmid + ".json")
    with json_path.open() as f:
        record = json.load(f)
    return record

with open(args.input_file) as f:
    lines = f.readlines()

lines = [line.split('\t') for line in lines]
lines = [line for line in lines if line[3].strip() == "Relevant"]

#pprint(lines)
#sys.exit(0)

# translation for animal table results
t_animal_test = {"Ja": "yes", "Nein": "no", "Sowohl_Als_Auch": "both"}
# made-up relevance score
relevance = .99

results = []
for line in lines:
    record = json_for_pmid(line[0])
    row = {"Record": record}
    row["Matching"] = { "AnimalTest": t_animal_test[line[1]],
                        "Similar": (line[2] == "Aehnlich"),
                        "Relevance": round(relevance, 2) }
    results.append(row)
    relevance -= .01

# the name of the TSV file contains the PMID for which it contains results
origin_pmid = os.path.basename(args.input_file).split('.')[0]
origin_record = json_for_pmid(origin_pmid)

# construct the response object
response = {}
response["Origin"] = origin_record
response["Results"] = results

print(json.dumps(response))
