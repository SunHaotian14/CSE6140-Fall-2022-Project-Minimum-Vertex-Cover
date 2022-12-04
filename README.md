# CSE6140-Fall-2022-Project-Minimum-Vertex-Cover
## Group Members: 
Haotian Sun, Xin Lian, Ruiqi Liu, Zifeng Liu

## Denpendencies
- Python 3.9
- NetworkX 2.8.4
- Matplotlib 3.4.3
- Numpy 1.21.5
- Pandas 1.4.4

## Platform
- OS: macOS 13.0.1
- CPU: Apple M1 Pro
- Memory: 16GB

## Executable Usage
Please locate yourself to the root directory of the project, and run the following command:
```
python ./code/exec.py -inst <filename> -alg [BnB|Approx|LS1|LS2] -time <cutoff in seconds> -seed <random seed>
```
For example, to execute the `Local Search 1` algorithm on the graph instance `dummy1.graph` with a cutoff time of `400` seconds and a random seed of `40`, run the following command:
```
python ./code/exec.py -inst dummy1 -alg LS1 -time 400 -seed 40
```
The output will be saved in the `./output` directory.

## Code Structure
- `./code/`: code directory containing the code for the project
    - `./code/exec.py`: the main executable file that runs the algorithms on the graph instances.
    - `./code/heuristic.py`: the implementation of the Approximation algorithm: Greedy Independent Cover (GIC)
    - `./code/BnB.py`: the implementation of the Branch-and-Bound (BnB) algorithm
    - `./code/local_search_1.py`: the implementation of the first Local Search algorithm: Simulated Annealing (SA)
    - `./code/local_search_2.py`: the implementation of the second Local Search algorithm: Hill Climbing (HC)
    - `./code/io_utils.py`: the implementation of the utility functions for file loading / writing
    - `./code/graph.py`: the implementation of graph data structure
    - `./code/evaluation_tools.py`: the implementation of the evaluation functions, i.e., formulating tables and plotting
    - `./code/evaluation_results.ipynb`: the jupyter notebook for presenting the results
- `./output/`: output directory containing the output files, i.e., solution and trace file
    - `./Exp_T0_P/`: supplementary directory containing the output files for the experiments on the effect of the initial temperature, files inside this directory are named as `<instance>_<method>_<cutoff>_<randSeed>_<T0_P>.*`
