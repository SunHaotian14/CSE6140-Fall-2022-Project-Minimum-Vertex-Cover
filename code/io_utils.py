"""
This file contains some support functions for
- loading graphs from the '/Data/' folder in format of Graph class;
- writing the results to the '/output/' folder in format of .sol and .trace file;
- loading the results from the '/output/' folder;
"""

import os
import numpy as np
from graph import Graph

DATA_PATH = './DATA/'
OUTPUT_PATH = './output/'

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
    graph_path = DATA_PATH + graph_file
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
def write_output(config, solution, trace):
    """
    Write the results to the output file

    Parameters
    ----------

    output_file : str
        The file name of the output file
    solution : list recording the found solution, in the format of:
        - line 1: quality of best solution found (integer)
        - lines 2: list of vertex IDs of the vertex cover (comma-separated)
    trace : list recording the trace of the algorithm, in the format of:
        - A timestamp in seconds (double)
        - Quality of the best found solution at that point in time (integer).

    """
    output_file = OUTPUT_PATH + config['graph'] + '_' + config['algorithm'] + '_' \
                + str(config['cutoff_time']) + '_' + str(config['seed']) + '.sol'
    with open(output_file, 'w') as f:
        # write the solution
        f.write(str(len(solution)))
        f.write('\n')
        f.write(','.join(map(str, solution)))
    
    output_file = OUTPUT_PATH + config['graph'] + '_' + config['algorithm'] + '_' \
                + str(config['cutoff_time']) + '_' + str(config['seed']) + '.trace'
    with open(output_file, 'w') as f:
        # write the trace
        for t in trace:
            f.write(','.join(map(str, t)))
            f.write('\n')
        
# load trace and solution from the output file
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

# get all graph files in the DATA_PATH
def get_graph_files():
    """
    Get all graph files in the DATA_PATH

    Returns
    -------
    graph_files : list
        The list of graph files

    """
    graph_files = os.listdir(DATA_PATH)
    graph_files = list(filter(lambda x: x.endswith('.graph'), graph_files))
    return graph_files

# Only for debugging purpose
if __name__ == '__main__':
    # load the graph
    print(os.getcwd())
    print(len(get_graph_files()))

   