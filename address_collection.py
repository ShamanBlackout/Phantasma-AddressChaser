import requests
import json
import threading
import os
"""
Created by: Shaman Blackout
Created on 05-0405-2025
This script fetches address data from the Phantasma API and saves it to a JSON file.
It also provides functions to count the number of stake masters and organize soul balances.
"""
LIMIT = "1000000"  # max values to be pulled
OFFSET = "0"
CHAIN = "main"
ORDER_BY = ("id", "address", "address_name")
ORDER_DIRECTION = ("asc", "desc")
VALIDATOR_KIND = ["Invalid", "Primary", "Secondary", "Proposed"]
SHOW_ALL = ('0', '1') # used for with_storage, with_stakes, with_balance, with_total , 0 for false, 1 for true
FOLDER = os.getcwd() +"/AddressCollection/"  # folder to save the json files


url = "https://api-explorer.phantasma.info/api/v1/addresses?ORDER_BY="+ORDER_BY[0] +\
    "&ORDER_DIRECTION="+ORDER_DIRECTION[0]+"&OFFSET="+OFFSET+"&LIMIT="+LIMIT+"&CHAIN="+CHAIN +\
    "&with_storage="+SHOW_ALL[0]+"&with_stakes="+SHOW_ALL[1] + \
    "&with_balance="+SHOW_ALL[1]+"&with_total="+SHOW_ALL[1]

def check_and_create_directory():
    """
    Checks if a directory exists and creates it if it doesn't.

    Args:
        directory_path (str): The path to the directory.
    """
    if not os.path.exists(FOLDER):
        try:
            os.makedirs(FOLDER)  # Use makedirs to create parent directories as needed
            print(f"Directory '{FOLDER}' created successfully.")
        except OSError as e:
            print(f"Error creating directory '{FOLDER}': {e}")
    else:
        print(f"Directory '{FOLDER}' already exists.")
        

def mastersCount(data):
    """
    Counts the number of stake masters on CHAIN.

    Args:
        data (json): The nested JSON data containing address information.

    """
    stake_masters = []
    for item in data["addresses"]:
        if float(item['stake']) >= 50000:
            stake_masters.append({
                "address": item['address'],
                "stake": item['stake']})

    stake_masters_count = {
        "stake_masters_count": len(stake_masters),
        "stake_masters": stake_masters
    }
    if stake_masters:
        with open(FOLDER+"stakeMasters.json", "w") as f:
            # Save with indentation for readability)
            json.dump(stake_masters_count, f, indent=4)
    print("Successfully fetched and saved data to stakeMasters.json")


def SoulBalances(data):
    """
    Organizes the soul balances of addresses in a JSON file and saves them to a new file.

    Args:
        data (json): The nested JSON data containing address information.
    """
    soul_balances = []
    for item in data["addresses"]:
        amount = None
        for balance in item['balances']:
            if balance["token"]["symbol"] == "SOUL" and balance["chain"]["chain_name"] == "main":
                amount = float(balance["amount"]) + float(item["stake"])
        if amount:  # Check if amount is not None or empty. Either SOUL is staked or they have no SOUL balance.
            soul_balances.append({
                "address": item['address'],
                "balance": amount})
        else:
            soul_balances.append({
                "address": item['address'],
                "balance": float(item['stake'])})
    if soul_balances:
        with open(FOLDER+"soulBalances.json", "w") as f:
            # Save with indentation for readability)
            json.dump(sorted(soul_balances, key=lambda x: x["balance"])[
                      ::-1], f, indent=4)
    print("Successfully fetched and saved data to soulBalances.json")


def fetch_and_save_address_collection(url, validator):
    """
    Fetches JSON data from a URL and saves it to a file named 'addressCollection.json'.

    Args:
        url (str): The URL to fetch the JSON data from.
    """
    try:
        url = url + "&VALIDATOR_KIND=" + validator
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)

        data = response.json()
        if validator == "Invalid":
            t1 = threading.Thread(target=mastersCount, args=(data,))
            t2 = threading.Thread(target=SoulBalances, args=(data,))
            t1.start()
            t2.start() 

        with open(FOLDER+"addressCollection_"+validator+".json", "w") as f:
            # Save with indentation for readability
            json.dump(data, f, indent=4)

        print("Successfully fetched and saved data to addressCollection_"+validator+".json")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from URL: {e}")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def update_all():
    # Will be used to update all the address collections in the future.
    print("Updating all address collections...")


if __name__ == "__main__":
    check_and_create_directory()
    for validator in VALIDATOR_KIND:
        fetch_and_save_address_collection(url, validator)
