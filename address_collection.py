import requests
import json

limit = "1000000" #max values to be pulled
offset = "0" #
chain = "main"
order_by = "id" #id, address, address_name 
order_direction = "asc"
validator_kind = "Invalid" #Primary, Secondary, Proposed, Invalid -default-
with_storage = ""  # 0 default    
with_stakes = "0" # 0 default
with_balance = "0" # 0 default
with_total = "0" # 0 default



url = "https://api-explorer.phantasma.info/api/v1/addresses?order_by="+order_by +\
"&order_direction="+order_direction+"&offset="+offset+"&limit="+limit+"&chain="+chain


def fetch_and_save_address_collection(url):
    """
    Fetches JSON data from a URL and saves it to a file named 'addressCollection.json'.

    Args:
        url (str): The URL to fetch the JSON data from.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)

        data = response.json()

        with open("addressCollection.json", "w") as f:
            json.dump(data, f, indent=4)  # Save with indentation for readability

        print("Successfully fetched and saved data to addressCollection.json")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from URL: {e}")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    fetch_and_save_address_collection(url)