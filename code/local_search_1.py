import time
import random
import math


def local_search_1(graph, seed, cutoff_time):
    """
        local search 1：Simulated Annealing
    """
    def cost_f(num_uncov, num_node):
        """ bigger cost -> worse candidate """
        return 5 * num_uncov + num_node

    def prob(gap, t):
        """ get the prob of updating """
        p = math.exp(-gap / T)
        return p

    def empty_init(graph):
        all_nodes = graph.get_vertices_set()
        uncov = set()
        cov = set()
        for node in all_nodes:
            neighbors = graph.get_neighbors_as_list(node)
            for neighbor in neighbors:
                uncov.add((node, neighbor))
        return uncov, cov

    def full_init(graph):
        all_nodes = graph.get_vertices_set()
        cov = set(list(all_nodes))
        uncov = set()
        return uncov, cov

    def random_init(graph, p=0.3):
        all_nodes = graph.get_vertices_set()
        num = (1 - p) * len(all_nodes)
        tmp = set(random.sample(all_nodes, int(num)))  # 70% nodes as uncovered
        cov = all_nodes - tmp  # covered nodes
        uncov = set()
        for node in tmp:
            neighbors = graph.get_neighbors_as_list(node)
            for neighbor in neighbors:
                if neighbor not in cov:
                    uncov.add((node, neighbor))
        return uncov, cov

    random.seed(seed)

    alpha = 0.99  # temp decrease rate
    Tmin = 1e-3
    inner_round = 150

    all_nodes, original_v = graph.get_vertices_set(), graph.get_vertices_set()
    num_whole_edge = graph.get_num_edges()
    num_whole_node = graph.get_num_nodes()
    T0 = num_whole_edge * 200 + 1000
    T = T0

    uncov, cov = empty_init(graph)
    score = cost_f(len(uncov), len(cov))
    best_score = score
    start_time = time.time()
    trace = [[time.time() - start_time, score]]
    solution = cov.copy()

    while (time.time() - start_time) < cutoff_time and T >= Tmin:
        for _ in range(inner_round):
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
                gap = score - former_score
                p = prob(gap, T)
                rand = random.uniform(0, 1)
                update = True if rand < p else False
            if not update:
                # back to last step
                cov, uncov, score = former_cov, former_uncov, former_score

            if not len(uncov):
                if score < best_score:
                    best_score = score
                    trace.append([time.time() - start_time, score])
                    solution = cov.copy()
        T *= alpha

    print("Answer:", len(solution))
    print("Time Cost:", (time.time() - start_time))
    return solution, trace
