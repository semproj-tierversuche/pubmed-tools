#!/usr/bin/env python3
import os
import sys

from elasticsearch5 import Elasticsearch

es = Elasticsearch()
es_options = {
        "index": "article_test",
        "doc_type": "article" }

query = {"query": {"match_all": {}}}

es.delete_by_query(**es_options, body=query)
