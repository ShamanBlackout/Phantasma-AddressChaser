from pymongo import MongoClient
import json
import snippets
from pathlib import Path
import os



CWD = Path(__file__).parent.absolute() # Ensure the current directory is set correctly

with open(os.path.join(CWD,"config.json"), "r") as file:
    config = json.load(file)

CONN = config["db_connection"]
RPC = config["rpc_url"]
API = config["api_url"]
LOG_DATA = []
LOG_PATH = config["logging"]["path"]

def create_database(name):
    """
    Create a MongoDB database and return the database object.
    """
    LOG_DATA.append(f"Creating database connection: {CONN}")
    try:
        client = MongoClient(CONN)
        if not client:
            raise Exception("Failed to connect to the database. Please check your connection string.")
        db = client[name]
        LOG_DATA.append(f"Database created: {db.name}")
        return db
    except Exception as e:
        LOG_DATA.append(f"Error creating database: {e}")
        return None
    
def create_collection(db, collection_name):
    """
    Create a collection in the database.
    
    Args:
        db: The database object.
        collection_name (str): The name of the collection to create.
    
    Returns:
        The created collection object or None if the creation failed.
    """
    if db is not None:
        try:
            collection = db[collection_name]
            LOG_DATA.append(f"Collection {collection_name} created in database {db.name}.")
            return collection
        except Exception as e:
            LOG_DATA.append(f"Error creating collection {collection_name}: {e}")
            return None
    else:
        LOG_DATA.append("Database connection is None. Cannot create collection.")
        return None


def get_database():
    """
    Connect to the MongoDB database and return the database object.
    """
    LOG_DATA.append(f"Connecting to database:  {CONN}")
    try:
        client = MongoClient(CONN)
        if not client:
            raise Exception("Failed to connect to the database. Please check your connection string.")
        if "local" in client.list_database_names():
            db = client["local"]
            return db
    except Exception as e:
        LOG_DATA.append(f"Error connecting to the database: {e}")
        return None
        

def get_collection(db, collection_name):
    """
    Get a collection from the database.
    """
    if db is not None and collection_name in db.list_collection_names():
        return db[collection_name]
    else:
        LOG_DATA.append(f"Collection {collection_name} does not exist in the database.")
        return None

if __name__ == "__main__":
 
    db = get_database()
    print(db)
    if db is not None:
        LOG_DATA.append(f"Connected to database: {db.name}")
    else:
        LOG_DATA.append("Failed to connect to the database.")
    
    # Example usage of get_collection
    collection_name = "startup_log"  # Replace with your collection name
    collection = get_collection(db, collection_name)
    if collection is not None:
        LOG_DATA.append(f"Collection {collection_name} is ready for use.")
    else:
        LOG_DATA.append(f"Collection {collection_name} does not exist in the database.")
    if config["logging"]["enabled"]:
        snippets.save_logs(os.path.join(CWD, LOG_PATH), LOG_DATA)
