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
def single_round_experiment(config):
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
    else:
        solution, trace = algorithm(graph, config['seed'], config['cutoff_time'])
    write_output(config, solution, trace)

# run the experiments for all the algorithms and all the graphs
def run_experiments():
    """
    Run the experiments for all the algorithms and all the graphs

    """
    seed = 1
    cutoff_time = 600
    graph_list = get_graph_files()
    for algorithm in ALGORITHM_LIST.values():
        if algorithm == None:
            continue
        for graph in graph_list:
            config = {'graph': graph, 'algorithm': algorithm, 'seed': seed, 'cutoff_time': cutoff_time}
            single_round_experiment(config)

# parse the command line arguments
def parse_args():
    # TODO
    pass

# Only for debugging purpose
if __name__ == '__main__':
    # load the graph
    print(os.getcwd())
    # run_experiments()
    verify_solutions()
