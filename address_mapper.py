import os
import requests
import json

rpc_url = ["https://pharpc1.phantasma.info/api/v1","https://pharpc2.phantasma.info/api/v1","https://pharpc3.phantasma.info/api/v1"]
api_url = "https://api-explorer.phantasma.info/api/v1/"

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

"""
    Fucntion to get transaction details from a given transaction hash
    """
def get_transaction_details():
    path = os.getcwd()+"/AddressTransactions/filteredTransactions.json"
    with open(path, "r") as file:
        data = json.load(file)
        address_mappper = {}
        for hash in data:
            try:
                response = requests.get(f"{api_url}/transaction?order_by=id&order_direction=asc&hash={hash}&with_events=1&with_event_data=1")
                if response.status_code == 200:
                    data = response.json()
                    for transaction in data["transactions"]:
                        for event in transaction["events"]:
                            
                    
                    
                else:
                    print(f"Error: {response.status_code}")
            except requests.exceptions.RequestException as e:
                print(f"Request failed: {e}")
            return None
"""
    Imports the transaction data from a given file and puts it into a list
    --Future--:
    - Will not be needed as transaction data will be checked per block and not per file
     This is a quick and dirt solution , will be improved in the future.
    """
def filter_transaction_data():
    path = os.getcwd()+"/AddressTransactions/"
    transaction_data = []
    with os.scandir(path) as entries:
        for entry in entries:
            if entry.is_file() and entry.name.endswith('.json'):
                try:
                    with open(entry.path, 'r') as file:
                        data = json.load(file)
                        # Check if the data is a dictionary
                        if not isinstance(data,dict):
                            continue
                        for transaction in data["hash"]:
                            if transaction not in transaction_data:
                                transaction_data.append(transaction)
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON from file {entry.name}: {e}")
                except FileNotFoundError as e:
                    print(f"File not found: {e}")
                except Exception as e:
                    print(f"An error occurred while processing file {entry.name}: {e}")

    with open(path + "filteredTransactions.json", 'w') as outfile:
        json.dump(transaction_data, outfile, indent=4)




if __name__ == "__main__":
 filter_transaction_data()
