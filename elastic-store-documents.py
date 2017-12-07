#!/usr/bin/env python3
import os

from elasticsearch5 import Elasticsearch

data_dir = "data/documents/"

es = Elasticsearch()
es_options = {
        "index": "article_test",
        "doc_type": "article" }

for file in os.listdir(data_dir):
    if not file.endswith(".json"):
        continue
    path = os.path.join(data_dir, file)
    with open(path) as f:
        body = f.read()
    print("Storing document from {}...".format(file))
    es.index(**es_options, body=body)
