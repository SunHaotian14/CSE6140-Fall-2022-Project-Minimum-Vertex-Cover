import time
import math
import sys


def branch_and_bound(graph, cut_off_time=600):
    """
    Branch and Bound Method.
    :param graph: Graph object
    :param cut_off_time: int (600 by default)
    """

    start_time = time.time()
    graph_temp = graph.copy()

    # Set up info for the graph:
    vertices = list(graph_temp.g.nodes)
    n_edges = graph_temp.g.number_of_edges()

    # Set up info for the task:
    upper_bound = graph_temp.g.number_of_nodes()
    best_cover = vertices
    trace = []

    # "renew" the recursion limit if the maximum recursion depth exceeds the recursion limit:
    while sys.getrecursionlimit() < upper_bound:
        sys.setrecursionlimit(upper_bound + 2)

    def _backtracking(cover, cover_n, subgraph, n_edge_subgraph):
        """
        Backtracking iteration.
        :param cover: set
        :param cover_n: int
        :param subgraph: Graph
        :param n_edge_subgraph: int
        :return:
        """
        # cut-off condition:
        if time.time() - start_time > cut_off_time:
            return
        # nonlocal best_cover, upper_bound
        nonlocal best_cover, trace, upper_bound
        if n_edge_subgraph == 0:
            if len(cover) < upper_bound:
                best_cover = cover.copy()
                upper_bound = len(best_cover)
                # upper_bound = n_vertices
                trace.append([time.time() - start_time, upper_bound])
            return

        # Find the vertex that has not been covered that has the most degree.
        next_vertex = None
        max_degree = None
        for vertex in subgraph.g.nodes:
            if vertex not in cover and subgraph.g.degree[vertex] > 0:
                if max_degree is None or max_degree < subgraph.g.degree[vertex]:
                    max_degree = subgraph.g.degree[vertex]
                    next_vertex = vertex
        if max_degree is None:
            # Then all the vertices are included in the cover.
            return
        lower_bound = math.ceil(n_edge_subgraph / max_degree)
        if cover_n + lower_bound >= upper_bound:
            # Then prune the subtree
            return

        # Case 1: include the new vertex into the cover
        cover.add(next_vertex)
        n_adj = len(subgraph.g.adj[next_vertex])  # The number of adjacent nodes for next_vertex
        adjacent_nodes = list(subgraph.g.adj[next_vertex].keys())
        subgraph.g.remove_node(next_vertex)
        _backtracking(cover, cover_n + 1, subgraph, n_edge_subgraph - n_adj)

        # Case 2: do not include the new vertex into the cover
        # Since we do not include the new vertex, all of its adjacent nodes have to be included,
        # so all the edges linked to the new vertex can be covered.
        cover_temp = cover.copy()
        cover_temp.remove(next_vertex)
        for adj_v in adjacent_nodes:
            # adj_v is int
            cover_temp.add(adj_v)
        _backtracking(cover_temp, len(cover_temp), subgraph, n_edge_subgraph - n_adj)

        # Finally restore the subgraph
        subgraph.g.add_node(next_vertex)
        for adj_v in adjacent_nodes:
            subgraph.g.add_edge(next_vertex, adj_v)
        cover.remove(next_vertex)

    cover_init = set()
    _backtracking(cover_init, 0, graph, n_edges)
    return best_cover, trace

