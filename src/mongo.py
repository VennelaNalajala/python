from pymongo import MongoClient
import json
client = MongoClient('mongodb://localhost:27017/')
db = client['mongo']
collection = db['collection']
with open('project.json') as file:
    file_data = json.load(file)
    if isinstance(file_data, list):
      collection.insert_many(file_data)  
    else:
      collection.insert_one(file_data)

