import requests
import json

limit = "1000000" #max values to be pulled
offset = "0" #
chain = "main"
order_by = "id" #id, address, address_name 
order_direction = "asc"
validator_kind =["Invalid","Primary","Secondary","Proposed","Invalid"]
with_storage = "1"  # 0 default    
with_stakes = "1" # 0 default
with_balance = "1" # 0 default
with_total = "1" # 0 or 1, 0 default 



url = "https://api-explorer.phantasma.info/api/v1/addresses?order_by="+order_by +\
"&order_direction="+order_direction+"&offset="+offset+"&limit="+limit+"&chain="+chain


def mastersCount(filename):
    
    """
    Counts the number of stake masters on chain.

    Args:
        filename (str): The name of the file to count lines in.

    Returns:
        int: The number of stake masters.
    """
    stake_masters = [];
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
            for item in data["addresses"]:
                if float(item['stake']) >= 50000:
                    stake_masters.append({
                        "address":item['address'],
                        "stake":item['stake']})
    except FileNotFoundError:
        print(f"File {filename} not found.")
    except json.JSONDecodeError:
        print(f"Error decoding JSON from file {filename}.")

    stake_masters_count = {
        "stake_masters_count": len(stake_masters),
        "stake_masters": stake_masters  
    }
    if stake_masters:
        with open("stakeMasters"".json", "w") as f:
            json.dump(stake_masters_count, f, indent=4)  # Save with indentation for readability)
        
        



  
    

    


def fetch_and_save_address_collection(url,validator):
    """
    Fetches JSON data from a URL and saves it to a file named 'addressCollection.json'.

    Args:
        url (str): The URL to fetch the JSON data from.
    """
    try:
        url = url + "&validator_kind=" + validator
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)

        data = response.json()

        with open("addressCollection_"+validator+".json", "w") as f:
            json.dump(data, f, indent=4)  # Save with indentation for readability

        print("Successfully fetched and saved data to addressCollection_"+validator+".json")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from URL: {e}")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")



if __name__ == "__main__":
    #for validator in validator_kind:
    #   fetch_and_save_address_collection(url,validator)
    mastersCount("addressCollection_Invalid.json")