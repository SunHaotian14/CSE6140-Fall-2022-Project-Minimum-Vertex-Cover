"""
This file contains the implementation of a constructive heuristic for MVC with approximation guarantees.
We choose to implement the Greedy Independent Cover (GIC) algorithm.
The implemntation is based on the following paper:
[1]Franc ̧ois Delbot and Christian Laforest. Analytical and experimental comparison of six algorithms 
   for the vertex cover problem. Journal of Experimental Algorithmics (JEA), 15:1–4, 2010.
"""

import numpy as np
import time

def heuristic(graph, cutoff_time=600):
    """
    A constructive heuristic for MVC with approximation guarantees.
    We choose to implement the Greedy Independent Cover (GIC) algorithm.

    Parameters
    ----------
    graph : Graph
        The graph object of the predefined Graph class

    Returns
    -------
    solution : list
        The solution of the MVC problem
    trace : list
        The trace of the heuristic

    """
    start_time = time.time()
    solution = set()
    graph_temp = graph.copy()
    while not graph_temp.is_empty() and time.time() - start_time < cutoff_time:
        # select the vertex with the minimum degree
        selected_node = graph_temp.get_node_with_min_degree()
        # get neighbors of the selected vertex
        neighbors = set(graph_temp.get_neighbors_as_list(selected_node))
        # add the selected vertex to the solution
        solution = solution.union(neighbors)
        # remove the selected vertex and its neighbors from the graph
        neighbors.add(selected_node)
        graph_temp.delete_nodes_from_set(neighbors)
        # add the solution to the trace
    trace= [[time.time() - start_time, len(solution)]]
    solution = list(solution)
    
    return solution, trace