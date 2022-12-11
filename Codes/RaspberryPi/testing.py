client = MongoClient("mongodb+srv://admin:li8TXxeO8n416O8t@cluster0.h0ymi0w.mongodb.net/?retryWrites=true&w=majority")
db = client['sensor']
collection = db['sensorData']

db.things.find( { a : { $exists : false } } )