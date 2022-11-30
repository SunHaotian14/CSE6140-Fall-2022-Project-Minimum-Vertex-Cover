"""
This file defines the graph class based on networkx and some essential operations.
"""

import networkx as nx
import matplotlib.pyplot as plt
import matplotlib

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
    def get_neighbors_as_list(self, node):
        return list(self.g.neighbors(node))

    # get the total number of nodes in the graph
    def get_num_nodes(self):
        return self.g.number_of_nodes()
    
    # get the total number of edges in the graph
    def get_num_edges(self):
        return self.g.number_of_edges()
    
    # get the set of nodes in the graph (copied object)
    def get_vertices_set(self):
        return set(self.g.nodes()).copy()

    # get the set of edges in the graph (copied object)
    def get_edges_set(self):
        return set(self.g.edges()).copy()

    # determine whether the graph is empty
    def is_empty(self):
        return self.g.number_of_nodes() == 0
    
    # delete the input nodes from the graph
    def delete_nodes_from_set(self, node_set):
        self.g.remove_nodes_from(iter(node_set))

    # get the node with the minimum degree
    def get_node_with_min_degree(self):
        return min(self.g, key=self.g.degree)

    # get the deep copy of the graph
    def copy(self):
        return Graph(self.g.copy())
    
    # draw the graph (debugging purpose)
    def show(self):
        plt.figure()
        nx.draw(self.g, with_labels=True)
        plt.show()
        plt.show()