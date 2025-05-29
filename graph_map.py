import json
import networkx as nx
import matplotlib.pyplot as plt
import os
import pandas as pd


FETCH_FOLDER = os.getcwd() + "/Mappings/"
CSV_DATA = os.getcwd() + "/CsvFiles/"


def load_mapper(address):
    """
    Loads the address mapper from a JSON file.

    Args:
        filename (str): The name of the file to load.

    Returns:
        dict: The loaded address mapper.
    """
    filename = address+".json"
    with open(FETCH_FOLDER+filename, "r") as file:
        address_mapper = json.load(file)
        return address_mapper

def shorten_address(address):
    """
    Shortens the address to a more manageable format.

    Args:
        address (str): The address to shorten.

    Returns:
        str: The shortened address.
    """
    if len(address) > 10:
        return address[:5] + "..." + address[-5:]
    else:
        return address

def convert_to_csv(type,data):
    if type not in ["NODES", "EDGES"]:
        raise ValueError("Type must be either 'NODES' or 'EDGES'")


    match type:
        case "NODES":
            print ("Converting Nodes to CSV")
            dict = {"address": data}
            df = pd.DataFrame(dict)
            df.to_csv(CSV_DATA+'AddressNodes.csv', index=False)
        case "EDGES":
            df2 = pd.DataFrame(data, columns=["from", "to", "weight"])  
            df2.to_csv(CSV_DATA+'AddressEdges.csv', index=False)

            print ("Converting Edges to CSV")   





def create_graph(address_mapper):
    """
    Creates a directed graph from the address mapper.

    Args:
        address_mapper (dict): The address mapper to convert to a graph.

    Returns:
        networkx.Graph: The directed graph representation of the address mapper.
    """
    G = nx.DiGraph()
    #node_list = [shorten_address(address) for address in address_mapper.keys()]
    node_list =  address_mapper.keys()
    edge_list = []
    G.add_nodes_from(node_list)
    for tokenSend, tokenReceive in address_mapper.items():
        for tokenReceive, data in tokenReceive.items():
            if round(data["sent"],1) > 0:
                G.add_edge(tokenSend, tokenReceive, weight=round(data["sent"],1))
                edge_list.append((tokenSend, tokenReceive, round(data["sent"],1)))  
    return G,edge_list

if __name__ == "__main__":
    # Load the address mapper from a file
    address = "P2K6Ymuv5tCuz9DJD2GtcRXKDo5sAeKdinYDC71gWzXZe5t"
    address_mapper = load_mapper(address)


    G,edge_list = create_graph(address_mapper)
    
    convert_to_csv("NODES",G.nodes)
    convert_to_csv("EDGES",edge_list)
    #pos = nx.circular_layout(G)
    #nx.draw(G, pos, with_labels=True, node_size=50,font_size=10, node_color="red")
    #edge_labels = nx.get_edge_attributes(G, "weight")
    #nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10, font_color="black",alpha=0.5)
    #plt.title("Address Mapper Graph")
    #plt.show()
