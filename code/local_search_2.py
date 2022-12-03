import numpy as np
import time
import heapq
#from io_utils import load_graph

def local_search_2(graph, initialize_ratio, seed, cutoff_time):

    def check_cover(covered_nodes, graph):
        for edge in graph.get_edges_set():
            if covered_nodes[edge[0]-1] + covered_nodes[edge[1]-1] == 0: # Neither of the two ends is covered
                return False
        return True

    def convert_to_set(array):
        result = set()
        for i,l in enumerate(array):
            if l: result.add(i+1)
        return result

    np.random.seed(seed)
    nodes = graph.get_vertices_set()
    nodes_num = graph.get_num_nodes()
    operation_graph = graph.copy() # operations of the graph are done on a copy of the graph

    covered_nodes = np.zeros(nodes_num, dtype=int)
    covered_nodes[:int(initialize_ratio*nodes_num)] = 1
    np.random.shuffle(covered_nodes) # initialization
    
    heap = [(len(operation_graph.get_neighbors_as_list(node)), node) for node in nodes] # create heap
    heapq._heapify_max(heap)

    trace = []
    start_time = time.time()

    while((time.time() - start_time) < cutoff_time):
        # every iteration, add the node with highest degree
        if len(heap)==0:
            print("Heap empty")
            return convert_to_set(covered_nodes), trace
        max_node = heapq._heappop_max(heap)[1]
        if covered_nodes[max_node-1] == 1:
            continue
        covered_nodes[max_node-1] = 1

        if check_cover(covered_nodes, graph):
            print("Finished Searching")
            return convert_to_set(covered_nodes), trace
        trace.append((time.time()-start_time, np.sum(covered_nodes)))
        #print(np.sum(covered_nodes))


    return convert_to_set(covered_nodes), trace

#G = load_graph('star.graph')
#print(local_search_2(G,0.1,1,1000))