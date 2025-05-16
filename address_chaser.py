import requests 
import time
import json
import math
import os
import snippets


RPC_URL,API_URL = snippets.load_config()


def get_tranasaction_count(address,chainInput):

    try:
        response = requests.get(f"{RPC_URL[0]}/GetAddressTransactionCount?account={address}&chainInput={chainInput}")
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            response.raise_for_status()
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
            response = requests.get(f"{RPC_URL[0]}/GetAddressTransactions?account={address}&page={page}&pageSize={pageSize}")
            response.raise_for_status()  # Raise an error for bad responses
            if response.status_code == 200:
                data = response.json()
                transactions.extend(data['result']['txs'])
            else:
                print(f"Error: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
        time.sleep(0.1)  # Add a delay to avoid rate limiting
    return transactions 

def get_transaction_details(hash):

    """
    Fetches transaction details from the Phantasma API.
    Options are hard coded for now, but can be changed to be dynamic.
    --Future work--
    Allow user to input the options they want to use for the API call.
    """

    try:
        response = requests.get(f"{API_URL}/?order_by=id&order_direction=asc&hash={hash}&chain=main"\
                                "&with_nft=0&with_events=1&with_event_data=1&with_fiat=0&with_script=0&with_total=0")
        response.raise_for_status()  # Raise an error for bad responses
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
    Only fetches the transactions that are of kind "TokenSend".
    """
    
    snippets.check_and_create_directory(os.getcwd()+"/AddressTransactions/")
    
    path = os.getcwd()+"/AddressCollection/soulBalances.json"
    try:
        with open(path, "r") as infile:
            data = json.load(infile)
            if not data:
                print(f"{path} is empty.")
            else:
                for x in data:
                    count = get_tranasaction_count(x["address"],"main")
                    transactions = get_transactions(x["address"],count) if count else None
                    if transactions:
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
    except FileNotFoundError:
        print(f"Error: File '{path}' not found.")
        exit(1)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from file '{path}': {e}")
        exit(1)
    except Exception as e:
            print(f"Error processing transactions: {e}")

   
                

#Not worked on yet, just some test code
def get_and_update_address(*addresses):
    """
    Fetches address data from the Phantasma API and updates the JSON file.
    """
    try:
        response = requests.get(f"{API_URL}/addresses?ORDER_BY=id&ORDER_DIRECTION=asc&OFFSET=0&LIMIT=1000000&CHAIN=main"\
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
    get_and_store_all_address_transaction()
