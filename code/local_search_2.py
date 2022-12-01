import numpy as np
import time
import heapq
#from io_utils import load_graph

def local_search_2(graph, seed, cutoff_time):

    def check_cover(covered_nodes, graph):
        for edge in graph.get_edges_set():
            if covered_nodes[edge[0]-1] + covered_nodes[edge[1]-1] == 0: # Neither of the two ends is covered
                return False
        return True

    nodes = graph.get_vertices_set()
    operation_graph = graph.copy() # operations of the graph are done on a copy of the graph
    
    heap = [(len(operation_graph.get_neighbors_as_list(node)), node) for node in nodes] # create heap
    heapq.heapify(heap)

    trace = []
    start_time = time.time()
    nodes_left = graph.get_num_nodes()

    covered_nodes = np.full(graph.get_num_nodes(),1, dtype=int)

    while(True):
        trace.append((time.time()-start_time, np.sum(covered_nodes)))

        # every iteration, delete the smallest possible degree node 
        while(True):
            print(f"Nodes left: {nodes_left}")
            nodes_left -= 1

            if len(heap)==0:
                return operation_graph.get_vertices_set(), trace
            min_node = heapq.heappop(heap)[1]
            covered_nodes[min_node-1] = 0

            if check_cover(covered_nodes, graph):
                operation_graph.delete_nodes_from_set([min_node])
                break
            else: 
                covered_nodes[min_node-1] = 1 # set the node back to covered
                continue


#G = load_graph('star.graph')
#print(local_search_2(G,1,1))