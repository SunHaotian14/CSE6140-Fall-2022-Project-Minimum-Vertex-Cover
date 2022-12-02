"""
This file contains functions to conduct the experiments, which can:
- parse the command line arguments and executes the corresponding experiments (one-time test);
- automatically run the experiments for all the algorithms and all the graphs (concrete results for project report).
"""

import argparse
import os
from heuristics import heuristic
from BnB import branch_and_bound
from local_search_1 import local_search_1
from local_search_2 import local_search_2
from io_utils import load_graph, write_output, get_graph_files
from evaluation_tools import verify_solutions


ALGORITHM_LIST = {'heuristic': heuristic, 'BnB': branch_and_bound, 'LS1': local_search_1, 'LS2': local_search_2}


# run single experiment with the given configuration
def single_round_experiment(config, T0_P = None):
    """
    Run single experiment with the given configuration and write the results to the output files (solution and trace)

    Parameters
    ----------
    config : dict
        The configuration of the experiment
    """
    print('=========================================')
    print('Graph: {}, Algorithm: {}, Seed: {}, Cutoff: {}'\
        .format(config['graph'], config['algorithm'], config['seed'], config['cutoff_time']))
    graph = load_graph(config['graph'])
    algorithm = ALGORITHM_LIST[config['algorithm']]
    if algorithm in {ALGORITHM_LIST['heuristic'], ALGORITHM_LIST['BnB']}:
        solution, trace = algorithm(graph, config['cutoff_time'])
    if algorithm == ALGORITHM_LIST['LS1']:
        solution, trace = algorithm(graph, config['seed'], config['cutoff_time'], T0_P)
    if algorithm == ALGORITHM_LIST['LS2']:
        solution, trace = algorithm(graph, config['seed'], config['cutoff_time'])
    if T0_P:
        write_output(config, solution, trace, OUTPUT_PATH='./output/Exp_T0_P/', T0_P=T0_P)
    else:
        write_output(config, solution, trace)

# run the experiments for all the algorithms and all the graphs
def run_experiments():
    """
    Run the experiments for all the algorithms and all the graphs

    """
    # EXP1: 
    #   Algorithm: heuristic, BnB, LS1, LS2
    #   Graph: all graphs
    #   Seed: 1
    #   Cutoff: 600
    seed = 1
    cutoff_time = 600
    graph_list = get_graph_files()
    for algorithm in ALGORITHM_LIST.keys():
        if algorithm == None:
            continue
        for graph in graph_list:
            config = {'graph': graph, 'algorithm': algorithm, 'seed': seed, 'cutoff_time': cutoff_time}
            single_round_experiment(config)

    # EXP2: 
    #   Algorithm: LS1
    #   Graph: power.graph, star2.graph
    #   Seed: 2, 3, 4, 5, 6, 7, 8, 9, 10
    #   Cutoff: 600
    graph_list = ['power.graph', 'star2.graph']
    seed_list = [2, 3, 4, 5, 6, 7, 8, 9, 10]
    for graph in graph_list:
        for seed in seed_list:
            config = {'graph': graph, 'algorithm': 'LS1', 'seed': seed, 'cutoff_time': cutoff_time}
            single_round_experiment(config)

    # EXP3:
    #   Algorithm: LS1
    #   Graph: all graphs
    #   Seed: 1, 2, 3
    #   Cutoff: 600
    #   T0_P: 50, 400
    graph_list = get_graph_files()
    seed_list = [1, 2, 3]
    T0_P_list = [50, 400]
    for graph in graph_list:
        for seed in seed_list:
            for T0_P in T0_P_list:
                config = {'graph': graph, 'algorithm': 'LS1', 'seed': seed, 'cutoff_time': cutoff_time}
                single_round_experiment(config, T0_P)

# parse the command line arguments
def parse_args():
    # TODO
    pass

# Only for debugging purpose
if __name__ == '__main__':
    # load the graph
    print(os.getcwd())
    run_experiments()
    verify_solutions()

