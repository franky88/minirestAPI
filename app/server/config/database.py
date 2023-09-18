from pymongo.mongo_client import MongoClient

uri = "mongodb://localhost:27017"

client = MongoClient(uri)

try:
    client.admin.command('ping')
    print("Sucessfully connected")
except Exception as e:
    print(e)

db = client.oarDB

user_col = db["user_collections"]

item_col = db["item_collections"]