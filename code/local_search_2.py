import numpy as np
import time
import heapq

def local_search_2(graph, seed, cutoff_time):

    def check_cover(graph_test, graph):
        nodes_covered = graph_test.get_vertices_set()
        for edge in graph.get_edges_set():
            if (edge[0] not in nodes_covered) and (edge[1] not in nodes_covered):
                return False
        return True

    nodes = graph.get_vertices_set()
    num_whole_edge = graph.get_num_edges()
    num_whole_node = graph.get_num_nodes()
    cov = set(list(nodes))
    uncov = set()
    

    heap = [(len(graph.get_neighbors_as_list(node)), node) for node in nodes] # create heap
    heap = heapq.heapify(heap)

    trace = []

    start_time = time.time()

    while (time.time() - start_time) < cutoff_time:
        trace.append((time.time()-start_time, graph.get_num_nodes()))

        # every iteration, delete the smallest possible degree node 
        while(True):
            if len(heap)==0:
                return graph.get_vertices_set(), trace
            graph_test = graph.copy()
            min_node = heapq.heappop(heap)
            graph_test.delete_nodes_from_set(min_node)
            if check_cover(graph_test):
                graph.delete_nodes_from_set(min_node)
                break
            else: 
                continue

    return cov, trace