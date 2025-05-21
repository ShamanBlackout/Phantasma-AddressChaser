import os
import requests
import json
import time
import math
import snippets

# Constants
DIR = os.getcwd()
FOLDER = DIR+ "/Mappings/"
FETCH_PATH = DIR+ "/AddressTransactions/"
RPC_URL,API_URL = snippets.load_config()



def update_address_map(address_mappper,tokenSend,tokenReceive,amount,timestamp):
    """
    Updates the address mapper with the given token send address , token receive address, and amount.
    Must Map both ways, Token Send and Token Receive will both be keys

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
        address_mappper[tokenSend][tokenReceive]["sent"] += amount
        address_mappper[tokenSend][tokenReceive]["sentTimeStamp"].append(timestamp)
    # Update the reverse mapping for tokenReceive
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
        address_mappper[tokenReceive][tokenSend]["received"] += amount
        address_mappper[tokenReceive][tokenSend]["receivedTimeStamp"].append(timestamp) 
    return address_mappper

def save_progress(address, address_mapper):
    """
    Saves the progress of the address mapper to a file.

    Args:
        hash (str): The hash of the transaction.
        address_mapper (dict): The address mapper to save.
    """
    snippets.check_and_create_directory(FOLDER)
    with open(FOLDER +address+".json", 'w') as outfile:
        json.dump(address_mapper, outfile, indent=4)
 

def load_progress():
    """
    Loads the progress of the address mapper from a file.

    Returns:
        dict: The loaded address mapper.
        hash (str): The latest hash of the transaction.

    --Future Work--
        - This will have to get reworked to load data from the last block
    """
    try:
        with open(FOLDER + "address_mapper.json", 'r') as outfile:
            address_mapper = json.load(outfile)
        last_hash = retrieve_last_line(FOLDER + "save_point.txt")

        return address_mapper, last_hash
    except FileNotFoundError:
        print("No progress file found.")
        return {},0
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from progress file: {e}")
        return {},0



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


"""
    Fucntion to get transaction details from a given transaction hash
 """    
def map_transactions(address):
    """
        Gets transaction details from a given transaction hash and updates the address mapper.

        Args:
            address_mappper (dict): The address mapper to update.

        Returns:
            dict: The updated address mapper.
    """
    path = DIR +"/AddressTransactions/"+address+".json"
    with open(path, "r") as file:
        data = json.load(file)
    try:
        address_mappper = {}
        for hash in data[address]:
            response = requests.get(f"{API_URL}transaction?order_by=id&order_direction=asc&hash={hash}&with_events=1&with_event_data=1")
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
            transaction_data = response.json()
            # Check if the response contains the expected structure
            if response.status_code == 200:
                #There shpuld be only one transaction in the response
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
        # Save the address mapper to a file
        save_progress(address, address_mappper)
    except KeyError as e:
        print(f"Key Error: Key '{address}' not found:{e}")
        exit(1)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from file '{path}': {e}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed for hash {address}: {e}")


"""
    Imports the transaction data from a given file and puts it into a list
    --Future--:
    - Will not be needed as transaction data will be checked per block and not per file
     This is a quick and dirt solution , will be improved in the future.
    """
if __name__ == "__main__":
    address = "P2KKQBFNmxyD3vWMFFiV15m8w2bLgDBi4JQKm4b7wT8gxi7"
    map_transactions(address) 



