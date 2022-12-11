# import pymongo
from pymongo import MongoClient


client = MongoClient("mongodb+srv://admin:li8TXxeO8n416O8t@cluster0.h0ymi0w.mongodb.net/?retryWrites=true&w=majority")
db = client['sensor']
collection1 = db['sensorData']



def delete_n(collection, n):
    ndoc = collection.find({}, ('_id',), limit=n)
    selector = {'_id': {'$in': [doc['_id'] for doc in ndoc]}}
    return collection.delete_many(selector)

result = delete_n(collection1, 400)
print(result.deleted_count)