"""
Created by: Shaman Blackout
Created on 05-05-2025
This script fetches address data from the Phantasma API and saves it to a JSON file.
It also provides functions to count the number of stake masters and organize soul balances.
"""
import requests
import json
import time
import threading
import os
import snippets

OFFSET = "0"
CHAIN = "main"
ORDER_BY = ("id", "address", "address_name")
ORDER_DIRECTION = ("asc", "desc")
VALIDATOR_KIND = ["Invalid", "Primary", "Secondary", "Proposed"]
SHOW_ALL = ('0', '1') # used for with_storage, with_stakes, with_balance, with_total , 0 for false, 1 for true
FOLDER = os.getcwd() +"/AddressCollection/"  # folder to save the json files
RPC_URL,API_URL = snippets.load_config()




"""
    Function that get the address count of a given validator kind
Args: VALIDATOR
    kind (str): The validator kind to filter by.
Returns:   
    int: the count of addresses for the given validator kind

--future work--
This could definitely be improved by making it possible to craft the url
    Right now this is too static and needs to be more flexible.
"""
def get_address_count(validator_kind,limit):

    url = craft_url(ORDER_BY[0], ORDER_DIRECTION[0], OFFSET, limit, CHAIN, SHOW_ALL[0], SHOW_ALL[0], SHOW_ALL[0], SHOW_ALL[1], validator_kind)
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        data = response.json()
        return data["total_results"] if data["total_results"]!=0 else None
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def craft_url(order_by,order_direction,offset,limit,chain,with_storage,with_stakes,with_balance,with_total,validator_kind):
    """
    Function that crafts the url for the API call       
    Args:
        order_by (str): The order by clause.
        order_direction (str): The order direction clause.
        offset (str): The offset clause.
        limit (str): The limit clause.
        chain (str): The chain clause.
        with_storage (str): The with storage clause.
        with_stakes (str): The with stakes clause.
        with_balance (str): The with balance clause.
        with_total (str): The with total clause.

    Returns:
        str: The crafted URL.
    """
    return f"{API_URL}addresses?ORDER_BY={order_by}&ORDER_DIRECTION={order_direction}&OFFSET={offset}&LIMIT={limit}&\
    CHAIN={chain}&with_storage={with_storage}&\
    with_stakes={with_stakes}&with_balance={with_balance}&with_total={with_total}&validator_kind={validator_kind}"



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
    try:
        for item in data["addresses"]:
            amount = None
            for balance in item['balances']:
                if balance["token"]["symbol"] == "SOUL" and balance["chain"]["chain_name"] == "main":
                    amount = float(balance["amount"]) + float(item["stake"])
            if amount:  
                soul_balances.append({
                    "address": item['address'],
                    "balance": amount})
            else:
                print(f"SOUL balance not found for address: {item['address']}")
                soul_balances.append({
                    "address": item['address'],
                    "balance": float(item['stake'])})
        if soul_balances:
            with open(FOLDER+"soulBalances.json", "w") as f:
                # Save with indentation for readability)
                json.dump(sorted(soul_balances, key=lambda x: x["balance"])[
                        ::-1], f, indent=4)
    except KeyError as e:
        print(f"KeyError: {e} - Check if the JSON structure has changed.")
    
    print("Successfully fetched and saved data to soulBalances.json")


def fetch_and_save_address_collection(url, validator):
    """
    Fetches JSON data from a URL and saves it to a file named 'addressCollection.json'.

    Args:
        url (str): The URL to fetch the JSON data from.
    """
    try:
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
    snippets.check_and_create_directory(FOLDER)
    for validator in VALIDATOR_KIND:
        count = get_address_count(validator, 1)
        if count:
            url = craft_url(ORDER_BY[0], ORDER_DIRECTION[0], OFFSET, count, CHAIN, SHOW_ALL[1], SHOW_ALL[1], SHOW_ALL[1], SHOW_ALL[0], validator)
            fetch_and_save_address_collection(url, validator)
            time.sleep(0.1)  # Add a delay to avoid rate limiting
