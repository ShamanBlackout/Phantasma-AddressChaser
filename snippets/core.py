import os
import json

CONFIG_PATH = os.getcwd() + "/config.json"

def load_config():
    """
    Loads the configuration from the config.json file.
    """
    try:
        with open("config.json", "r") as config_file:
            config = json.load(config_file)
            return config["rpc_url"], config["api_url"] 
    except FileNotFoundError:
        print(f"Error: File '{CONFIG_PATH}' not found.")
        exit(1)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from file '{CONFIG_PATH}': {e}")
        exit(1)


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