from pymongo import MongoClient
from pprint import pprint

client = MongoClient("mongodb+srv://admin:li8TXxeO8n416O8t@cluster0.h0ymi0w.mongodb.net/?retryWrites=true&w=majority")
db = client.ctox
serverStatusResult = db.command("serverStatus")
pprint(serverStatusResult)