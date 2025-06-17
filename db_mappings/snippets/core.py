import os
import json
from datetime import datetime

CONFIG_PATH = os.getcwd() + "/config.json"


def retrieve_last_line(file_path):
    """
    Retrieves the last line from a file.

    Args:
        file_path (str): The path to the file.

    Returns:
        str: The last line of the file.
    """
    with open(file_path, 'rb') as f:
        try:
            f.seek(-2, os.SEEK_END)
            while f.read(1) != b'\n':
                f.seek(-2, os.SEEK_CUR)
        except OSError:
            f.seek(0)
        return f.readline().decode().strip()


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

def create_weekly_folder(folder_path):
    """
    Creates a weekly folder based on the current date.
    """
    current_date = datetime.now()
    week_number = current_date.isocalendar()[1]
    year = current_date.year
    folder_name = f"week_{week_number}_{year}"
    path = os.path.join(folder_path, folder_name)
    check_and_create_directory(path)