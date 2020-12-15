# CSE-571-Pacman-Search-Problem

A Pacman goal-based agent. I have solved several of these search problems using depth-first search, breadth-first search, uniform cost search, and a star search. A full description of the project can be found in ![PJ1-Desp.pdf](https://github.com/forksup/CSE-571-Pacman-Search-Problem/blob/main/PJ1-Desp.pdf).


The goal of this problem is to navigate through a maze and find one food node. Below is an example of the medium maze:

![pacman Domain](https://adrianyi.com/img/Pacman/medium_maze_bfs.gif)

In the [search.py](https://github.com/forksup/CSE-571-Pacman-Search-Problem/blob/main/search.py) file you can see my execution of these algorithm styles. These are used as agents for pathfinding in the Pacman world. 


In the [searchAgents.py](https://github.com/forksup/CSE-571-Pacman-Search-Problem/blob/main/searchAgents.py) file, I created problem definitions to encode the state space differently to allow my search algorithms to solve different problems. Such as the find all corners and eat all food. I developed heuristics that increased the efficiency of the A* algorithm.

A detailed description of the project can be found here:
https://inst.eecs.berkeley.edu/~cs188/sp19/project1.html#Q8
