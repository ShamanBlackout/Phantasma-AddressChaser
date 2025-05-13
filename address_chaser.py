import requests 
from pprint import pprint
import json
import math
import os


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


def get_tranasaction_count(address,chainInput):

    try:
        response = requests.get(f"{rpc_url[0]}/GetAddressTransactionCount?account={address}&chainInput={chainInput}")
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"Error: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
    return 

def get_transactions(address,transcactionCount):
    
    pageSize = 100 #default page size
    page = math.ceil(transcactionCount/pageSize) #amount of pages to be requested
    transactions = [] #list to store transactions
    for i in range(page):
        try:
            response = requests.get(f"{rpc_url[0]}/GetAddressTransactions?account={address}&page={page}&pageSize={pageSize}")
            if response.status_code == 200:
                data = response.json()
                transactions.extend(data['result']['txs'])
            else:
                print(f"Error: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
        return transactions 

def get_transaction_details(hash):

    """
    Fetches transaction details from the Phantasma API.
    Options are hard coded for now, but can be changed to be dynamic.
    --Future work--
    Allow user to input the options they want to use for the API call.
    """

    try:
        response = requests.get(f"{url[0]}/?order_by=id&order_direction=asc&hash={hash}&chain=main"\
                                "&with_nft=0&with_events=1&with_event_data=1&with_fiat=0&with_script=0&with_total=0")
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"Error: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
    return
 

def get_and_store_all_address_transaction():
    """
    Fetches all address transactions from the Phantasma API and stores them in a JSON file.
    """

    #Check if the directory exists, if not create it
    check_and_create_directory(os.getcwd()+"/AddressTransactions/")

    with open(os.getcwd()+"/AddressCollection/soulBalances.json", "r") as infile:
        data = json.load(infile)
    # Check if the file is empty
        if not data:
            print("The file is empty.")
            return  
        for x in data:
            count = get_tranasaction_count(x["address"],"main")
            if count:
                transactions = get_transactions(x["address"],count) if count else None
                if transactions:
                    #Only need to get the transaction hashes that
                    filtered_transactions = {
                        "address": x["address"],
                        "transactionCount": count,
                        "hash": [x["hash"] for x in transactions for i in x["events"] if i["kind"] == "TokenSend"],
                    }

                    with open(os.getcwd()+f"/AddressTransactions/{x['address']}.json", "w") as outfile:
                        json.dump(filtered_transactions, outfile, indent=4)
                    print(f"Transactions for {x['address']} updated in {x['address']}.json")
                else:
                    print(f"No transactions found for {x['address']}")
            else:
                print(f"Failed to get transaction count for {x['address']}")
            


def get_and_update_address(*addresses):
    """
    Fetches address data from the Phantasma API and updates the JSON file.
    """
    try:
        response = requests.get(f"{url}/addresses?ORDER_BY=id&ORDER_DIRECTION=asc&OFFSET=0&LIMIT=1000000&CHAIN=main"\
                                "&with_storage=0&with_stakes=1&with_balance=1&with_total=1")
        if response.status_code == 200:
            data = response.json()
            with open("address_transactions.json", "w") as outfile:
                json.dump(data, outfile, indent=4)
            print("Address transactions updated in address_transactions.json")
        else:
            print(f"Error: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    #transctionCount = get_tranasaction_count("P2KKQBFNmxyD3vWMFFiV15m8w2bLgDBi4JQKm4b7wT8gxi7", "main")
    #transactions = get_transactions("P2KKQBFNmxyD3vWMFFiV15m8w2bLgDBi4JQKm4b7wT8gxi7",transctionCount) if transctionCount else None
    #pprint(transactions)
    get_and_store_all_address_transaction()
