# CSE6140-Fall-2022-Project-Minimum-Vertex-Cover
CSE6140 Fall 2022 Project: Minimum Vertex Cover

## Executable Usage
Locate to the root directory of the project, and run the following command:
```
python ./code/exec.py -inst <filename> -alg [BnB|Approx|LS1|LS2] -time <cutoff in seconds> -seed <random seed>
```
For example, to execute the heuristic algorithm on the graph instance `dummy1.graph` with a cutoff time of 400 seconds and a random seed of 40, run the following command:
```
python ./code/exec.py -inst dummy1 -alg LS1 -time 400 -seed 40
```
The output will be saved in the `./output` directory.