import os
import requests
import json
import time

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


def update_address_map(address_mappper,tokenSend,tokenReceive,amount,timestamp):
    """
    Updates the address mapper with the given token send address , token receive address, and amount.
    Must Map both ways, Token Send and Token Receive will both be keys=

    Args:
        address_mappper (dict): The address mapper to update.
        tokenSend (str): The token send address.
        tokenReceive (str): The token receive address.
        amount (float): The amount to update.

    Returns:
        dict: The updated address mapper.
    """
    if tokenSend not in address_mappper:
        address_mappper[tokenSend] = {}
    if tokenReceive not in address_mappper[tokenSend]:
        address_mappper[tokenSend][tokenReceive] ={
            "sent": amount,
            "received": 0,
            "sentTimeStamp":[timestamp],
            "receivedTimeStamp":[]
        } 
    else:
        address_mappper[tokenSend][tokenReceive] += amount
        address_mappper[tokenSend][tokenReceive]["sentTimeStamp"].append(timestamp)
    if tokenReceive not in address_mappper:
        address_mappper[tokenReceive] = {}
    if tokenSend not in address_mappper[tokenReceive]:
        address_mappper[tokenReceive][tokenSend] = {
            "sent": 0,
            "received": amount,
            "sentTimeStamp":[],
            "receivedTimeStamp":[timestamp]
        }
    else:
        address_mappper[tokenReceive][tokenSend] += amount
        address_mappper[tokenReceive][tokenSend]["receivedTimeStamp"].append(timestamp) 
    return address_mappper


"""
    Fucntion to get transaction details from a given transaction hash
    """
def get_transaction_details():
    """
        Gets transaction details from a given transaction hash and updates the address mapper.

        Args:
            address_mappper (dict): The address mapper to update.

        Returns:
            dict: The updated address mapper.
    """
    path = os.getcwd() +"/AddressTransactions/filteredTransactions.json"
    try:
        with open(path, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"Error: File '{path}' not found.")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from file '{path}': {e}")

    address_mappper = {}
    for hash in data:
        try:
            response = requests.get(f"{api_url}/transaction?order_by=id&order_direction=asc&hash={hash}&with_events=1&with_event_data=1")
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
            transaction_data = response.json()

            for transaction in transaction_data["transactions"]:
                tokenSend, tokenReceive, amount,timestamp = None, None, 0 ,0 # Initialize amount to 0
                for event in transaction["events"]:
                    if event["contract"]["name"] == "SOUL":
                        if event["event_kind"] == "TokenSend":
                            tokenSend = event["address"]
                            timestamp = event["date"]
                            amount = float(event["token_event"]["value"])  # Extract amount from TokenSend event
                        if event["event_kind"] == "TokenReceive":
                            tokenReceive = event["address"]

                if tokenSend and tokenReceive:
                    address_mappper = update_address_map(address_mappper, tokenSend, tokenReceive, amount,timestamp)

            time.sleep(0.1)  # Add a delay to avoid rate limiting

        except requests.exceptions.RequestException as e:
            print(f"Request failed for hash {hash}: {e}")
        except (KeyError, TypeError) as e:
            print(f"Error processing transaction {hash}: {e}") #Catching errors related to missing keys
        except Exception as e:
            print(f"An unexpected error occurred while processing transaction {hash}: {e}")

        return address_mappper 
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
