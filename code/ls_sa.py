import time
import random
import math


def cost_f(graph):
    """ return evaluation of current solution """
    return graph.get_num_edges() / graph.get_num_nodes()


def local_search_1(graph, cutoff_time=600):
    original = graph.copy()

    start_time = time.time()
    alpha = 0.99
    T0 = 200
    T = T0
    threshold = 5
    num_cov = graph.get_num_edges()  # record number of covered edge
    cover = graph.get_vertices_set()
    # initialization
    score = num_cov / graph.get_num_nodes()
    former_score = score
    best_score = score
    trace = [str(round(time.time() - start_time, 2)) + ' ' + str(best_score)]  # trace file content
    solution = graph.copy()
    fail = 0

    while (time.time() - start_time) < cutoff_time:
        # select a node randomly
        node = random.sample(original.get_vertices_set(), 1)
        # explore neighborhood
        former = graph.copy()
        f_num_cov = num_cov
        neighbors = original.get_vertices_set()
        curr_nodes = graph.get_vertices_set()
        if node in curr_nodes:
            for neighbor in neighbors:
                num_cov = num_cov - 1 if neighbor not in curr_nodes else num_cov
            graph.delete_nodes_from_set(set(node))
        else:
            for neighbor in neighbors:
                num_cov = num_cov + 1 if neighbor not in curr_nodes else num_cov
            graph.add_node(node)
            graph.add_edge_from(node, neighbors)
        # calculate score of changed graph
        score = cost_f(graph)
        update = True
        if score <= former_score:
            if random.uniform(0, 1) < math.exp((former_score - score) / T):
                update = False
        T *= alpha
        # if not update, return last position
        if not update:
            graph = former
            num_cov = f_num_cov
        else:
            former_score = score

        if num_cov == original.get_num_edges():
            if best_score > score:
                trace.append(str(round(time.time() - start_time, 2)) + ' ' + str(score))
                best_score = score
                solution = graph.get_vertices_set
            else:
                fail += 1
            if threshold <= fail:
                fail = 0
                T = T0

        return solution, trace
