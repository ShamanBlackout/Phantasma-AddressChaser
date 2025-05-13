import os
import requests
import json

rpc_url = ["https://pharpc1.phantasma.info/api/v1","https://pharpc2.phantasma.info/api/v1","https://pharpc3.phantasma.info/api/v1"]
url = "https://api-explorer.phantasma.info/api/v1/"

def check_and_create_directory(folder):
    """
    Checks if a directory exists and creates it if it doesn't.

    Args:
        directory_path (str): The path to the directory.
    """
    if not os.path.exists(folder):
        try:
            os.makedirs(folder)  # Use makedirs to create parent directories as needed
            print(f"Directory '{folder}' created successfully.")
        except OSError as e:
            print(f"Error creating directory '{folder}': {e}")
    else:
        print(f"Directory '{folder}' already exists.")