import time
import random
import math


def local_search_1(graph, seed, cutoff_time):
    def cost_f(num_uncov, num_node):
        """ bigger cost -> worse candidate """
        return 10 * num_uncov + num_node

    def prob(gap, t):
        """ get the prob of updating """
        p = math.exp(-gap / T)
        return p

    random.seed(seed)

    alpha = 0.99  # temp decrease rate
    T0 = 1000  # initial temp
    T = T0
    threshold = 5
    fail = 0
    tolerance = max(int(graph.get_num_nodes() * 0.5), 1500)
    down = 0

    all_nodes, original_v = graph.get_vertices_set(), graph.get_vertices_set()
    num_whole_edge = graph.get_num_edges()
    num_whole_node = graph.get_num_nodes()

    cov = set(list(all_nodes))
    uncov = set()
    score = cost_f(0, num_whole_node)
    best_score = score
    start_time = time.time()
    trace = []
    trace.append([time.time() - start_time, score])
    # trace = [str(round(time.time() - start_time, 2)) + ' ' + str(best_score)]  # trace file content
    solution = cov.copy()

    while (time.time() - start_time) < cutoff_time:
        if down > tolerance:
            # break
            pass
        # pick a random node
        node = random.sample(original_v, 1)[0]
        former_cov = cov.copy()
        former_uncov = uncov.copy()
        # explore neighborhood
        neighbors = graph.get_neighbors_as_list(node)
        if node in cov:
            for nei in neighbors:
                if nei not in cov:
                    uncov.add((node, nei))
                    uncov.add((nei, node))
            cov.remove(node)
        else:
            for nei in neighbors:
                if nei not in cov:
                    uncov.remove((node, nei))
                    uncov.remove((nei, node))
            cov.add(node)
        # evaluate candidate
        former_score = score
        score = cost_f(len(uncov), len(cov))
        update = True
        if score > former_score:
            down += 1
            gap = score - former_score
            p = prob(gap, T)
            rand = random.uniform(0, 1)
            update = True if rand < p else False
        else:
            down = 0
        if not update:
            # back to last step
            cov, uncov, score = former_cov, former_uncov, former_score
        T *= alpha

        if not len(uncov):
            if score < best_score:
                best_score = score
                trace.append([time.time() - start_time, score])
                solution = cov.copy()
            else:
                fail += 1
            if threshold <= fail:
                fail = 0
                T = T0
    print("Answer:", len(solution))
    print("Time Cost:", (time.time() - start_time))
    return solution, trace




