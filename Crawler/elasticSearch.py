# import time
# from pymongo import MongoClient
# from elasticsearch import Elasticsearch

# mongodb_client = MongoClient('mongodb://localhost:27017')
# es_client = Elasticsearch(['http://localhost:9200/'])

# mdb = mongodb_client['darkweb']

# drop_index = es_client.indices.create(index='_id', ignore=400)
# create_index = es_client.indices.delete(index='_id', ignore=[400, 404])

# data = mdb.mycollection.find()

# for x in data:
#     _date = x['Name']
#     _type = x['Page Text']
#     print(_date,_type)

#     doc = {
#         'name': _date,
#         'page Text': _type
#     }

#     res = es_client.index(index="_id", doc_type="docs", body=doc)
#     time.sleep(0.2)

# print("Done")



from pymongo import MongoClient
from elasticsearch import Elasticsearch
import os

# Mongo Config
client = MongoClient('mongodb://localhost:27017')
db = client['darkweb']
collection = db['DW_data']

# Elasticsearch Config
es_host = 'http://localhost:9200/'
es = Elasticsearch([es_host])
es_index = '_id'

from elasticsearch import helpers
import json

def migrate():
  res = collection.find()
  # number of docs to migrate
  num_docs = 2000
  actions = []
  for i in range(num_docs):
      doc = res[i]
      mongo_id = doc['_id']
      print(mongo_id)
      doc.pop('_id', None)
      actions.append({
          "_index": es_index,
          "_id": mongo_id,
          "_source": json.dumps(doc)
      })
  helpers.bulk(es, actions)

doc=''
import datetime
json.dumps(doc)
def defaultconverter(o):
  if isinstance(o, datetime):
    return o.__str__()