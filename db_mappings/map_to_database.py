from pymongo import MongoClient
import json
import datetime
import snippets
import os




with open(os.path.join(os.getcwd()+"config.json"), "r") as file:
    config = json.load(file)

CONN = config["db_connection"]
RPC = config["rpc_url"]
API = config["api_url"]
LOG_DATA = []
LOG_PATH = config["log"]["path"]




def get_database():
    """
    Connect to the MongoDB database and return the database object.
    """
    print(f"Connecting to database: {config["f"]} at {CONN}")
    try:
        client = MongoClient(CONN)
        if not client:
            raise Exception("Failed to connect to the database. Please check your connection string.")
        if config["db_name"] in client.list_database_names():
            db = client[config["db_name"]]
            return db
    except Exception as e:
        LOG_PATH.append(f"Error connecting to the database: {e}")
        

def get_collection(db, collection_name):
    """
    Get a collection from the database.
    """
    if db and collection_name in db.list_collection_names():
        return db[collection_name]
    else:
        LOG_PATH.append(f"Collection {collection_name} does not exist in the database.")
        return None

if __name__ == "__main__":

    db = get_database()
    if db:
        LOG_PATH.append(f"Connected to database: {db.name}")
    else:
        LOG_PATH.append("Failed to connect to the database.")
    
    # Example usage of get_collection
    collection_name = "example_collection"  # Replace with your collection name
    collection = get_collection(db, collection_name)
    if collection:
        LOG_PATH.append(f"Collection {collection_name} is ready for use.")
    else:
        LOG_PATH.append(f"Collection {collection_name} does not exist in the database.")
    if config["log"]["enabled"]:
        snippets.save_logs(os.path.join(os.getcwd(LOG_PATH), LOG_DATA))
