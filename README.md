# Buddy Pairing
### A simple pairing algorithm to create an optimal set of pairs from a list of members with known closeness ratings.
The **buddy-pairing-algorithm** repository contains the main Python script for pairing (`buddies.py`), as well as two example files (`even.txt` and `odd.txt`) that users can use as an input to the program to see an example of how the program works. This pairing algorithm was motivated by a lunch buddies event that my club holds every month to help members to get to know one another. Each month, all the members are paired with another member (or pairs+one trio if there are an odd number of people) and encouraged to grab lunch together. In subsequent events, the same two people are not paired again. I wanted to optimize and automate this process through a pairing algorithm that takes "closeless ratings" (Please see  [Buddy Pairing Options](#Options) for more information) as input, creates a graph, then runs a pairing algorithm to return a set of pairings where the closeness ratings are minimized in each round of pairing.

[Prerequisites](#Prerequisites) | [Basic Usage](#Usage) | [Buddy Pairing Options](#Options) | [Future Direction](#Direction)

## Prerequisites<a name="Prerequisites"></a>
`buddies` requires the following python libraries to be installed:
* networkx
* matplotlib
* csv
* numpy
* typing
* argparse
* os

These prerequisites can be installed with the following `pip` command:
```
pip install networkx matplotlib csv numpy typing argparse os
```

## Basic Usage<a name="Usage"></a>
The basic usage of 'buddies' is as follows:
```
python buddies.py [CSV] [other options]
```

To run `buddies.py` on a small test example, run the following commands on an input csv with an 1) even and 2) odd number of members:
```
python buddies.py even.txt
python buddies.py odd.txt
```

Using no other option flags, this should produce the outputs below:

even:
```
( ˶ˆᗜˆ˵ ) WELCOME TO THE BUDDY PAIRING PROGRAM ( ˶ˆᗜˆ˵ )

LOADING CSV...
Members: Chandler, Joey, Monica, Phoebe, Rachel, Ross

LOADING GRAPH...

CREATING PAIRS...
Set 1: (Joey, Monica), (Phoebe, Ross), (Chandler, Rachel)
Set 2: (Phoebe, Chandler), (Monica, Ross), (Joey, Rachel)
Set 3: (Phoebe, Joey), (Monica, Rachel), (Chandler, Ross)
Set 4: (Monica, Phoebe), (Joey, Chandler), (Rachel, Ross)
Set 5: (Chandler, Monica), (Phoebe, Rachel), (Ross, Joey)
```

odd:
```
( ˶ˆᗜˆ˵ ) WELCOME TO THE BUDDY PAIRING PROGRAM ( ˶ˆᗜˆ˵ )

LOADING CSV...

	WARNING: Odd number of members.
	Trios may include re-encounter(s).
	Disregard the NULL member, which is used to make trios.

Members: Chandler, Joey, NULL, Phoebe, Rachel, Ross

LOADING GRAPH...

CREATING PAIRS...
Set 1: (Phoebe, Ross), (Chandler, Rachel, Joey)
Set 2: (Chandler, Ross), (Phoebe, Joey, Rachel)
Set 3: (Joey, Rachel), (Phoebe, Chandler, Ross)
Set 4: (Phoebe, Rachel), (Joey, Ross, Chandler)
Set 5: (Rachel, Ross), (Joey, Chandler, Phoebe)
```

## Buddy Pairing Options<a name="Options"></a>
'buddies.py' requires the following input file:
* `[CSV]`: relative file path to the CSV file containing the members' closeness ratings. More specifically, the file should have comma separated values name1,name2,weight in each row representing the relationship between the members name1 and name2 with a weight (either `int` or `float `). This weight should be between the floats 0.0 to 10.0 (inclusive). This csv should complete enough information to represent all relationships from one member to all the other members, resulting in a complete graph (for n vertices, there should be n(n-1)/2 edges, which is equivalent to n(n-1)/2 rows in the csv). As an example, the graph with 6 members should have 6(6-1)/2 = 15 edges, and the graph with 5 members should have 5(5-1)/2 = 10 edges.

Additional options include:
* `-m`, `--show_matrix`: Show the adjacency matrix of the graph in the terminal output.
* `-v`, `--visualize_graph`: Visualize the graph and save the file as 'buddies.png' to the current working directory.

## Future Direction<a name="Dierction"></a>
In the context of this algorithm, "optimal" refers to a pairing of members that results in the lowest total sum of edge weights between those paired members. This means that members who aren't very close with one another are much more likely to be paired. Currently, the buddies algorithm creates optimal pairs when an even number of nodes is presented by using the `networkx` graph object's inbuilt `minimum_weight_matching` method; however, the code to create trios is not yet optimized, and rather creates a dummy node with a high weight edge to all other nodes, then later corrects the pairing of a member paired to the null node by moving that member to an existing pair to form a group of three. In the future, with more knowledge of mathematics for computer science, I hope to optimze this code.
