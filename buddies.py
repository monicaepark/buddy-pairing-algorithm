# USAGE ---------------------------------------------------------
# python3 buddies.py [csv_file] -m -v -h

# DEPENDENCIES --------------------------------------------------
# networkx matplotlib csv numpy
# if you don't have these packages, make sure to install them with
# pip install networkx matplotlib csv numpy argparse os

# IMPORTS --------------------------------------------------------
import networkx as nx
import matplotlib.pyplot as plt
import csv
import numpy as np
from typing import Tuple, List
import argparse
import os

# UTILITIES -------------------------------------------------------
def read_csv_to_matrix(filename: str) -> Tuple[list[str], np.ndarray]:
    names: set = set()
    edges: list[str] = []

    with open(filename, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) != 3:
                continue
            name1, name2, weight = row
            names.add(name1)
            names.add(name2)
            edges.append((name1, name2, weight))
    if len(names) %2 != 0: # add dummy node if odd number of members
        print("\n\tWARNING: Odd number of members.\n\tTrios may include re-encounter(s).\n\tDisregard the NULL member, which is used to make trios.\n")
        names.add("NULL")
        for name in names:
            edges.append((name, "NULL", 100.0))
    names = sorted(names)
    name_index = {name: i for i, name in enumerate(names)}

    # 3. Create n x n matrix (n = len(names)) filled with weights from csv
    matrix = np.zeros((len(names), len(names)))
    for name1, name2, weight in edges:
        i, j = name_index[name1], name_index[name2]
        matrix[i][j] = weight
        matrix[j][i] = weight
    
    return names, matrix

def create_graph_from_matrix(names: list[str], matrix: np.ndarray) -> nx.Graph:
    G = nx.Graph()
    G.add_nodes_from(names)
    for i in range(len(names)):
        for j in range(i+1, len(names)): # upper triangle, since matrix is symmetric
            weight = matrix[i][j]
            G.add_edge(names[i], names[j], weight=weight)
    return G

def visualize(G: nx.Graph) -> None:
    # Note: spring layout positions nodes such that edges are similar length to each other, with as few crossing edges as possible.
    pos = nx.spring_layout(G)
    
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=2000, font_size=15, font_weight='bold', edge_color='gray')
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red', font_size=12)
    
    plt.title("My Buddies Graph")
    plt.savefig("buddies.png")
    plt.show()
    print("The graph was successfully saved as 'buddies.png' in the current working directory.")

def pairing_algorithm(G: nx.Graph) -> Tuple[list[list[str]], nx.Graph()]:
    """
    Create all possible pairings for the graph, ensuring each person is paired
    with every other person exactly once across all sets.

    Args:
        G (nx.Graph): The original graph representing all relationships.

    Returns:
        list[list[str]]: A list of all pairing sets.
        nx.Graph: updated graph object with edges between previously paired nodes removed
    """
    temp: nx.Graph() = G.copy() # remaining nodes in the graph; will update in scope of function
    pairs: list[str] = []
    
    if temp.number_of_nodes() %2 != 0:
        print(f"Error: Odd number of nodes in pairing algorithm. Please submit a pull request.")
        return

    while temp.number_of_nodes() > 0:
        matching = nx.min_weight_matching(temp)
        for pair in matching:
            pairs.append(pair)
            temp.remove_nodes_from(pair)
            G.remove_edge(*pair)

    return pairs, G
 
def format_pairs(pairs: List[Tuple[str, str]]) -> str:
    makeTrio = False

    # check if null node exists
    for pair in pairs:
        if "NULL" in pair:
            null_pair = pair
            makeTrio = True
    
    if makeTrio:
        # remove pairing with null
        null = pairs.pop(pairs.index(null_pair))
        if null[0] == "NULL":
            lone = null[1]
        else:
            lone = null[0]
        # create a trio with the last pair
        last = pairs.pop()
        trio = (*last, lone)
        pairs.append(trio)

    formatted_pairs = ", ".join(f"({', '.join(pair)})" for pair in pairs)
    return formatted_pairs

# MAIN ------------------------------------------------------------
def main() -> None:

    # 1. Set up and parse arguments
    parser = argparse.ArgumentParser(description="create a set of pairings from a list of members with known closeness ratings, displaying the closeness matrix and relationship graph if desired")
    parser.add_argument("csv_file", type=str, help="relative file path to the CSV file containing the members' closeness ratings")
    parser.add_argument("-m", "--show-matrix", action="store_true", help="show the adjacency matrix of the graph")
    parser.add_argument("-v", "--visualize-graph", action="store_true", help="visualize the graph and save the file ('buddies.png')")
    args = parser.parse_args()

    # 2. Load CSV to matrix. Show matrix if -m flag.
    print("\n( ˶ˆᗜˆ˵ ) WELCOME TO THE BUDDY PAIRING PROGRAM ( ˶ˆᗜˆ˵ )")    
    print("\nLOADING CSV...")
    if not os.path.isfile(args.csv_file):
        print(f"Error: The file '{args.csv_file}' does not exist.")
        return
    names, matrix = read_csv_to_matrix(args.csv_file)
    print("Members:", ", ".join(names))
    if args.show_matrix:
        print("Closeness Matrix:\n", matrix)

    # Create graph from matrix. Visualize if -v flag.
    print("\nLOADING GRAPH...")
    myGraph = create_graph_from_matrix(names, matrix)
    if args.visualize_graph:
        print("Close the graph when ready to continue.")
        visualize(myGraph)
    
    # 3. Run pairing algorithm and return buddies.    
    print("\nCREATING PAIRS...")
    for i in range(len(names) - 1):
        myPairs, myGraph = pairing_algorithm(myGraph)
        if myPairs:
            formatted_pairs = format_pairs(myPairs)
            print(f'Set {i+1}: {formatted_pairs}')
    print("\n")
# Run main
if __name__ == '__main__':
    main()



