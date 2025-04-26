from pymongo import MongoClient

def init_db(mongo_uri: str):
    client = MongoClient(mongo_uri)
    return client
  
