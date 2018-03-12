import os
import sys
import json
import requests
from elasticsearch import Elasticsearch
from elasticsearch import helpers


acts = []
cnter = 0

# This code will refresh (update) all the documents in the index

for files in os.listdir('./bfdata'):
  if files.endswith('.json'):

    # Read all source json file
    with open('./bfdata/' + files) as f:
      raw_data = json.load(f)

    # Iterating each post
    for iter in raw_data['posts']:
      if 'description' not in iter:
        iter['description'] = ' '

      # Python with ES bulk API
      act = {

        "_index" : "bfintaiwan",
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

# Indexing thru bulk API
es = Elasticsearch()
helpers.bulk(es, acts)
