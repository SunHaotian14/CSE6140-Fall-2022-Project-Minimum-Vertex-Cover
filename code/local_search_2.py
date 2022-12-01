import numpy as np
import time
import heapq
#from io_utils import load_graph

def local_search_2(graph, seed, cutoff_time):

    def check_cover(graph_test, graph):
        nodes_covered = graph_test.get_vertices_set()
        for edge in graph.get_edges_set():
            if (edge[0] not in nodes_covered) and (edge[1] not in nodes_covered):
                return False
        return True

    nodes = graph.get_vertices_set()
    operation_graph = graph.copy() # operations of the graph are done on a copy of the graph
    
    heap = [(len(operation_graph.get_neighbors_as_list(node)), node) for node in nodes] # create heap
    heapq.heapify(heap)

    trace = []
    start_time = time.time()

    while (time.time() - start_time) < cutoff_time:
        trace.append((time.time()-start_time, operation_graph.get_num_nodes()))

        # every iteration, delete the smallest possible degree node 
        while(True):
            if len(heap)==0:
                return operation_graph.get_vertices_set(), trace
            graph_test = operation_graph.copy()
            min_node = heapq.heappop(heap)
            graph_test.delete_nodes_from_set([min_node[1]]) # try to delete the node with min degree
            if check_cover(graph_test, graph):
                operation_graph.delete_nodes_from_set([min_node[1]])
                break
            else: 
                continue


#G = load_graph('dummy2')
#print(local_search_2(G,1,1000))