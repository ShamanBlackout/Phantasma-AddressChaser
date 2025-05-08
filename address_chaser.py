import requests 
from pprint import pprint
import json
import math


rpc_url = ["https://pharpc1.phantasma.info/api/v1","https://pharpc2.phantasma.info/api/v1","https://pharpc3.phantasma.info/api/v1"]
url = "https://api-explorer.phantasma.info/api/v1/"



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
                transactions.extend(data['result'][tx])
            else:
                print(f"Error: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
        return transactions 

def get_transaction_details(**kwargs):
    try:
        response = requests.get(f"{url[0]}/GetTransactionDetails?txid={txid}")
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"Error: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
    return
 


#result = get_tranasaction_count("P2KKQBFNmxyD3vWMFFiV15m8w2bLgDBi4JQKm4b7wT8gxi7", "main")
#pprint(result)
transctionCount = get_tranasaction_count("P2KKQBFNmxyD3vWMFFiV15m8w2bLgDBi4JQKm4b7wT8gxi7", "main")
transactions = get_transactions("P2KKQBFNmxyD3vWMFFiV15m8w2bLgDBi4JQKm4b7wT8gxi7",transctionCount) if transctionCount else None

pprint(transactions)

if __name__ == "__main__":
    print("main")