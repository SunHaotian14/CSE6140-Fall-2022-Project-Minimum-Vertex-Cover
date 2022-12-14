"""
This file contains some support functions for evaluation, i.e.,
- formulating a comprehensive table to present the results from different algorithms;
- plotting the Qualified Runtime for various solution qualities (QRTDs);
- plotting the Solution Quality Distributions for various run-times (SQDs);
- box plotting for running time comparison.
"""
import numpy as np
import pandas as pd
from pandas import DataFrame as df
from matplotlib import pyplot as plt
from io_utils import load_graph, load_solution, load_trace, get_graph_files, get_solution_files

PLOTS_PATH = './plots/'
ALGORITHM_NAME_LIST = {'Approx', 'BnB', 'LS1', 'LS2'}
OPT_SOL = {'jazz': 158, 'karate': 14, 'football': 94, 'as-22july06': 3303, 'hep-th': 3926, 'star': 6902,\
            'star2': 4542, 'netscience': 899, 'email': 594, 'delaunay_n10': 703, 'power': 2203, 'dummy1': 2, 'dummy2': 3}
T0_P_LIST = [50, 200, 400]

# Function to verify the goodness of solution
def verify_solutions():
    """
    Verify the solutions generated by the algorithms

    """
    qualified = True
    solution_files = get_solution_files()
    for solution_file in solution_files:
        if 'delaunay_n10' in solution_file:
            graph_name0, graph_name1, algorithm, cutoff_time, seed = solution_file.split('_')
            graph_name = graph_name0 + '_' + graph_name1
        else:
            graph_name, algorithm, cutoff_time, seed = solution_file.split('_')
        graph = load_graph(graph_name)
        num_sol, solution = load_solution(solution_file)
        print('=========================================')
        print('Graph: {}, Algorithm: {}, Seed: {}, Cutoff: {}' 
            .format(graph_name, algorithm, seed, cutoff_time))
        if len(solution) != num_sol:
            print('The number of vertices ({}) in the solution does not match the number of solution ({})!'
                .format(num_sol, len(solution)))
            qualified = False
            continue
        if not set(solution).issubset(set(graph.get_vertices_set())): 
            print('The solution contains vertices that are not in the graph!')
            qualified = False
            continue
        for edge in graph.get_edges_set():
            if (edge[0] not in solution) and (edge[1] not in solution):
                print('Edge {} is not covered by the solution!'.format(edge))
                qualified = False
                break
        if qualified:
            print('The solution is qualified!')
    if qualified:
        print('All the solutions are qualified!')

def get_results_table():
    """
    Formulate a comprehensive table to present the results from different algorithms

    Returns
    -------
    table : pandas.DataFrame
        The comprehensive table of the results

    """
    df_list = {}
    for algorithm in ALGORITHM_NAME_LIST:
        results = []
        for graph in get_graph_files():
            dummy = np.zeros((10, 3))
            for seed in range(1, 11):
                file_name = graph + '_' + algorithm + '_' \
                    + str(600) + '_' + str(1)
                num_sol, _ = load_solution(file_name)
                trace = load_trace(file_name)
                if trace is None:
                    continue
                time = trace[-1][0]
                relative_error = (num_sol - OPT_SOL[graph]) / OPT_SOL[graph] * 100
                dummy[seed - 1, :] = [time, num_sol, relative_error]
            results.append(dummy.mean(axis = 0))
        df_results = pd.DataFrame(results,
                                    index=get_graph_files(),
                                    columns=['Time (s)',  'VC Value', 'RelErr (%)'])
        df_results = df_results.sort_values(by=['VC Value'])
        df_list[algorithm] = df_results
    return df_list

def get_Ps(graph, algorithm, RT_leq, SQ_leq):
    """
    Calculate the probability that the solution quality is less than or equal to SQ_leq
    and the runtime is less than or equal to RT_leq

    Parameters
    ----------
    graph : Graph
        The graph
    algorithm : str
        The algorithm name
    RT_leq : float
        The runtime threshold
    SQ_leq : int
        The solution quality threshold
    Returns
    -------
    P : float
        The probability that the solution quality is less than or equal to SQ_leq
        and the runtime is less than or equal to RT_leq

    """
    count = 0
    for seed in range(1, 11):
        file_name = graph + '_' + algorithm + '_' \
                + str(600) + '_' + str(seed)
        trace = load_trace(file_name)
        if trace is None:
            continue
        time_q = np.array([np.array([record[0], (record[1] - OPT_SOL[graph]) / OPT_SOL[graph] * 100]) for record in trace])
        # print(time_q)
        count += np.logical_and(time_q[:, 0] <= RT_leq, time_q[:, 1] <= SQ_leq).any()
    return count / 10


def QRTD_plot(graph, algorithm, q_stars = list(range(10)), time_steps = list(range(10))):
    """
    Plot the Qualified Runtime for various solution qualities (QRTDs)
    Parameters
    ----------
    graph : Graph
        The graph
    algorithm : str
        The algorithm name

    """
    plt.figure()
    for q_star in q_stars:
        Ps = [get_Ps(graph, algorithm, RT_leq, q_star) for RT_leq in time_steps]
        plt.plot(time_steps, Ps, label='q* = {}%'.format(q_star))
    plt.grid(color='0.95', linestyle='-')
    plt.xlabel('Runtime (s)')
    plt.ylabel('P(solve)')
    plt.title('QRTD for {} on {}'.format(algorithm, graph))
    plt.legend()
    plt.savefig(PLOTS_PATH + 'QRTD_{}_{}.png'.format(algorithm, graph))
    plt.show()

def SQD_plot(graph, algorithm, q_stars = list(range(10)), time_steps = list(range(10))):
    """
    Plot the Solution Quality Distributions for various run-times (SQDs)
    Parameters
    ----------
    graph : Graph
        The graph
    algorithm : str
        The algorithm name
    """
    # time_steps = list(range(start_time, end_time, ceil(end_time/num_time)))
    plt.figure()
    for RT_leq in time_steps:
        Ps = [get_Ps(graph, algorithm, RT_leq, q_star) for q_star in q_stars]
        plt.plot(q_stars, Ps, label='RT = {}s'.format(RT_leq))
    plt.grid(color='0.95', linestyle='-')
    plt.xlabel('Relative solution Quality (%)')
    plt.ylabel('P(solve)')
    plt.title('SQD for {} on {}'.format(algorithm, graph))
    plt.legend()
    plt.savefig(PLOTS_PATH + 'SQD_{}_{}.png'.format(algorithm, graph))
    plt.show()

def box_plot(graph, algorithm, q_star_range=[0, 1]):
    """
    Box plotting for running time comparison

    """
    results = []
    for seed in range(1, 11):
        file_name = graph + '_' + algorithm + '_' \
                + str(600) + '_' + str(seed)
        trace = load_trace(file_name)
        if trace is None:
            continue
        time_q = np.array([np.array([record[0], (record[1] - OPT_SOL[graph]) / OPT_SOL[graph] * 100]) for record in trace])
        results.append(time_q)
    final_qs = [single_result[-1][1] for single_result in results]
    print('The final solution qualities of each run are {}%'.format(sorted(final_qs)))
    selected_RTs = []
    for single_result in results:
        for record in single_result:
            if record[1] <= q_star_range[1] and record[1] >= q_star_range[0]:
                selected_RTs.append(record[0])
                break
    print('The selected runtimes are {}s'.format(sorted(selected_RTs)))
    plt.figure()
    bp_dict = plt.boxplot(selected_RTs, showmeans=True)
    for line in bp_dict['medians']:
        x, y = line.get_xydata()[0] 
        plt.text(x, y, 'median: {:.2f}'.format(y), horizontalalignment='right', verticalalignment='bottom')
    for line in bp_dict['boxes']:
        x, y = line.get_xydata()[0]
        plt.text(x, y, 'Q3: {:.2f}'.format(y), horizontalalignment='right', verticalalignment='bottom')
        x, y = line.get_xydata()[3]
        plt.text(x, y, 'Q1: {:.2f}'.format(y), horizontalalignment='right', verticalalignment='bottom')
    for idx, line in enumerate(bp_dict['caps']):
        if idx:
            x, y = line.get_xydata()[0]
            plt.text(x, y, 'max: {:.2f}'.format(y), horizontalalignment='right', verticalalignment='bottom')
        else:
            x, y = line.get_xydata()[0]
            plt.text(x, y, 'min: {:.2f}'.format(y), horizontalalignment='right', verticalalignment='bottom')
    plt.grid(color='0.95', linestyle='-')
    plt.xlabel(algorithm)
    plt.ylabel('Runtime (s)')
    plt.title('Box plot for {} on {}, within solution quality range [{}%, {}%]'.format(algorithm, graph, q_star_range[0], q_star_range[1]))
    plt.savefig(PLOTS_PATH + 'Box_{}_{}_{}_{}.png'.format(algorithm, graph, q_star_range[0], q_star_range[1]))
    plt.show()

def get_exp_T0P_table():
    """
    Get the table of experiment of T0P for LS1 on each graph

    """
    algorithm = 'LS1'
    df_list = {}
    for T0_P in T0_P_LIST:
        results = []
        for graph in get_graph_files():
            dummy = np.zeros((3, 3))
            for seed in range(1, 4):
                file_name = graph + '_' + algorithm + '_' \
                    + str(600) + '_' + str(seed)
                if T0_P != 200:
                    trace = load_trace(file_name, T0_P)
                else:
                    trace = load_trace(file_name)
                if trace is None:
                    continue
                time, num_sol = trace[-1][0], trace[-1][1]
                relative_error = (num_sol - OPT_SOL[graph]) / OPT_SOL[graph] * 100
                dummy[seed - 1, :] = [time, num_sol, relative_error]
            results.append(dummy.mean(axis = 0))
        df_results = pd.DataFrame(results,
                                index=get_graph_files(),
                                columns=['Time (s)',  'VC Value', 'RelErr (%)'])
        df_results = df_results.sort_values(by=['VC Value'])
        df_list[T0_P] = df_results
    return df_list

def T0_P_trace_plot(graph):
    """
    Plot the trace of T0P for LS1 on given graph

    Parameters
    ----------
    graph : Graph
        The graph
    T0_P : int
        The T0_P value
    """
    algorithm = 'LS1'
    seed = 1
    
    file_name = graph + '_' + algorithm + '_' \
                + str(600) + '_' + str(seed)
    plt.figure()
    for T0_P in T0_P_LIST:
        if T0_P != 200:
            trace = load_trace(file_name, T0_P)
        else:
            trace = load_trace(file_name)
        if trace is None:
            continue
        time_q = np.array([np.array([record[0], (record[1] - OPT_SOL[graph]) / OPT_SOL[graph] * 100]) for record in trace])
        plt.plot(time_q[:, 0], time_q[:, 1], label='T0_P = {}'.format(T0_P))
    plt.grid(color='0.95', linestyle='-')
    plt.xlabel('Runtime (s)')
    plt.ylabel('Relative solution Quality (%)')
    plt.title('Trace plot for {} on {}'.format(algorithm, graph))
    plt.legend()
    plt.savefig(PLOTS_PATH + 'Trace_{}_{}.png'.format(algorithm, graph))
    plt.show()


# for debugging purpose
if __name__ == '__main__':
    # get_results_table()
    # get_Ps('power', 'LS1', 600, 8)
    # box_plot('power', 'LS1', [7,10])
    # print(get_exp_T0P_table())
    pass
