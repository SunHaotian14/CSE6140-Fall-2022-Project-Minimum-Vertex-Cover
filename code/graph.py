"""
This file defines the graph class based on networkx and some essential operations.
"""

import networkx as nx
import matplotlib.pyplot as plt

# Create a wrapper class for networkx graph object and add some essential operations.
class Graph:
    """
    Wrapper class for networkx graph object

    Parameters
    ----------
    incoming_graph_data : nx_G (None by default)

    """
    # initialize the graph class
    def __init__(self, nx_G=None):
        self.g = nx.Graph() if nx_G is None else nx_G

    # define graph iterator
    def __iter__(self):
        return iter(list(self.g))

    # add a new node to the graph
    def add_node(self, node):
        self.g.add_node(node)

    # add a new edge to the graph
    def add_edge(self, from_node, to_node):
        self.g.add_edge(from_node, to_node)
    
    def add_edge_from(self, from_node, to_nodes):
        if not to_nodes:
            self.g.add_node(from_node)
        else:
            self.g.add_edges_from([(from_node, to_node) for to_node in to_nodes])

    # get the list of nodes connected with the input node
    def get_neighbors(self, node):
        return self.g.neighbors(node)

    # get the total number of nodes in the graph
    def get_num_nodes(self):
        return self.g.number_of_nodes()
    
    # get the total number of edges in the graph
    def get_num_edges(self):
        return self.g.number_of_edges()
    
    # draw the graph (debugging purpose)
    def show(self):
        plt.figure()
        nx.draw(self.g)
        plt.show()