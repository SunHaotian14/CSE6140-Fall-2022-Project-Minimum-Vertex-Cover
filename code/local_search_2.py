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

    def convert_to_set(array):
        result = set()
        for i,l in enumerate(array):
            if l: result.add(i+1)
        return result



    np.random.seed(seed)
    nodes = graph.get_vertices_set()
    nodes_num = graph.get_num_nodes()

    # set up different init ratio for network size
    initialize_ratio = 0
    if nodes_num < 200:
        initialize_ratio = 0.05
    elif nodes_num < 2000:
        initialize_ratio = 0.02
    else:
        initialize_ratio = 0.01

    max_init_iter = 1000
    i = 0
    # Try initialization for max iter times
    while(True):
        covered_nodes = np.zeros(nodes_num, dtype=int)+1
        covered_nodes[:int(initialize_ratio*nodes_num)] = 0
        np.random.shuffle(covered_nodes) # initialization, set some of the nodes to be 0

        if check_cover(covered_nodes, graph):
            break
        i += 1
        if i == max_init_iter:
            print("Initialization Error!")
            return None
    
    heap = [(len(graph.get_neighbors_as_list(node)), node) for node in nodes] # create heap, degree as key
    heapq.heapify(heap)

    trace = []
    start_time = time.time()

    while((time.time() - start_time) < cutoff_time):
        # every iteration, delete the node with lowest degree
        if len(heap)==0:
            #print("Heap empty")
            return convert_to_set(covered_nodes), trace
        min_node = heapq.heappop(heap)[1]
        if covered_nodes[min_node-1] == 0:
            continue
        covered_nodes[min_node-1] = 0

        if not check_cover(covered_nodes, graph):
            covered_nodes[min_node-1] = 1 #restore
        trace.append((time.time()-start_time, np.sum(covered_nodes)))
        #print(np.sum(covered_nodes))
    print("Timeout!")
    return convert_to_set(covered_nodes), trace

#G = load_graph('as-22july06.graph')
#print(local_search_2(G,1,1000))