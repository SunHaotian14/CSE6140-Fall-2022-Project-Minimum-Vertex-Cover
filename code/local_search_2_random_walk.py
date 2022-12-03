import numpy as np
import time
import random
#from io_utils import load_graph

def local_search_2(graph, seed, cutoff_time):

    def check_cover(covered_nodes, graph):
        for edge in graph.get_edges_set():
            if edge[0] not in covered_nodes and edge[1] not in covered_nodes: # Neither of the two ends is covered
                return False
        return True

    random.seed(seed)
    uncov = list(graph.get_vertices_set())
    cov = []
    
    trace = []
    start_time = time.time()

    while(True):
        trace.append((time.time()-start_time, len(cov)))
        #print(len(cov))
        selected_node = random.choice(uncov)
        cov.append(selected_node)
        uncov.remove(selected_node)
        if check_cover(cov, graph):
            return cov, trace

#G = load_graph('star.graph')
#print(local_search_2(G,1,1))