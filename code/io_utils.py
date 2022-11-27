"""
This file contains some support functions for
- loading graphs from the '/Data/' folder in format of Graph class;
- writing the results to the '/output/' folder in format of .sol and .trace file;
- loading the results from the '/output/' folder;
"""

import os
import numpy as np
from graph import Graph

# load the graph from the graph file
def load_graph(graph_file):
    """
    Load the graph from the graph file indicated by graph_file

    Parameters
    ----------
    graph_file : str
        The file name of the graph

    Returns
    -------
    g : Graph
        The loaded graph object of the predefined Graph class

    """
    if not graph_file.endswith('.graph'):
        graph_file = graph_file + '.graph'
    graph_path = './DATA/' + graph_file
    graph = Graph()
    with open(graph_path, 'rb') as file:
        temp = file.readline().split()
        num_nodes, num_edges = int(temp[0]), int(temp[1])
        for current_node in range(1, num_nodes + 1):
            nodes = list(map(lambda x: int(x), file.readline().split()))
            graph.add_edge_from(current_node, nodes)
    assert graph.get_num_nodes() == num_nodes, '# nodes ({}) does not match the file ({})'.format(graph.get_num_nodes(), num_nodes)
    assert graph.get_num_edges() == num_edges, '# edges ({}) does not match the file ({})'.format(graph.get_num_edges(), num_edges)
    return graph

# write the results to the output file
def write_output(graph, output_file, solution, trace):
    """
    Write the results to the output file

    Parameters
    ----------
    graph : Graph
        The graph object of the predefined Graph class
    output_file : str
        The file name of the output file
    solution : list
        TODO
    trace : list
        TODO

    """
    with open(output_file, 'w') as f:
        # write the solution
        # TODO: write the solution to the output file
        pass

def load_results(result_file):
    """
    Load the results from the output file

    Parameters
    ----------
    output_file : str
        The file name of the output file

    Returns
    -------
    solution : list
        TODO
    trace : list
        TODO

    """
    # TODO


# Only for debugging purpose
if __name__ == '__main__':
    # load the graph
    print(os.getcwd())
    graph = load_graph('hep-th')
    # graph.show()
   