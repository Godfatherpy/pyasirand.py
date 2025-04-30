from pymongo import MongoClient

def init_db(mongo_uri: str, db_name: str = None):
    client = MongoClient(mongo_uri)
    if db_name:
        return client[db_name]
    else:
        return client.get_default_database()
