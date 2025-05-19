import json
import networkx as nx
import matplotlib.pyplot as plt
import os
FOLDER = os.getcwd() + "/Mappings/"


def load_mapper(filename):
    """
    Loads the address mapper from a JSON file.

    Args:
        filename (str): The name of the file to load.

    Returns:
        dict: The loaded address mapper.
    """
    try:
        with open(FOLDER+filename, "r") as file:
            address_mapper = json.load(file)
            return address_mapper
    except FileNotFoundError:
        print(f"File '{filename}' not found. Returning empty address mapper.")
        exit(1)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from file '{filename}': {e}")
        exit(1)

def create_graph(address_mapper):
    """
    Creates a directed graph from the address mapper.

    Args:
        address_mapper (dict): The address mapper to convert to a graph.

    Returns:
        networkx.Graph: The directed graph representation of the address mapper.
    """
    G = nx.MultiDiGraph()
    for tokenSend, tokenReceive in address_mapper.items():
        for tokenReceive, data in tokenReceive.items():
            if tokenSend not in G:
                G.add_node(tokenSend)
            if tokenReceive not in G:
                G.add_node(tokenReceive)
            if data["sent"] >0:
                G.add_edge(tokenSend, tokenReceive, weight=data["sent"])
            if data["received"] >0:
                G.add_edge(tokenReceive, tokenSend, weight=data["received"])
    return G

if __name__ == "__main__":
    # Load the address mapper from a file
    address_mapper = load_mapper("address_mapper.json")

    # Create a graph from the address mapper
    G = create_graph(address_mapper)

    # Draw the graph
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_size=50,node_color="red", font_size=1, font_weight="bold")
    edge_labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=5, font_color="black",alpha=0.5)
    plt.title("Address Mapper Graph")
    plt.show()