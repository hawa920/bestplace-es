import sys
import json
import requests
from elasticsearch import Elasticsearch
from elasticsearch import helpers


with open('./bpsample.json') as f:
  raw_data = json.load(f)


acts = []
cnter = 0

for iter in raw_data["posts"]:

  act = {

    "_index" : "bpintaiwan",
    "_type" : "posts",
    "_id" : cnter,

    "_source" : {

      "postURL" : iter["url"],
      "imgURL" : iter["urlImage"],
      "description" : iter["description"],
      "date" : iter["date"]

    }
  }
  acts.append(act)
  cnter += 1

es = Elasticsearch()
helpers.bulk(es, acts)
